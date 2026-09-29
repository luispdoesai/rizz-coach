from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from rizz_coach.llm import LLMClient, llm_client

class TacticalMove(BaseModel):
    category: str  # "Banter / Push-Pull", "Direct Escalation", "Low-Investment Reset"
    text: str
    rizz_score: int
    rationale: str

class AnalysisReport(BaseModel):
    interest_score: int          # 0 - 100
    interest_level: str          # "High / Flirty", "Medium / Banter", "Dry / Stalled", "Hostile"
    subtext_translation: str     # What she said vs. what she actually means
    frame_holder: str            # "You lead", "She leads", "Neutral / Contested"
    investment_ratio: str        # e.g., "User: 34 words | Match: 12 words"
    cringe_warnings: List[str]   # Flags needy or over-invested behavior
    tactical_moves: List[TacticalMove]

ANALYZER_SYSTEM_PROMPT = """
You are an elite, modern dating coach and master conversationalist.
Your role is to act as a wingman: decode the hidden subtext of a conversation, calculate interest level, identify frame control, and recommend 3 tactical next moves.

You must respond in strict JSON matching this schema:
{
  "interest_score": <int between 0 and 100>,
  "interest_level": "<string e.g. High / Flirty, Medium / Banter, Dry / Stalled, Low / Skeptical>",
  "subtext_translation": "<concise explanation of what her message actually means emotionally and dynamically>",
  "frame_holder": "<You lead | She leads | Neutral / Contested>",
  "investment_ratio": "<Comparison of effort, word length, and questions>",
  "cringe_warnings": ["<List of behaviors the user must avoid, e.g., double texting, over-apologizing>"],
  "tactical_moves": [
    {
      "category": "Banter / Push-Pull",
      "text": "<playful, tension-building response>",
      "rizz_score": <int 80-99>,
      "rationale": "<psychological reason why this works>"
    },
    {
      "category": "Direct Escalation",
      "text": "<smooth invitation for drink/date or phone number>",
      "rizz_score": <int 80-99>,
      "rationale": "<why this smoothly escalates>"
    },
    {
      "category": "Low-Investment Reset",
      "text": "<relaxed, unbothered reply if her text is dry>",
      "rizz_score": <int 70-85>,
      "rationale": "<why this matches pace without losing frame>"
    }
  ]
}

Guidelines:
- Never generate creepy or pushy PUA lines.
- Favor clever banter, playful teasing, and authentic confidence.
- Lowercase / casual texting style that sounds 100% human.
"""

class ConversationAnalyzer:
    def __init__(self, client: Optional[LLMClient] = None):
        self.client = client or llm_client

    async def analyze(self, chat_history: str, target_name: Optional[str] = "Match") -> AnalysisReport:
        user_prompt = f"""
Target Name: {target_name}
Conversation History (latest message at bottom):
----------------------------------------
{chat_history}
----------------------------------------
Analyze this conversation, decode the subtext, and produce the 3 best tactical responses.
"""
        data = await self.client.generate_json(ANALYZER_SYSTEM_PROMPT, user_prompt)
        
        # Ensure fallback defaults if parsing missed keys
        moves = [
            TacticalMove(
                category=m.get("category", "Banter"),
                text=m.get("text", "Haha fair point, but don't get ahead of yourself."),
                rizz_score=m.get("rizz_score", 85),
                rationale=m.get("rationale", "Playful frame maintenance.")
            )
            for m in data.get("tactical_moves", [])
        ]

        if not moves:
            moves = [
                TacticalMove(
                    category="Banter / Push-Pull",
                    text="You talk a big game. Let's see if that holds up over drinks this week.",
                    rizz_score=89,
                    rationale="Challenges her playfully while creating an opening for a date."
                )
            ]

        return AnalysisReport(
            interest_score=data.get("interest_score", 70),
            interest_level=data.get("interest_level", "Medium / Banter"),
            subtext_translation=data.get("subtext_translation", "She is testing your confidence."),
            frame_holder=data.get("frame_holder", "Neutral"),
            investment_ratio=data.get("investment_ratio", "Balanced effort detected"),
            cringe_warnings=data.get("cringe_warnings", ["Keep it brief; do not over-explain."]),
            tactical_moves=moves
        )
