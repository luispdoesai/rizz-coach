import re
import random
from datetime import datetime
from typing import Optional, Tuple
from pydantic import BaseModel
from rizz_coach.config import settings

class AutomationDecision(BaseModel):
    action: str              # "AUTO_REPLY_QUEUED", "HANDOFF_TO_USER", "ABORT_THREAD", "MANUAL_REVIEW"
    outcome_status: str      # "ACTIVE", "CONVERTED_NUMBER", "CONVERTED_DATE", "FAILED_REJECTED", "GHOSTED"
    reason: str
    contact_extracted: Optional[str] = None
    scheduled_delay_seconds: int = 0

class AutomationEngine:
    def __init__(self):
        self.phone_regex = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        self.instagram_regex = re.compile(r'(?:ig|insta|instagram)?\s*[:@]\s*([a-zA-Z0-9._]{3,30})', re.IGNORECASE)

    def evaluate_inbound_outcome(self, incoming_text: str) -> Tuple[str, Optional[str]]:
        """
        Heuristic fast-pass for success or rejection detection.
        Returns (status, extracted_contact).
        """
        # Phone extraction
        phone_match = self.phone_regex.search(incoming_text)
        if phone_match:
            return "CONVERTED_NUMBER", phone_match.group(0).strip()

        # Instagram handle extraction
        ig_match = self.instagram_regex.search(incoming_text)
        if ig_match and ("insta" in incoming_text.lower() or "ig" in incoming_text.lower() or "@" in incoming_text):
            return "CONVERTED_NUMBER", f"@{ig_match.group(1).strip()}"

        lower = incoming_text.lower()
        
        # Date agreement triggers
        date_triggers = [
            "sounds good let's do drinks",
            "thursday works",
            "friday works",
            "let's do it",
            "see you then",
            "i'd love to meet up",
            "down for drinks",
            "what time works for you"
        ]
        if any(t in lower for t in date_triggers):
            return "CONVERTED_DATE", None

        # Rejection triggers
        rejection_triggers = [
            "stop texting me",
            "not interested",
            "leave me alone",
            "i have a boyfriend",
            "unmatch me"
        ]
        if any(r in lower for r in rejection_triggers):
            return "FAILED_REJECTED", None

        return "ACTIVE", None

    def calculate_human_delay(self, partner_response_time_seconds: Optional[int] = None) -> int:
        """
        Calculates a natural human-like delay with jitter so the bot never feels robotic.
        """
        min_sec = settings.automation_min_delay_seconds
        max_sec = settings.automation_max_delay_seconds

        if partner_response_time_seconds and partner_response_time_seconds > 60:
            # Match their pace ± 25% (bounded by min/max)
            base_delay = int(partner_response_time_seconds * random.uniform(0.75, 1.25))
            return max(min_sec, min(base_delay, max_sec))

        # Default random jitter
        return random.randint(min_sec, max_sec)

    def process_message(self, incoming_text: str, auto_mode: Optional[str] = None) -> AutomationDecision:
        mode = auto_mode or settings.automation_mode
        status, contact = self.evaluate_inbound_outcome(incoming_text)

        # 1. Success condition (Number / Date won) -> Always hand off to user so they don't fumble the real date!
        if status in ["CONVERTED_NUMBER", "CONVERTED_DATE"]:
            return AutomationDecision(
                action="HANDOFF_TO_USER",
                outcome_status=status,
                reason="Goal achieved! Contact info or date agreement secured.",
                contact_extracted=contact,
                scheduled_delay_seconds=0
            )

        # 2. Rejection condition -> Abort immediately
        if status == "FAILED_REJECTED":
            return AutomationDecision(
                action="ABORT_THREAD",
                outcome_status=status,
                reason="Rejection trigger detected. Conversation aborted.",
                contact_extracted=None,
                scheduled_delay_seconds=0
            )

        # 3. Ongoing conversation
        if mode == "autonomous":
            delay = self.calculate_human_delay()
            return AutomationDecision(
                action="AUTO_REPLY_QUEUED",
                outcome_status="ACTIVE",
                reason=f"Auto-reply scheduled with human-pacing delay ({delay}s).",
                contact_extracted=None,
                scheduled_delay_seconds=delay
            )
        else:
            return AutomationDecision(
                action="MANUAL_REVIEW",
                outcome_status="ACTIVE",
                reason="Copilot mode active: Tactical moves ready for user selection.",
                contact_extracted=None,
                scheduled_delay_seconds=0
            )

automation_engine = AutomationEngine()
