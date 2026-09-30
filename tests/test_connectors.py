import pytest
from httpx import AsyncClient, ASGITransport
from rizz_coach.server import app
from rizz_coach.storage.db import db
from rizz_coach.connectors.tinder import TinderConnector, tinder_connector
from rizz_coach.connectors.instagram import InstagramConnector, instagram_connector
from rizz_coach.connectors.manager import OutreachManager, outreach_manager
from rizz_coach.adapters.telegram_bot import telegram_bot

@pytest.fixture(autouse=True)
def clean_outreach_db():
    with db._get_connection() as conn:
        conn.execute("DELETE FROM outreach_queue")
        conn.commit()
    yield
    with db._get_connection() as conn:
        conn.execute("DELETE FROM outreach_queue")
        conn.commit()

@pytest.mark.asyncio
async def test_tinder_connector_fetch_and_send():
    connector = TinderConnector()
    matches = await connector.fetch_new_matches()
    assert len(matches) > 0
    assert "match_id" in matches[0]
    assert "name" in matches[0]
    assert "bio" in matches[0]

    sent = await connector.send_message(matches[0]["match_id"], "Hey, playful opener test.")
    assert sent is True

@pytest.mark.asyncio
async def test_instagram_connector():
    connector = InstagramConnector()
    matches = await connector.fetch_new_matches()
    assert len(matches) > 0
    sent = await connector.send_message(matches[0]["match_id"], "Hey Sarah, love your work.")
    assert sent is True

@pytest.mark.asyncio
async def test_outreach_manager_sync_and_approval():
    manager = OutreachManager()
    
    # 1. Sync matches
    result = await manager.sync_platform_matches(platform="tinder")
    assert result["status"] == "success"
    assert result["queued_count"] > 0
    
    item = result["queued_items"][0]
    item_id = item["id"]
    
    # Verify in DB
    pending = db.get_pending_outreach()
    assert any(p["id"] == item_id for p in pending)
    
    # 2. Approve with instant dispatch
    approved = await manager.approve_and_dispatch(item_id, instant=True)
    assert approved["status"] == "sent"
    
    # Verify DB status updated
    updated_item = db.get_outreach_item(item_id)
    assert updated_item["status"] in ["APPROVED", "SENT"]

@pytest.mark.asyncio
async def test_outreach_reject():
    manager = OutreachManager()
    item = db.create_outreach_item(
        item_id="test_reject_1",
        platform="tinder",
        match_id="mock_test_1",
        match_name="TestName",
        match_bio="Test bio",
        proposed_text="Test opener"
    )
    
    rej = await manager.reject_outreach(item["id"])
    assert rej["status"] == "rejected"
    
    item_check = db.get_outreach_item("test_reject_1")
    assert item_check["status"] == "REJECTED"

@pytest.mark.asyncio
async def test_outreach_api_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Sync
        sync_resp = await client.post("/api/outreach/sync", json={"platform": "tinder"})
        assert sync_resp.status_code == 200
        sync_data = sync_resp.json()
        assert sync_data["status"] == "success"
        
        # 2. Pending list
        pending_resp = await client.get("/api/outreach/pending")
        assert pending_resp.status_code == 200
        pending_data = pending_resp.json()
        assert isinstance(pending_data, list)
        assert len(pending_data) > 0
        
        item_to_approve = pending_data[0]["id"]
        
        # 3. Approve
        approve_resp = await client.post("/api/outreach/approve", json={
            "item_id": item_to_approve,
            "instant": True
        })
        assert approve_resp.status_code == 200
        assert approve_resp.json()["status"] == "sent"

@pytest.mark.asyncio
async def test_telegram_webhook_callback_buttons():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create a sample queue item
        item = db.create_outreach_item(
            item_id="tg_test_123",
            platform="tinder",
            match_id="mock_tg_1",
            match_name="Elena",
            match_bio="NYC consultant",
            proposed_text="Careful, keep talking like that and I might believe you."
        )
        
        # Simulate Telegram sending a callback query when user clicks [⚡ Send Now]
        payload = {
            "callback_query": {
                "id": "cb_query_999",
                "from": {"id": 123456, "first_name": "Luis"},
                "message": {
                    "message_id": 100,
                    "chat": {"id": 123456}
                },
                "data": "send_now:tg_test_123"
            }
        }
        
        resp = await client.post("/webhooks/telegram", json=payload)
        assert resp.status_code == 200
        assert resp.json()["status"] == "callback_processed"
        
        # Verify item status changed
        updated = db.get_outreach_item("tg_test_123")
        assert updated["status"] in ["APPROVED", "SENT"]

@pytest.mark.asyncio
async def test_imessage_connector_methods():
    from rizz_coach.connectors.imessage import imessage_connector
    
    # 1. Matches/recent threads
    matches = await imessage_connector.fetch_new_matches()
    assert isinstance(matches, list)
    assert len(matches) > 0
    assert "name" in matches[0]
    assert "last_message" in matches[0]

    # 2. Fetch history
    history = await imessage_connector.fetch_chat_history(matches[0]["match_id"])
    assert isinstance(history, str)
    assert len(history) > 0

    # 3. Send message
    ok = await imessage_connector.send_message(matches[0]["match_id"], "Test reply from RizzCoach")
    assert ok is True

@pytest.mark.asyncio
async def test_mobile_quick_coach_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Quick Coach endpoint for iOS Action Button / Shortcuts
        resp = await client.post("/api/mobile/quick-coach", json={
            "text": "haha maybe, depends on if you're trouble",
            "target_name": "Sophie",
            "channel": "imessage"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert "best_move" in data
        assert "clipboard_text" in data
        assert len(data["moves"]) > 0
        assert "ios_hud" in data
        assert "trouble" in data["ios_hud"].lower() or "best move" in data["ios_hud"].lower()

        # 2. iOS Shortcut guide
        guide_resp = await client.get("/api/mobile/shortcut/guide")
        assert guide_resp.status_code == 200
        assert "setup_steps" in guide_resp.json()

        # 3. iMessage recent threads
        recent_resp = await client.get("/api/mobile/imessage/recent")
        assert recent_resp.status_code == 200
        assert "threads" in recent_resp.json()

        # 4. iMessage send
        send_resp = await client.post("/api/mobile/imessage/send", json={
            "recipient": "+13105550199",
            "text": "Sounds good, see you at 8."
        })
        assert send_resp.status_code == 200
        assert send_resp.json()["status"] == "sent"

        # 5. iMessage tactical reply generator
        reply_resp = await client.post("/api/mobile/imessage/tactical-reply", json={
            "recipient": "+13105550199",
            "context_text": "Her: what are you doing tonight?\nMe: debating if I want to be productive or reckless.",
            "auto_send": False
        })
        assert reply_resp.status_code == 200
        reply_data = reply_resp.json()
        assert "best_move" in reply_data
        assert reply_data["dispatched"] is False

@pytest.mark.asyncio
async def test_telegram_mobile_commands():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test /score command
        score_payload = {
            "message": {
                "message_id": 201,
                "chat": {"id": 998877},
                "text": "/score You are the most beautiful goddess in the world please reply"
            }
        }
        score_resp = await client.post("/webhooks/telegram", json=score_payload)
        assert score_resp.status_code == 200
        assert score_resp.json()["status"] == "scored"

        # Test /sync command
        sync_payload = {
            "message": {
                "message_id": 202,
                "chat": {"id": 998877},
                "text": "/sync"
            }
        }
        sync_resp = await client.post("/webhooks/telegram", json=sync_payload)
        assert sync_resp.status_code == 200
        assert sync_resp.json()["status"] == "synced"

        # Test /imessage command
        imessage_payload = {
            "message": {
                "message_id": 203,
                "chat": {"id": 998877},
                "text": "/imessage recent"
            }
        }
        imsg_resp = await client.post("/webhooks/telegram", json=imessage_payload)
        assert imsg_resp.status_code == 200
        assert imsg_resp.json()["status"] == "imessage_recent"
