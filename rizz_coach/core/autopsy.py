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

from rizz_coach.prompts import load_prompt

def get_autopsy_system_prompt() -> str:
    return load_prompt("autopsy.md")


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
        data = await self.client.generate_json(get_autopsy_system_prompt(), user_prompt)
        
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
