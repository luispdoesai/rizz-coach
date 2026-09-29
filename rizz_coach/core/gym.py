from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from rizz_coach.llm import LLMClient, llm_client

class CoachSidelineFeedback(BaseModel):
    turn_rizz_score: int
    what_worked: str
    coaching_tip: str

class GymTurnResponse(BaseModel):
    character_name: str
    character_reply: str
    coach_feedback: CoachSidelineFeedback

ARCHETYPES = {
    "elena": {
        "name": "Elena (The Skeptical High-Flyer)",
        "persona": "Corporate consultant in NYC. Smart, busy, and skeptical of men who try too hard. She tests whether you fold or qualify yourself when challenged.",
        "opener": "I usually delete this app after 5 minutes. Convince me why I shouldn't."
    },
    "chloe": {
        "name": "Chloe (The Banter Queen)",
        "persona": "Sharp, witty, playful, and loves roasting. If you give a boring answer, she will tease you immediately.",
        "opener": "Your profile looks like a curated advertisement for a good boy. Are you actually fun or just well-behaved?"
    },
    "mia": {
        "name": "Mia (The Dry / One-Word Replier)",
        "persona": "Sends very short, lukewarm replies ('haha cool', 'wyd'). Hardest test: can you lead and build intrigue without writing essays in response?",
        "opener": "hey"
    },
    "sofia": {
        "name": "Sofia (The Adventurous Creative)",
        "persona": "Photographer who loves spontaneous adventures, deep late-night topics, and banter about art and travel.",
        "opener": "If we were skipping town right now, what's our first terrible spontaneous decision?"
    }
}

GYM_SYSTEM_PROMPT = """
You are acting in a double role:
1. CHARACTER ROLEPLAY: You are roleplaying as {char_name}: {char_persona}
   Reply naturally to the user in 1-2 casual sentences as this character.
2. EXPERT DATING COACH SIDELINE: Evaluate the user's latest text. Did they hold frame? Were they witty, needy, boring, or smooth?

Respond in strict JSON:
{
  "character_reply": "<Character's spoken text in lowercase/casual tone>",
  "coach_feedback": {
    "turn_rizz_score": <0-100 integer>,
    "what_worked": "<Positive aspect of user's text>",
    "coaching_tip": "<Actionable instruction for how to respond next>"
  }
}
"""

class RizzGym:
    def __init__(self, client: Optional[LLMClient] = None):
        self.client = client or llm_client

    def get_archetypes(self) -> Dict[str, Dict[str, str]]:
        return ARCHETYPES

    async def step(self, archetype_id: str, user_message: str, history: List[Dict[str, str]]) -> GymTurnResponse:
        char = ARCHETYPES.get(archetype_id, ARCHETYPES["chloe"])
        sys_prompt = GYM_SYSTEM_PROMPT.replace(
            "{char_name}", char["name"]
        ).replace(
            "{char_persona}", char["persona"]
        )

        formatted_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-6:]])
        user_prompt = f"""
Conversation History:
{formatted_history}

User's Latest Move: "{user_message}"
"""
        data = await self.client.generate_json(sys_prompt, user_prompt)
        
        feedback_raw = data.get("coach_feedback", {})
        feedback = CoachSidelineFeedback(
            turn_rizz_score=feedback_raw.get("turn_rizz_score", 82),
            what_worked=feedback_raw.get("what_worked", "Good playful confidence."),
            coaching_tip=feedback_raw.get("coaching_tip", "Keep your reply punchy; don't over-explain.")
        )

        return GymTurnResponse(
            character_name=char["name"],
            character_reply=data.get("character_reply", "Haha is that your best shot?"),
            coach_feedback=feedback
        )
