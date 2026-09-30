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

    async def handle_update(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes an incoming Telegram webhook or polling update.
        Handles text messages, inline buttons, and command shortcuts.
        """
        # 1. Handle Inline Button Clicks (Approve / Send Now / Reject)
        if "callback_query" in update:
            cb = update["callback_query"]
            cb_id = cb["id"]
            data = cb.get("data", "")
            chat_id = str(cb.get("message", {}).get("chat", {}).get("id", ""))

            from rizz_coach.connectors.manager import outreach_manager

            if data.startswith("approve:"):
                item_id = data.split("approve:")[1]
                res = await outreach_manager.approve_and_dispatch(item_id, instant=False)
                await self.answer_callback_query(cb_id, f"✅ Approved! Scheduled with delay ({res.get('scheduled_delay', 0)}s)")
                await self.send_message(chat_id, "✅ *Opener approved & scheduled with anti-detection pacing delay.*")
            elif data.startswith("send_now:"):
                item_id = data.split("send_now:")[1]
                res = await outreach_manager.approve_and_dispatch(item_id, instant=True)
                await self.answer_callback_query(cb_id, "⚡ Dispatched immediately!")
                await self.send_message(chat_id, "⚡ *Opener dispatched immediately to match.*")
            elif data.startswith("reject:"):
                item_id = data.split("reject:")[1]
                await outreach_manager.reject_outreach(item_id)
                await self.answer_callback_query(cb_id, "❌ Match skipped.")
                await self.send_message(chat_id, "❌ *Match opener skipped.*")

            return {"status": "callback_processed"}

        # 2. Handle Text Messages
        if "message" in update:
            msg = update["message"]
            chat_id = str(msg.get("chat", {}).get("id", ""))
            text = (msg.get("text") or msg.get("caption") or "").strip()

            if not text:
                if "photo" in msg:
                    await self.send_message(
                        chat_id,
                        "📸 *Screenshot received!*\nType her last text message below (e.g. _\"Her: what are you up to tonight?\"_) to decode her subtext and get 3 tap-to-copy tactical moves."
                    )
                    return {"status": "photo_prompt_sent"}
                return {"status": "ignored"}

            if text.startswith("/start") or text.startswith("/help"):
                help_text = (
                    "🔥 *RIZZCOACH MOBILE WINGMAN*\n"
                    "━━━━━━━━━━━━━━━━━━━\n"
                    "Your personal pocket dating coach.\n\n"
                    "📱 *How to use from your phone:*\n"
                    "• *Forward or paste any text* from Tinder, Hinge, or iMessage → get instant subtext decoding and 3 tap-to-copy moves.\n"
                    "• `/score <draft>` → test what you're about to send before you send it.\n"
                    "• `/sync` → scan Tinder / Instagram for new matches and approve openers.\n"
                    "• `/autopsy <chat>` → diagnose why a conversation died and get revival moves.\n"
                )
                await self.send_message(chat_id, help_text)
                return {"status": "help_sent"}

            if text.startswith("/score"):
                draft = text.replace("/score", "").strip()
                if not draft:
                    await self.send_message(chat_id, "Type `/score <your draft text>` to test a move.")
                    return {"status": "score_prompt"}
                from rizz_coach.core.scorer import RizzScorer
                scorer = RizzScorer()
                res = await scorer.score_draft(draft_message=draft)
                flags = "\n".join([f"⚠️ {f}" for f in res.cringe_flags]) if res.cringe_flags else "✅ Zero cringe flags detected."
                rewrite = f"\n\n✨ *Coach Rewrite:* `{res.suggested_rewrite}`" if res.suggested_rewrite else ""
                reply = (
                    f"🎯 *DRAFT RATING: {res.score}/100 ({res.letter_grade})*\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"⚖️ *Pacing:* {res.pacing_rating}\n"
                    f"🔬 *Assessment:* {res.why_it_scored}\n"
                    f"{flags}{rewrite}"
                )
                await self.send_message(chat_id, reply)
                return {"status": "scored"}

            if text.startswith("/sync"):
                platform = "tinder"
                if "insta" in text.lower():
                    platform = "instagram"
                elif "imessage" in text.lower():
                    platform = "imessage"
                from rizz_coach.connectors.manager import outreach_manager
                await self.send_message(chat_id, f"🔄 Scanning {platform.upper()} for new matches/threads...")
                res = await outreach_manager.sync_platform_matches(platform)
                await self.send_message(chat_id, f"Found & queued {res.get('queued_count', 0)} items for {platform.upper()}!")
                return {"status": "synced"}

            if text.startswith("/pending"):
                from rizz_coach.storage.db import db
                pending = db.get_pending_outreach()
                if not pending:
                    await self.send_message(chat_id, "✨ No pending outreach items in queue right now.")
                    return {"status": "no_pending"}
                await self.send_message(chat_id, f"📋 Found {len(pending)} pending outreach approval(s):")
                for item in pending:
                    await self.send_approval_request(
                        chat_id=chat_id,
                        item_id=item["item_id"],
                        platform=item["platform"],
                        match_name=item["match_name"],
                        match_bio=item["match_bio"],
                        proposed_text=item["proposed_text"],
                        delay_seconds=item.get("scheduled_delay_seconds", 180)
                    )
                return {"status": "pending_sent"}

            if text.startswith("/imessage"):
                cmd_parts = text.replace("/imessage", "").strip().split(" ", 2)
                subcmd = cmd_parts[0].lower() if cmd_parts and cmd_parts[0] else "recent"
                from rizz_coach.connectors.imessage import imessage_connector

                if subcmd == "recent" or not subcmd:
                    matches = await imessage_connector.fetch_new_matches()
                    lines = ["💬 *RECENT iMESSAGE CONVERSATIONS:*"]
                    for m in matches:
                        lines.append(f"• *{m['name']}*: \"_{m.get('last_message', '')}_\"")
                    lines.append("\n_To reply via iMessage:_ `/imessage send <contact> <text>`")
                    await self.send_message(chat_id, "\n".join(lines))
                    return {"status": "imessage_recent"}

                elif subcmd == "send" and len(cmd_parts) >= 3:
                    recipient = cmd_parts[1]
                    send_text = cmd_parts[2]
                    ok = await imessage_connector.send_message(recipient, send_text)
                    if ok:
                        await self.send_message(chat_id, f"✅ iMessage dispatched to `{recipient}`: \"{send_text}\"")
                    else:
                        await self.send_message(chat_id, f"❌ Failed to dispatch iMessage to `{recipient}`.")
                    return {"status": "imessage_sent"}

            # Default: Analyze conversation
            from rizz_coach.core.analyzer import ConversationAnalyzer
            analyzer = ConversationAnalyzer()
            report = await analyzer.analyze(chat_history=text)
            card = self.format_coaching_card(report)
            await self.send_message(chat_id, card)
            return {"status": "analyzed"}

        return {"status": "ignored"}

telegram_bot = TelegramBotWingman()

