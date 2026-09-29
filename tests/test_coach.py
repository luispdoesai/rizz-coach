import pytest
from rizz_coach.core.analyzer import ConversationAnalyzer
from rizz_coach.core.scorer import RizzScorer
from rizz_coach.core.autopsy import ChatAutopsy
from rizz_coach.core.gym import RizzGym
from rizz_coach.core.profile import ProfileAuditor
from rizz_coach.core.automation import automation_engine

@pytest.mark.asyncio
async def test_analyzer_returns_tactical_moves():
    analyzer = ConversationAnalyzer()
    sample_chat = "Her: haha nice, what are you up to this weekend?\nMe: just hanging out, u?"
    report = await analyzer.analyze(sample_chat, target_name="Chloe")

    assert report.interest_score >= 0 and report.interest_score <= 100
    assert len(report.tactical_moves) >= 1
    assert report.subtext_translation != ""
    assert report.frame_holder != ""

@pytest.mark.asyncio
async def test_scorer_catches_cringe_anti_patterns():
    scorer = RizzScorer()
    needy_draft = "You are the most beautiful goddess I have ever laid eyes on in my entire life please reply to me."
    context = "Her: haha cool"
    
    scorecard = await scorer.score_message(needy_draft, context)
    assert scorecard.is_cringe is True
    assert len(scorecard.cringe_flags) > 0
    assert any("pedestalizing" in f.lower() for f in scorecard.cringe_flags)

def test_automation_engine_detects_number_and_date():
    # Test phone number extraction
    text_with_phone = "Sounds like a plan! Text me at 415-555-0142"
    status, contact = automation_engine.evaluate_inbound_outcome(text_with_phone)
    assert status == "CONVERTED_NUMBER"
    assert "415-555-0142" in contact

    decision = automation_engine.process_message(text_with_phone)
    assert decision.action == "HANDOFF_TO_USER"
    assert decision.outcome_status == "CONVERTED_NUMBER"

    # Test date agreement
    text_with_date = "Thursday works for drinks, let's do it!"
    status_date, _ = automation_engine.evaluate_inbound_outcome(text_with_date)
    assert status_date == "CONVERTED_DATE"

    # Test rejection
    text_with_rejection = "Please stop texting me, not interested."
    status_rej, _ = automation_engine.evaluate_inbound_outcome(text_with_rejection)
    assert status_rej == "FAILED_REJECTED"

@pytest.mark.asyncio
async def test_autopsy_and_revival_texts():
    autopsy = ChatAutopsy()
    dead_chat = "Me: hey\nHer: hey\nMe: how are you\nHer: good\nMe: cool what did you eat\n[Ghosted]"
    report = await autopsy.diagnose(dead_chat)
    
    assert report.status != ""
    assert report.fatal_turn != ""
    assert len(report.revival_texts) >= 1

@pytest.mark.asyncio
async def test_gym_sparring_turn():
    gym = RizzGym()
    response = await gym.step(
        archetype_id="chloe",
        user_message="I wear Patagonia vests and buy vinyl. Peak identity crisis.",
        history=[]
    )
    assert response.character_name != ""
    assert response.character_reply != ""
    assert response.coach_feedback.turn_rizz_score > 0
    assert response.coach_feedback.coaching_tip != ""

@pytest.mark.asyncio
async def test_profile_auditor():
    auditor = ProfileAuditor()
    report = await auditor.audit(
        bio="6'0. Love gym, tacos, traveling, and my dog. Fluent in sarcasm.",
        photo_descriptions="Gym selfie in bathroom mirror, sunglasses on boat"
    )
    assert report.overall_score > 0
    assert len(report.improved_bios) >= 1
    assert len(report.photo_audit) >= 1

def test_markdown_prompts_loaded():
    from rizz_coach.prompts import load_prompt
    analyzer_p = load_prompt("analyzer.md")
    assert "Mark Manson" in analyzer_p
    assert "Logan Ury" in analyzer_p
    assert "Matthew Hussey" in analyzer_p

    scorer_p = load_prompt("scorer.md")
    assert "interview_mode" in scorer_p

    profile_p = load_prompt("profile.md")
    assert "Blaine Anderson" in profile_p

