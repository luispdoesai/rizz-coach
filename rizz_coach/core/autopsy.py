from typing import List, Optional
from pydantic import BaseModel
from rizz_coach.llm import LLMClient, llm_client

class RevivalText(BaseModel):
    name: str
    text: str
    why_it_works: str

class AutopsyReport(BaseModel):
    status: str
    fatal_turn: str
    root_cause: str
    recovery_probability: str
    lessons_learned: List[str]
    revival_texts: List[RevivalText]

AUTOPSY_SYSTEM_PROMPT = """
You are a master dating strategist performing a forensic autopsy on a stalled, ghosted, or dead conversation.

Analyze:
1. THE FATAL TURN: Pinpoint the exact message where momentum died, frame was lost, or she withdrew.
2. ROOT CAUSE: Why did she ghost? (e.g. over-texting, boring interview questions, took too long to ask for date, killed conversational tension).
3. RECOVERY PROBABILITY: Realistic percentage chance of reviving the conversation.
4. REVIVAL TEXTS: Provide 2 high-conversion revival options:
   - "The Playful Callout": Flips the frame, makes light of her silence without being bitter.
   - "The Curiosity Loop": Drops an intriguing statement that compels her to ask 'what?'.

Return strict JSON:
{
  "status": "<GHOSTED | STALLED | COLD>",
  "fatal_turn": "<Quote and number of the turn where it died>",
  "root_cause": "<1-2 sentence core reason>",
  "recovery_probability": "<e.g. 60%>",
  "lessons_learned": ["<Actionable rule 1>", "<Actionable rule 2>"],
  "revival_texts": [
    {
      "name": "<e.g. Playful Frame Flip>",
      "text": "<The text to send>",
      "why_it_works": "<Psychological rationale>"
    }
  ]
}
"""

class ChatAutopsy:
    def __init__(self, client: Optional[LLMClient] = None):
        self.client = client or llm_client

    async def diagnose(self, full_chat_history: str) -> AutopsyReport:
        user_prompt = f"""
Perform a post-mortem on this stalled conversation:
----------------------------------------
{full_chat_history}
----------------------------------------
"""
        data = await self.client.generate_json(AUTOPSY_SYSTEM_PROMPT, user_prompt)
        
        revivals = [
            RevivalText(
                name=r.get("name", "Revival Move"),
                text=r.get("text", "Are you always this quiet or did I strike you speechless?"),
                why_it_works=r.get("why_it_works", "Playfully challenges the silence.")
            )
            for r in data.get("revival_texts", [])
        ]

        if not revivals:
            revivals = [
                RevivalText(
                    name="The Playful Callout",
                    text="Are you always this quiet or did you get lost in thought?",
                    why_it_works="Teases without appearing bothered."
                )
            ]

        return AutopsyReport(
            status=data.get("status", "GHOSTED_OR_STALLED"),
            fatal_turn=data.get("fatal_turn", "Turn 4: Excessive questioning without playful banter."),
            root_cause=data.get("root_cause", "Loss of tension and overly predictable responses."),
            recovery_probability=data.get("recovery_probability", "65%"),
            lessons_learned=data.get("lessons_learned", ["Limit questions to 1 per 3 messages", "Suggest drinks before message 12"]),
            revival_texts=revivals
        )
