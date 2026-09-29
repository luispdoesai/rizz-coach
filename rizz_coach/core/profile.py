from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from rizz_coach.llm import LLMClient, llm_client

class ImprovedBio(BaseModel):
    style: str
    bio: str

class PhotoAuditItem(BaseModel):
    photo_num: int
    score: int
    verdict: str

class ProfileAuditReport(BaseModel):
    overall_score: int
    photo_audit: List[PhotoAuditItem]
    bio_critique: str
    cliches_detected: List[str]
    improved_bios: List[ImprovedBio]

PROFILE_SYSTEM_PROMPT = """
You are an elite dating profile consultant and photographer critic.
Evaluate dating profile inputs (bio, prompts, and photo notes).

Score the profile out of 100 based on:
- High Status & Intrigue (does it trigger curiosity or look like a job resume?)
- Polarization (is it memorable or boringly agreeable?)
- Photo quality & vibe balance (headshots, social proof, fitness, lifestyle)

Detect classic cliches:
- Gym selfie / bathroom mirror pic
- Sunglasses hiding eye contact
- Confusing group photos
- "Fluent in sarcasm" / "Looking for my partner in crime" / "Love traveling and food"

Generate 3 high-converting bio replacements:
1. Witty & Polarizing (provokes playful debate)
2. High-Value Minimalist (effortless, cool)
3. Playful Storyteller (distinctive scenario hook)

Return strict JSON matching this schema:
{
  "overall_score": <0-100>,
  "photo_audit": [
    {"photo_num": 1, "score": <0-100>, "verdict": "<Honest critique>"}
  ],
  "bio_critique": "<Detailed breakdown of what is hurting the bio>",
  "cliches_detected": ["<List of clichés found>"],
  "improved_bios": [
    {"style": "<Style Name>", "bio": "<Text>"}
  ]
}
"""

class ProfileAuditor:
    def __init__(self, client: Optional[LLMClient] = None):
        self.client = client or llm_client

    async def audit(self, bio: str, photo_descriptions: Optional[str] = "", prompts_text: Optional[str] = "") -> ProfileAuditReport:
        user_prompt = f"""
Current Bio: "{bio}"
Profile Prompts/Q&A: "{prompts_text}"
Photo Descriptions/Notes: "{photo_descriptions}"
"""
        data = await self.client.generate_json(PROFILE_SYSTEM_PROMPT, user_prompt)

        improved_bios = [
            ImprovedBio(style=b.get("style", "Modern"), bio=b.get("bio", "Exploring the city and hunting down the best espresso."))
            for b in data.get("improved_bios", [])
        ]
        if not improved_bios:
            improved_bios = [
                ImprovedBio(style="Witty & Polarizing", bio="6'1. Probably better at Mario Kart than you. Looking for someone to debate whether cereal is soup."),
                ImprovedBio(style="High-Value Minimalist", bio="Designing tech by day, finding hidden speakeasies by night. Convince me your music taste isn't terrible.")
            ]

        photo_audit = [
            PhotoAuditItem(photo_num=p.get("photo_num", i+1), score=p.get("score", 75), verdict=p.get("verdict", "Good clear picture."))
            for i, p in enumerate(data.get("photo_audit", []))
        ]
        if not photo_audit:
            photo_audit = [
                PhotoAuditItem(photo_num=1, score=85, verdict="Solid clear headshot with good lighting. Keep as primary."),
                PhotoAuditItem(photo_num=2, score=65, verdict="Decent lifestyle photo, but ensure smiling with teeth.")
            ]

        return ProfileAuditReport(
            overall_score=data.get("overall_score", 72),
            photo_audit=photo_audit,
            bio_critique=data.get("bio_critique", "Bio relies on standard clichés. Needs more distinctive hooks."),
            cliches_detected=data.get("cliches_detected", ["Generic hobby listing", "Safe agreeable tone"]),
            improved_bios=improved_bios
        )
