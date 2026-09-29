from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BasePlatformConnector(ABC):
    """
    Abstract Base Class for social and dating platform connectors.
    Provides standardized interface for Tinder, Instagram, Bumble, etc.
    """
    platform_name: str = "generic"

    @abstractmethod
    async def is_authenticated(self) -> bool:
        """Checks if current auth credentials/token are valid."""
        pass

    @abstractmethod
    async def fetch_new_matches(self) -> List[Dict[str, Any]]:
        """
        Fetches recent matches that have zero or unreplied messages.
        Returns a list of match dicts:
        [{
            "match_id": str,
            "name": str,
            "bio": str,
            "age": Optional[int],
            "photos": List[str],
            "last_message": Optional[str]
        }]
        """
        pass

    @abstractmethod
    async def fetch_chat_history(self, match_id: str) -> str:
        """Fetches and formats recent chat history for a match."""
        pass

    @abstractmethod
    async def send_message(self, match_id: str, text: str) -> bool:
        """Sends a text message to a specific match on the platform."""
        pass
