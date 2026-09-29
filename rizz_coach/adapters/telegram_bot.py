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

    async def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown", reply_markup: Optional[Dict[str, Any]] = None) -> bool:
        if not self.api_url:
            print(f"[Telegram Mock] Sent to {chat_id}:\n{text}")
            if reply_markup:
                print(f"[Telegram Mock Buttons] {reply_markup}")
            return True

        url = f"{self.api_url}/sendMessage"
        payload: Dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            return resp.status_code == 200

    async def answer_callback_query(self, callback_query_id: str, text: str) -> bool:
        if not self.api_url:
            print(f"[Telegram Mock] Callback Answer: {text}")
            return True

        url = f"{self.api_url}/answerCallbackQuery"
        payload = {
            "callback_query_id": callback_query_id,
            "text": text
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            return resp.status_code == 200

    async def send_approval_request(
        self,
        chat_id: str,
        item_id: str,
        platform: str,
        match_name: str,
        match_bio: str,
        proposed_text: str,
        delay_seconds: int = 180
    ) -> bool:
        """Sends an interactive Telegram card with inline approval buttons."""
        mins = delay_seconds // 60
        secs = delay_seconds % 60
        delay_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"

        text = (
            f"🔥 *OUTREACH APPROVAL NEEDED* ({platform.upper()})\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"👤 *Match:* {match_name}\n"
            f"📝 *Bio:* {match_bio or 'No bio provided'}\n\n"
            f"🎯 *Proposed Opener:*\n"
            f"`{proposed_text}`\n\n"
            f"⏱️ *Scheduled Delay:* {delay_str} (Human Anti-Detection Jitter)\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"_Select an action below to proceed:_"
        )

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "✅ Approve & Schedule", "callback_data": f"approve:{item_id}"},
                    {"text": "⚡ Send Now", "callback_data": f"send_now:{item_id}"}
                ],
                [
                    {"text": "❌ Skip / Reject", "callback_data": f"reject:{item_id}"}
                ]
            ]
        }

        return await self.send_message(chat_id, text, reply_markup=reply_markup)

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

