import os
from functools import lru_cache

PROMPTS_DIR = os.path.dirname(os.path.abspath(__file__))

@lru_cache(maxsize=32)
def load_prompt(filename: str, fallback_default: str = "") -> str:
    """
    Loads a markdown prompt template from the rizz_coach/prompts directory.
    Caches the result in memory for zero-overhead runtime performance.
    """
    if not filename.endswith(".md"):
        filename = f"{filename}.md"
    
    filepath = os.path.join(PROMPTS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
            
    return fallback_default.strip()
