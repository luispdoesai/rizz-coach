from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BasePlatformAdapter(ABC):
    """Abstract platform connector for receiving & sending messages."""
    
    @abstractmethod
    async def receive_event(self, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize platform-specific payload into a standard event."""
        pass

    @abstractmethod
    async def send_message(self, recipient_id: str, text: str) -> bool:
        """Send message out through platform API."""
        pass
