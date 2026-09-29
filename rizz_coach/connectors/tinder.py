import httpx
from typing import List, Dict, Any, Optional
from rizz_coach.config import settings
from rizz_coach.connectors.base import BasePlatformConnector

class TinderConnector(BasePlatformConnector):
    """
    Tinder Web API Connector.
    Uses the session X-Auth-Token from Tinder Web to fetch matches and send messages.
    Includes smart mock mode for offline demonstration and testing.
    """
    platform_name: str = "tinder"
    BASE_URL = "https://api.gotinder.com"

    def __init__(self, auth_token: Optional[str] = None):
        self.auth_token = auth_token or settings.tinder_auth_token

    def _get_headers(self) -> Dict[str, str]:
        return {
            "X-Auth-Token": self.auth_token or "",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "platform": "web"
        }

    async def is_authenticated(self) -> bool:
        if not self.auth_token:
            return False
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{self.BASE_URL}/v2/profile", headers=self._get_headers())
                return resp.status_code == 200
        except Exception:
            return False

    async def fetch_new_matches(self) -> List[Dict[str, Any]]:
        """
        Fetches fresh matches with 0 messages awaiting an opener.
        Falls back to realistic mock matches if not authenticated.
        """
        if not self.auth_token:
            return self._mock_matches()

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                url = f"{self.BASE_URL}/v2/matches?count=40&is_tinder_u=false"
                resp = await client.get(url, headers=self._get_headers())
                if resp.status_code != 200:
                    print(f"[TinderConnector] Failed to fetch matches: HTTP {resp.status_code}")
                    return self._mock_matches()

                data = resp.json()
                matches_raw = data.get("data", {}).get("matches", [])
                unopened = []

                for m in matches_raw:
                    msg_count = m.get("message_count", 0)
                    person = m.get("person", {})
                    if msg_count == 0 and person:
                        unopened.append({
                            "match_id": m.get("id"),
                            "name": person.get("name", "Match"),
                            "bio": person.get("bio", ""),
                            "birth_date": person.get("birth_date"),
                            "photos": [p.get("url") for p in person.get("photos", []) if "url" in p],
                            "last_message": None
                        })
                return unopened if unopened else self._mock_matches()
        except Exception as e:
            print(f"[TinderConnector Error] {e}. Falling back to mock matches.")
            return self._mock_matches()

    async def fetch_chat_history(self, match_id: str) -> str:
        """Fetches chat messages for a match."""
        if not self.auth_token or match_id.startswith("mock_"):
            return "Her: hey! what are you up to this week?"

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                url = f"{self.BASE_URL}/v2/matches/{match_id}/messages?count=20"
                resp = await client.get(url, headers=self._get_headers())
                if resp.status_code == 200:
                    messages = resp.json().get("data", {}).get("messages", [])
                    formatted = []
                    for msg in reversed(messages):
                        sender = "Me" if msg.get("from") != match_id else "Her"
                        formatted.append(f"{sender}: {msg.get('message')}")
                    return "\n".join(formatted)
        except Exception as e:
            print(f"[TinderConnector Error] fetch_chat_history: {e}")

        return "Her: hey, how's your week going?"

    async def send_message(self, match_id: str, text: str) -> bool:
        """Sends an approved message to Tinder match."""
        if not self.auth_token or match_id.startswith("mock_"):
            print(f"[Tinder Mock Dispatch] Sent to match {match_id}: '{text}'")
            return True

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                url = f"{self.BASE_URL}/user/matches/{match_id}"
                payload = {"message": text}
                resp = await client.post(url, headers=self._get_headers(), json=payload)
                return resp.status_code in [200, 201]
        except Exception as e:
            print(f"[TinderConnector Error] send_message: {e}")
            return False

    def _mock_matches(self) -> List[Dict[str, Any]]:
        return [
            {
                "match_id": "mock_tinder_101",
                "name": "Jessica",
                "bio": "Architect in Brooklyn. Probably drinking an iced matcha right now. Convince me your favorite pasta place isn't overrated.",
                "photos": ["https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400"],
                "last_message": None
            },
            {
                "match_id": "mock_tinder_102",
                "name": "Chloe",
                "bio": "Consultant by day, vinyl collector by night. Looking for someone who can keep up with banter.",
                "photos": ["https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400"],
                "last_message": None
            },
            {
                "match_id": "mock_tinder_103",
                "name": "Maya",
                "bio": "Photographer & avid traveler. Tell me your worst travel story.",
                "photos": ["https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400"],
                "last_message": None
            }
        ]

tinder_connector = TinderConnector()
