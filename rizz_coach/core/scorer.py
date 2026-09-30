import re
from typing import List, Optional
from pydantic import BaseModel
from rizz_coach.llm import LLMClient, llm_client

class RizzScorecard(BaseModel):
    score: int                  # 0 - 100
    letter_grade: str           # "A+", "A", "B", "C", "D", "F"
    is_cringe: bool
    cringe_flags: List[str]
    pacing_rating: str          # "Too fast", "Ideal", "Lagging"
    why_it_scored: str
    suggested_rewrite: Optional[str] = None

from rizz_coach.prompts import load_prompt

def get_scorer_system_prompt() -> str:
    return load_prompt("scorer.md")


class RizzScorer:
    def __init__(self, client: Optional[LLMClient] = None):
        self.client = client or llm_client

    async def score_message(self, draft_message: str, context_message: str = "") -> RizzScorecard:
        # Rule-based pre-check for blatant cringe triggers
        quick_flags = []
        lower_draft = draft_message.lower()

        if any(w in lower_draft for w in ["most beautiful girl", "goddess", "drop dead gorgeous", "please reply"]):
            quick_flags.append("pedestalizing (putting her on a pedestal too soon)")

        if any(w in lower_draft for w in ["how was your day", "how is work", "how's your monday", "what are your hobbies"]):
            quick_flags.append("interview_mode (generic filler question)")

        if len(draft_message.split()) > 35 and len(context_message.split()) < 8:
            quick_flags.append("essay_trap (huge message length disparity)")

        user_prompt = f"""
Context / Her Last Message: "{context_message}"
User Drafted Message: "{draft_message}"
Pre-detected heuristic flags: {quick_flags}
"""
        data = await self.client.generate_json(get_scorer_system_prompt(), user_prompt)

        flags = list(set(quick_flags + data.get("cringe_flags", [])))
        score = data.get("score", 75)
        
        # Determine letter grade
        if score >= 93:
            grade = "A+"
        elif score >= 85:
            grade = "A"
        elif score >= 75:
            grade = "B"
        elif score >= 65:
            grade = "C"
        elif score >= 50:
            grade = "D"
        else:
            grade = "F"

        return RizzScorecard(
            score=score,
            letter_grade=grade,
            is_cringe=score < 65 or len(flags) > 0,
            cringe_flags=flags,
            pacing_rating=data.get("pacing_rating", "Ideal"),
            why_it_scored=data.get("why_it_scored", "Decent message but could have more punch."),
            suggested_rewrite=data.get("suggested_rewrite")
        )

    async def score_draft(self, draft_message: str, context_message: str = "") -> RizzScorecard:
        """Alias for score_message to support mobile/bot adapters."""
        return await self.score_message(draft_message=draft_message, context_message=context_message)

