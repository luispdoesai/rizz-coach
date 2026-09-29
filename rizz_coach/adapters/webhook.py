from typing import Dict, Any
from rizz_coach.adapters.base import BasePlatformAdapter

class GenericWebhookAdapter(BasePlatformAdapter):
    """
    Generic webhook adapter that enables iOS Shortcuts, Zapier, n8n,
    or custom scripts to stream messages in and receive tactical moves.
    """

    async def receive_event(self, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "channel": raw_payload.get("channel", "generic"),
            "thread_id": raw_payload.get("thread_id", "default_thread"),
            "sender_id": raw_payload.get("sender_id", "external_contact"),
            "incoming_text": raw_payload.get("message", raw_payload.get("text", "")),
            "context": raw_payload.get("context", "")
        }

    async def send_message(self, recipient_id: str, text: str) -> bool:
        print(f"[Webhook Adapter] Outbound dispatched to {recipient_id}: '{text}'")
        return True

webhook_adapter = GenericWebhookAdapter()
