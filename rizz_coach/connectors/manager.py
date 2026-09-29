import uuid
import asyncio
from typing import List, Dict, Any, Optional
from rizz_coach.config import settings
from rizz_coach.storage.db import db
from rizz_coach.core.analyzer import ConversationAnalyzer
from rizz_coach.core.automation import automation_engine
from rizz_coach.adapters.telegram_bot import telegram_bot
from rizz_coach.connectors.tinder import tinder_connector
from rizz_coach.connectors.instagram import instagram_connector

class OutreachManager:
    """
    Orchestrates automated match detection, AI opening strategy generation,
    approval queueing (Telegram/Web), human pacing, and message dispatch.
    """

    def __init__(self):
        self.connectors = {
            "tinder": tinder_connector,
            "instagram": instagram_connector
        }
        self.analyzer = ConversationAnalyzer()

    async def sync_platform_matches(self, platform: str = "tinder") -> Dict[str, Any]:
        """
        Polls a platform for new matches, runs AI analysis on their bio/context,
        and adds them to the outreach approval queue.
        """
        connector = self.connectors.get(platform, tinder_connector)
        
        # Enforce safety daily outreach cap to prevent account bans
        daily_count = db.get_daily_outreach_count(platform)
        if daily_count >= settings.max_daily_outreach:
            return {
                "status": "rate_limited",
                "message": f"Daily outreach cap ({settings.max_daily_outreach}) reached for {platform}. Pausing to protect account safety.",
                "queued_count": 0
            }

        matches = await connector.fetch_new_matches()
        queued_items = []

        for match in matches:
            match_id = match["match_id"]
            name = match.get("name", "Match")
            bio = match.get("bio", "")

            # Generate personalized opening text using proven methodologies
            prompt_context = f"Her Name: {name}\nHer Bio: {bio}\nHer Photos/Interests: {match.get('photos', [])[:2]}"
            report = await self.analyzer.analyze(
                chat_history=f"New Match Profile Context:\n{prompt_context}",
                target_name=name
            )

            # Pick the top tactical move
            best_move = report.tactical_moves[0].text if report.tactical_moves else f"Hey {name}, your profile looks like trouble in the best way."
            
            # Calculate human jitter delay (e.g. 180-600s)
            delay = automation_engine.calculate_human_delay()
            item_id = f"outreach_{uuid.uuid4().hex[:8]}"

            # Save to SQLite approval queue
            item = db.create_outreach_item(
                item_id=item_id,
                platform=platform,
                match_id=match_id,
                match_name=name,
                match_bio=bio,
                proposed_text=best_move,
                delay_seconds=delay
            )
            queued_items.append(item)

            # Send Telegram Approval notification with inline buttons if configured
            if settings.telegram_chat_id:
                try:
                    await telegram_bot.send_approval_request(
                        chat_id=settings.telegram_chat_id,
                        item_id=item_id,
                        platform=platform,
                        match_name=name,
                        match_bio=bio,
                        proposed_text=best_move,
                        delay_seconds=delay
                    )
                except Exception as e:
                    print(f"[OutreachManager Telegram Warning] Failed to send alert: {e}")

        return {
            "status": "success",
            "platform": platform,
            "queued_count": len(queued_items),
            "queued_items": queued_items
        }

    async def approve_and_dispatch(self, item_id: str, instant: bool = False, edited_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Approves a queued outreach message and dispatches it through the platform connector.
        """
        item = db.get_outreach_item(item_id)
        if not item:
            return {"status": "error", "message": f"Item {item_id} not found."}

        text_to_send = edited_text or item["proposed_text"]
        platform = item["platform"]
        match_id = item["match_id"]
        delay = 0 if instant else item.get("scheduled_delay_seconds", 0)

        # Mark as approved in DB
        db.update_outreach_status(item_id, status="APPROVED", edited_text=text_to_send)

        connector = self.connectors.get(platform, tinder_connector)

        async def _dispatch_task():
            if delay > 0:
                print(f"[Pacing Guardrail] Waiting human jitter delay ({delay}s) before sending to {match_id} on {platform}...")
                await asyncio.sleep(delay)
            
            success = await connector.send_message(match_id, text_to_send)
            if success:
                db.update_outreach_status(item_id, status="SENT")
                # Log to conversation thread
                db.upsert_thread(
                    thread_id=f"{platform}_{match_id}",
                    platform=platform,
                    target_name=item["match_name"],
                    status="ACTIVE"
                )
                db.log_message(
                    thread_id=f"{platform}_{match_id}",
                    sender="User",
                    text=text_to_send
                )
                print(f"[OutreachManager] Successfully dispatched text to {item['match_name']} on {platform}.")

        if instant or delay == 0:
            await _dispatch_task()
            return {"status": "sent", "item_id": item_id, "text": text_to_send, "delay": 0}
        else:
            # Run delay asynchronously in background
            asyncio.create_task(_dispatch_task())
            return {"status": "scheduled", "item_id": item_id, "text": text_to_send, "scheduled_delay": delay}

    async def reject_outreach(self, item_id: str) -> Dict[str, Any]:
        """Rejects/skips an outreach item."""
        updated = db.update_outreach_status(item_id, status="REJECTED")
        return {"status": "rejected" if updated else "not_found", "item_id": item_id}

outreach_manager = OutreachManager()
