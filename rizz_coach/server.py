from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os

from rizz_coach.config import settings
from rizz_coach.core.analyzer import ConversationAnalyzer
from rizz_coach.core.scorer import RizzScorer
from rizz_coach.core.autopsy import ChatAutopsy
from rizz_coach.core.gym import RizzGym
from rizz_coach.core.profile import ProfileAuditor
from rizz_coach.core.automation import automation_engine
from rizz_coach.storage.db import db
from rizz_coach.adapters.sms_twilio import twilio_adapter
from rizz_coach.adapters.telegram_bot import telegram_bot
from rizz_coach.connectors import outreach_manager, tinder_connector, instagram_connector

app = FastAPI(
    title="OpenWingman / RizzCoach",
    description="Open-Source AI Dating Coach, Text Game Analyzer, Profile Auditor, and Sparring Gym",
    version="0.1.0"
)

# Static and template mounts
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "web", "static")
templates_dir = os.path.join(current_dir, "web", "templates")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory=templates_dir)

# Initialize core instances
analyzer = ConversationAnalyzer()
scorer = RizzScorer()
autopsy = ChatAutopsy()
gym = RizzGym()
profile_auditor = ProfileAuditor()

# ----------------- UI Route -----------------
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    stats = db.get_funnel_stats()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "stats": stats,
            "provider": settings.llm_provider,
            "model": settings.llm_model,
            "automation_mode": settings.automation_mode
        }
    )

# ----------------- API Request Schemas -----------------
class AnalyzeRequest(BaseModel):
    chat_history: str
    target_name: Optional[str] = "Match"

class ScoreRequest(BaseModel):
    draft_message: str
    context_message: Optional[str] = ""

class AutopsyRequest(BaseModel):
    chat_history: str

class GymTurnRequest(BaseModel):
    archetype_id: str
    user_message: str
    history: List[Dict[str, str]] = []

class ProfileAuditRequest(BaseModel):
    bio: str
    prompts_text: Optional[str] = ""
    photo_descriptions: Optional[str] = ""

class AutomationProcessRequest(BaseModel):
    incoming_text: str
    channel: Optional[str] = "sms"
    thread_id: Optional[str] = "demo_thread"
    sender_name: Optional[str] = "Match"

class OutreachSyncRequest(BaseModel):
    platform: Optional[str] = "tinder"

class OutreachApproveRequest(BaseModel):
    item_id: str
    instant: Optional[bool] = False
    edited_text: Optional[str] = None

class OutreachRejectRequest(BaseModel):
    item_id: str


# ----------------- Core Coach Endpoints -----------------
@app.post("/api/analyze")
async def api_analyze(req: AnalyzeRequest):
    report = await analyzer.analyze(req.chat_history, req.target_name)
    # Log turn to db
    db.upsert_thread(
        thread_id=f"chat_{req.target_name.lower()}",
        platform="web_copilot",
        target_name=req.target_name,
        status="ACTIVE"
    )
    return report

@app.post("/api/score")
async def api_score(req: ScoreRequest):
    scorecard = await scorer.score_message(req.draft_message, req.context_message)
    return scorecard

@app.post("/api/autopsy")
async def api_autopsy(req: AutopsyRequest):
    report = await autopsy.diagnose(req.chat_history)
    return report

@app.get("/api/gym/archetypes")
async def api_gym_archetypes():
    return gym.get_archetypes()

@app.post("/api/gym/turn")
async def api_gym_turn(req: GymTurnRequest):
    response = await gym.step(req.archetype_id, req.user_message, req.history)
    return response

@app.post("/api/profile/audit")
async def api_profile_audit(req: ProfileAuditRequest):
    report = await profile_auditor.audit(req.bio, req.photo_descriptions, req.prompts_text)
    return report

@app.get("/api/stats")
async def api_stats():
    return db.get_funnel_stats()

# ----------------- Automation Endpoint -----------------
@app.post("/api/automation/process")
async def api_automation_process(req: AutomationProcessRequest):
    decision = automation_engine.process_message(req.incoming_text)
    db.upsert_thread(
        thread_id=req.thread_id,
        platform=req.channel,
        target_name=req.sender_name,
        status=decision.outcome_status,
        contact=decision.contact_extracted
    )
    db.log_message(
        thread_id=req.thread_id,
        sender=req.sender_name,
        text=req.incoming_text
    )
    return decision

# ----------------- Outreach & Platform Connector Endpoints -----------------
@app.get("/api/outreach/pending")
async def api_outreach_pending():
    """Returns list of pending outreach approvals from the queue."""
    return db.get_pending_outreach()

@app.post("/api/outreach/sync")
async def api_outreach_sync(req: OutreachSyncRequest):
    """Syncs new matches from Tinder/Instagram, creates AI openers, and adds them to approval queue."""
    return await outreach_manager.sync_platform_matches(req.platform or "tinder")

@app.post("/api/outreach/approve")
async def api_outreach_approve(req: OutreachApproveRequest):
    """Approves a queued outreach message (triggers human jitter delay or instant send)."""
    return await outreach_manager.approve_and_dispatch(req.item_id, req.instant or False, req.edited_text)

@app.post("/api/outreach/reject")
async def api_outreach_reject(req: OutreachRejectRequest):
    """Rejects or skips a queued outreach message."""
    return await outreach_manager.reject_outreach(req.item_id)

# ----------------- Webhooks -----------------
@app.post("/webhooks/telegram")
async def telegram_webhook(req: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Telegram Webhook handler.
    1. Interactive Inline Button Clicks: Approve, Send Now, or Skip.
    2. Forwarded Messages / Screenshots: Returns instant Wingman analysis card.
    """
    # 1. Inline button callback query
    if "callback_query" in req:
        cb = req["callback_query"]
        cb_id = cb.get("id")
        data = cb.get("data", "")
        chat_id = str(cb.get("message", {}).get("chat", {}).get("id", ""))

        parts = data.split(":", 1)
        action = parts[0]
        item_id = parts[1] if len(parts) > 1 else ""

        if action == "approve":
            background_tasks.add_task(outreach_manager.approve_and_dispatch, item_id, False)
            await telegram_bot.answer_callback_query(cb_id, "✅ Approved! Scheduled with human pacing delay.")
            await telegram_bot.send_message(chat_id, "✅ *Approved!* Message queued and scheduled with human jitter delay.")
        elif action == "send_now":
            background_tasks.add_task(outreach_manager.approve_and_dispatch, item_id, True)
            await telegram_bot.answer_callback_query(cb_id, "⚡ Dispatched immediately!")
            await telegram_bot.send_message(chat_id, "⚡ *Dispatched!* Message sent immediately to match.")
        elif action == "reject":
            background_tasks.add_task(outreach_manager.reject_outreach, item_id)
            await telegram_bot.answer_callback_query(cb_id, "❌ Match outreach skipped.")
            await telegram_bot.send_message(chat_id, "❌ *Skipped.* Match outreach removed from queue.")
        return {"status": "callback_processed"}

    # 2. Regular message received for analysis
    if "message" in req:
        msg = req["message"]
        chat_id = str(msg.get("chat", {}).get("id", ""))
        text = msg.get("text", "")
        if text:
            report = await analyzer.analyze(text)
            card = telegram_bot.format_coaching_card(report)
            await telegram_bot.send_message(chat_id, card)
        return {"status": "message_analyzed"}

    return {"status": "ignored"}

@app.post("/webhooks/twilio")
async def twilio_webhook(request: Request, background_tasks: BackgroundTasks):
    form_data = await request.form()
    event = await twilio_adapter.receive_event(dict(form_data))
    decision = automation_engine.process_message(event["incoming_text"])

    db.upsert_thread(
        thread_id=event["thread_id"],
        platform="twilio_sms",
        status=decision.outcome_status,
        contact=decision.contact_extracted
    )

    if decision.action == "AUTO_REPLY_QUEUED":
        report = await analyzer.analyze(event["incoming_text"])
        best_move = report.tactical_moves[0].text if report.tactical_moves else "Haha fair enough."
        background_tasks.add_task(twilio_adapter.send_message, event["sender_id"], best_move)

    return {"status": "received", "decision": decision.dict()}

@app.post("/webhooks/generic")
async def generic_webhook(req: Dict[str, Any]):
    text = req.get("message", req.get("text", ""))
    report = await analyzer.analyze(text)
    decision = automation_engine.process_message(text)
    return {
        "analysis": report,
        "decision": decision
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("rizz_coach.server:app", host=settings.host, port=settings.port, reload=settings.debug)
