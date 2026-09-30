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
from rizz_coach.connectors.imessage import imessage_connector

app = FastAPI(
    title="RizzCoach",
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

class QuickCoachRequest(BaseModel):
    text: str
    target_name: Optional[str] = "Match"
    channel: Optional[str] = "mobile"

class IMessageSendRequest(BaseModel):
    recipient: str
    text: str

class IMessageReplyRequest(BaseModel):
    recipient: str
    context_text: Optional[str] = None
    auto_send: Optional[bool] = False


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

# ----------------- Mobile & Phone First Endpoints -----------------
@app.post("/api/mobile/quick-coach")
async def api_mobile_quick_coach(req: QuickCoachRequest):
    """
    High-speed mobile endpoint designed for iPhone Action Button, iOS Shortcuts,
    and Share Sheet. Returns the top tactical move formatted for instant clipboard copying.
    """
    report = await analyzer.analyze(req.text, req.target_name)
    best_move = report.tactical_moves[0].text if report.tactical_moves else "Haha fair enough, you got me."
    
    # Format iOS notification banner HUD string
    ios_hud = f"🎯 Best Move: \"{best_move}\"\n🧐 Subtext: {report.subtext_translation} ({report.interest_score}% interest)"
    
    return {
        "status": "success",
        "best_move": best_move,
        "subtext": report.subtext_translation,
        "interest_score": report.interest_score,
        "interest_level": report.interest_level,
        "moves": [m.model_dump() if hasattr(m, "model_dump") else m.dict() for m in report.tactical_moves],
        "cringe_warnings": report.cringe_warnings,
        "ios_hud": ios_hud,
        "clipboard_text": best_move
    }

@app.get("/api/mobile/shortcut/guide")
async def api_mobile_shortcut_guide():
    """Returns iOS Shortcuts / Action Button setup guide for 1-tap iPhone usage."""
    return {
        "name": "RizzCoach Wingman Action",
        "trigger": "iPhone 15/16 Action Button, Back Tap, or Share Sheet",
        "method": "POST",
        "endpoint": "/api/mobile/quick-coach",
        "setup_steps": [
            "1. Open the Apple 'Shortcuts' app on your iPhone.",
            "2. Create a new shortcut named 'RizzCoach'.",
            "3. Add Action: 'Get Clipboard' (or Shortcut Input from Share Sheet).",
            "4. Add Action: 'Get Contents of URL' -> Method: POST, URL: http://<mac-ip>:8000/api/mobile/quick-coach, Request Body: JSON with key 'text' = Clipboard.",
            "5. Add Action: 'Get Dictionary Value' -> key 'clipboard_text'.",
            "6. Add Action: 'Copy to Clipboard' (sets top tactical reply ready to paste).",
            "7. Add Action: 'Show Notification' -> Text: result['ios_hud']."
        ]
    }

@app.get("/api/mobile/imessage/recent")
async def api_mobile_imessage_recent():
    """Returns recent incoming iMessage threads on the host Mac."""
    matches = await imessage_connector.fetch_new_matches()
    return {"threads": matches, "is_macos": imessage_connector.is_macos}

@app.post("/api/mobile/imessage/send")
async def api_mobile_imessage_send(req: IMessageSendRequest):
    """Sends an iMessage through AppleScript on the host Mac."""
    success = await imessage_connector.send_message(req.recipient, req.text)
    return {"status": "sent" if success else "failed", "recipient": req.recipient, "text": req.text}

@app.post("/api/mobile/imessage/tactical-reply")
async def api_mobile_imessage_tactical_reply(req: IMessageReplyRequest):
    """Reads conversation context, generates the best tactical move, and optionally dispatches it."""
    chat_context = req.context_text
    if not chat_context:
        chat_context = await imessage_connector.fetch_chat_history(req.recipient)
    report = await analyzer.analyze(chat_context, req.recipient)
    best_move = report.tactical_moves[0].text if report.tactical_moves else "Haha fair enough."
    
    dispatched = False
    if req.auto_send:
        dispatched = await imessage_connector.send_message(req.recipient, best_move)
        
    return {
        "recipient": req.recipient,
        "best_move": best_move,
        "subtext": report.subtext_translation,
        "moves": [m.model_dump() if hasattr(m, "model_dump") else m.dict() for m in report.tactical_moves],
        "dispatched": dispatched
    }

# ----------------- Webhooks -----------------
@app.post("/webhooks/telegram")
async def telegram_webhook(req: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Unified Telegram Webhook handler for inline approvals, coaching queries, and match syncs.
    """
    return await telegram_bot.handle_update(req)


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
