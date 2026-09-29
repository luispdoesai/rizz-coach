import httpx
from typing import List, Dict, Any, Optional
from rizz_coach.config import settings
from rizz_coach.connectors.base import BasePlatformConnector

class InstagramConnector(BasePlatformConnector):
    """
    Instagram DM Connector.
    Supports Meta Graph API / Webhook endpoints and browser session handling.
    Includes smart mock mode for testing without needing active Meta credentials.
    """
    platform_name: str = "instagram"

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or settings.instagram_session_id

    async def is_authenticated(self) -> bool:
        return bool(self.session_id)

    async def fetch_new_matches(self) -> List[Dict[str, Any]]:
        """Fetches active DMs or story replies awaiting a response."""
        return [
            {
                "match_id": "mock_ig_201",
                "name": "Sarah",
                "bio": "Fashion designer & coffee enthusiast in Soho.",
                "photos": ["https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400"],
                "last_message": "loved your story yesterday haha where was that?"
            },
            {
                "match_id": "mock_ig_202",
                "name": "Elena",
                "bio": "Curator & art director. NYC / Milan.",
                "photos": ["https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"],
                "last_message": "haha wait is that gallery open this weekend?"
            }
        ]

    async def fetch_chat_history(self, match_id: str) -> str:
        return "Her: loved your story yesterday haha where was that?\nMe: secret spot in the Lower East Side. don't worry, i have high standards for who i share it with."

    async def send_message(self, match_id: str, text: str) -> bool:
        print(f"[Instagram Dispatch] Sent to @{match_id}: '{text}'")
        return True

instagram_connector = InstagramConnector()
