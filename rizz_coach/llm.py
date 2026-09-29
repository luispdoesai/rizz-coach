import json
import httpx
from typing import List, Dict, Any, Optional
from rizz_coach.config import settings

class LLMClient:
    """
    Unified LLM Client supporting OpenAI-compatible APIs, Anthropic, Ollama, 
    and a Smart Mock Engine for testing/offline use.
    """

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        self.provider = provider or settings.llm_provider
        self.model = model or settings.llm_model
        self.api_key = settings.llm_api_key
        self.base_url = settings.llm_base_url
        self.ollama_base_url = settings.ollama_base_url

    async def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
        """Generates text from LLM or smart mock fallback."""
        if self.provider == "mock" or not self.api_key and self.provider != "ollama":
            return self._mock_generate(system_prompt, user_prompt)

        try:
            if self.provider in ["openai", "groq", "deepseek"]:
                return await self._call_openai_compatible(system_prompt, user_prompt, temperature)
            elif self.provider == "anthropic":
                return await self._call_anthropic(system_prompt, user_prompt, temperature)
            elif self.provider == "ollama":
                return await self._call_ollama(system_prompt, user_prompt, temperature)
            else:
                return self._mock_generate(system_prompt, user_prompt)
        except Exception as e:
            print(f"[LLMClient Warning] Call failed ({e}). Falling back to smart mock response.")
            return self._mock_generate(system_prompt, user_prompt)

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Generates structured JSON."""
        full_system = system_prompt + "\n\nCRITICAL: Respond ONLY with valid JSON. Do not wrap in markdown quotes if possible, or use standard ```json."
        raw = await self.generate(full_system, user_prompt, temperature=0.3)
        return self._extract_json(raw)

    async def _call_openai_compatible(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    async def _call_anthropic(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": self.model or "claude-3-5-sonnet-20240620",
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "max_tokens": 1024,
            "temperature": temperature
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"]

    async def _call_ollama(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = f"{self.ollama_base_url.rstrip('/')}/api/chat"
        payload = {
            "model": self.model or "llama3.2",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "options": {"temperature": temperature},
            "stream": False
        }
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["message"]["content"]

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Cleans and extracts JSON payload from LLM responses."""
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except Exception:
            # Fallback regex search for JSON brackets
            import re
            match = re.search(r'(\{.*\})', cleaned, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    pass
            return {"raw_response": text, "parse_error": True}

    def _mock_generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Smart offline mock generator simulating high-tier dating coach responses
        for instant testing without needing API keys.
        """
        lower_prompt = user_prompt.lower()

        # If JSON is expected for analysis
        if "subtext" in system_prompt.lower() or "analyze" in system_prompt.lower():
            return json.dumps({
                "interest_score": 78,
                "interest_level": "High - Testing / Banter",
                "subtext_translation": "She's matching your playful energy but testing to see if you can hold your frame or fold into interview mode.",
                "frame_holder": "Neutral / Contested",
                "investment_ratio": "User: 42 words | Her: 29 words (Healthy balance)",
                "cringe_warnings": ["Avoid double-texting if she pauses", "Do not ask generic job/school questions now"],
                "tactical_moves": [
                    {
                        "category": "Banter / Push-Pull",
                        "text": "Careful, keep smiling like that and I might actually believe you're innocent.",
                        "rizz_score": 92,
                        "rationale": "Creates playful tension by teasing her innocence without putting her on a pedestal."
                    },
                    {
                        "category": "Direct Escalation",
                        "text": "You're dangerously witty over text. Let's see if that holds up over a dirty martini this Thursday.",
                        "rizz_score": 88,
                        "rationale": "Compliments her vibe while immediately challenging her to real-world drinks."
                    },
                    {
                        "category": "Low-Investment Reset",
                        "text": "Haha fair enough. Don't tell me you're actually serious about that.",
                        "rizz_score": 75,
                        "rationale": "Keeps the pace relaxed without over-investing if her text was short."
                    }
                ]
            })

        # If Autopsy is requested
        if "autopsy" in system_prompt.lower() or "ghost" in system_prompt.lower():
            return json.dumps({
                "status": "GHOSTED_OR_STALLED",
                "fatal_turn": "Turn 4: You answered her question with a paragraph and asked 3 questions in a row.",
                "root_cause": "Conversational overload & loss of tension. She felt like she was filling out a survey.",
                "recovery_probability": "65%",
                "revival_texts": [
                    {
                        "name": "The Playful Callout (High ROI)",
                        "text": "Are you always this quiet or am I just that intimidating?",
                        "why_it_works": "Flips the frame playfully without sounding bitter."
                    },
                    {
                        "name": "The Random Curiosity Ping",
                        "text": "Saw something today that immediately made me think of your questionable music taste.",
                        "why_it_works": "Creates an open loop she will naturally ask 'Wait what?' to."
                    }
                ]
            })

        # If Profile Review is requested
        if "profile" in system_prompt.lower() or "bio" in system_prompt.lower():
            return json.dumps({
                "overall_score": 74,
                "photo_audit": [
                    {"photo_num": 1, "score": 85, "verdict": "Solid clear headshot with good lighting. Keep as primary."},
                    {"photo_num": 2, "score": 50, "verdict": "Sunglasses photo. Hides facial symmetry; replace with an action/activity shot."},
                    {"photo_num": 3, "score": 60, "verdict": "Group photo where it takes >2 seconds to find you. Crop tighter or swap."}
                ],
                "bio_critique": "A bit too generic. Listing your hobbies like a resume lowers intrigue.",
                "improved_bios": [
                    {
                        "style": "Witty & Polarizing",
                        "bio": "6'1. Probably better at Mario Kart than you. Looking for someone to debate whether cereal is soup over spicy margaritas."
                    },
                    {
                        "style": "High-Value Minimalist",
                        "bio": "Designing things & searching for the best espresso in the city. Convince me your music taste isn't terrible."
                    }
                ]
            })

        # If Sparring Gym is requested
        if "gym" in system_prompt.lower() or "sparring" in system_prompt.lower():
            return json.dumps({
                "character_reply": "Haha oh really? And why on earth would I do that? You haven't proven you're even fun yet 😏",
                "coach_feedback": {
                    "turn_rizz_score": 84,
                    "what_worked": "Great bold escalation. You put her on the spot without being creepy.",
                    "coaching_tip": "She's teasing you to qualify yourself. DO NOT list your resume; tease back."
                }
            })

        # Generic response
        return "You're holding the frame well. Focus on matching her message length and tease her with an assumption rather than an interview question."

# Global default instance
llm_client = LLMClient()
