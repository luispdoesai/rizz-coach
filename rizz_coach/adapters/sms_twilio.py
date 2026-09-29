import httpx
from typing import Dict, Any, Optional
from rizz_coach.adapters.base import BasePlatformAdapter
from rizz_coach.config import settings

class TwilioSMSAdapter(BasePlatformAdapter):
    """
    Twilio SMS Adapter for handling incoming text messages via webhook
    and dispatching automated or approved replies.
    """

    def __init__(self):
        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token
        self.from_phone = settings.twilio_phone_number

    async def receive_event(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses Twilio webhook POST form data.
        Twilio sends: From, Body, MessageSid, To, etc.
        """
        sender = form_data.get("From", "unknown")
        body = form_data.get("Body", "").strip()
        message_id = form_data.get("MessageSid", "")

        return {
            "channel": "sms",
            "thread_id": f"sms_{sender}",
            "sender_id": sender,
            "incoming_text": body,
            "raw_id": message_id
        }

    async def send_message(self, recipient_phone: str, text: str) -> bool:
        if not self.account_sid or not self.auth_token or not self.from_phone:
            print(f"[Twilio Adapter Mock] Sent SMS to {recipient_phone}: '{text}'")
            return True

        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
        data = {
            "From": self.from_phone,
            "To": recipient_phone,
            "Body": text
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data, auth=(self.account_sid, self.auth_token))
            return resp.status_code in [200, 201]

twilio_adapter = TwilioSMSAdapter()
