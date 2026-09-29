import httpx
from typing import Optional, Dict, Any
from rizz_coach.config import settings

class TelegramBotWingman:
    """
    Telegram Mobile Wingman bot integration.
    Allows users to forward texts or send screenshots and receive instant
    subtext breakdowns, tactical moves, and cringe interception directly on their phone.
    """

    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.telegram_bot_token
        self.api_url = f"https://api.telegram.org/bot{self.token}" if self.token else None

    async def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
        if not self.api_url:
            print(f"[Telegram Mock] Sent to {chat_id}:\n{text}")
            return True

        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            return resp.status_code == 200

    def format_coaching_card(self, analysis_report) -> str:
        """Formats the analysis report into a punchy Telegram markdown message."""
        moves_text = ""
        for i, move in enumerate(analysis_report.tactical_moves, 1):
            moves_text += f"\n*{i}. [{move.category}]* (Rizz: {move.rizz_score}/100)\n`{move.text}`\n_Why:_ {move.rationale}\n"

        warnings = "\n".join([f"⚠️ {w}" for w in analysis_report.cringe_warnings])

        return (
            f"🎯 *WINGMAN ANALYSIS REPORT*\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📊 *Interest Score:* {analysis_report.interest_score}/100 ({analysis_report.interest_level})\n"
            f"🧐 *Subtext:* {analysis_report.subtext_translation}\n"
            f"⚖️ *Investment:* {analysis_report.investment_ratio}\n"
            f"{warnings}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🔥 *RECOMMENDED MOVES:*{moves_text}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"_Tip: Tap any text above to copy and send._"
        )

telegram_bot = TelegramBotWingman()
