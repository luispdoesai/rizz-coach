// =========================================================
// RizzCoach - Client Interactive Controller
// =========================================================

let currentArchetype = "chloe";
let gymHistory = [];

const SAMPLE_CHATS = {
    chloe: `Chloe: Your profile is so confusing. Are you a finance bro or a closet hipster?
Me: I wear Patagonia vests while buying vinyl records. Peak identity crisis.
Chloe: haha oh god, that's tragic. What's the last record you bought then?`,
    dead_chat: `Me: Hey! How's your week going?
Her: good, super busy with work.
Me: Oh nice what do you do again?
Her: marketing.
Me: That's cool! Do you like it or is it stressful?
[No response - Ghosted for 5 days]`
};

const SAMPLE_BIOS = {
    bio: "6'1. Love hiking, tacos, traveling, gym, and hanging out with my dog. Fluent in sarcasm. Looking for my partner in crime.",
    prompts: "Prompt: The secret to getting along with me...\nAnswer: Don't take life too seriously and feed me pizza.",
    photos: "Photo 1: Gym mirror selfie\nPhoto 2: Sunglasses on a yacht\nPhoto 3: Big group shot where everyone is wearing hats"
};

// Tab Switching
function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));

    const activeBtn = document.getElementById(`tab-${tabId}-btn`);
    const activeContent = document.getElementById(`tab-${tabId}`);

    if (activeBtn) activeBtn.classList.add('active');
    if (activeContent) activeContent.classList.add('active');

    if (tabId === 'automation') {
        loadOutreachQueue();
    }
}

// Toast Helper
function showToast(message) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>🔥</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 200);
    }, 2800);
}

// Copy Text
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast("Copied tactical move to clipboard!");
    }).catch(() => {
        showToast("Copied!");
    });
}

// Load Samples
function loadSampleChat() {
    document.getElementById('chat-history-input').value = SAMPLE_CHATS.chloe;
    document.getElementById('match-name-input').value = "Chloe";
    showToast("Sample conversation loaded!");
}

function loadSampleDeadChat() {
    document.getElementById('autopsy-history-input').value = SAMPLE_CHATS.dead_chat;
    showToast("Dead chat sample loaded!");
}

function loadSampleBio() {
    document.getElementById('profile-bio-input').value = SAMPLE_BIOS.bio;
    document.getElementById('profile-prompts-input').value = SAMPLE_BIOS.prompts;
    document.getElementById('profile-photos-input').value = SAMPLE_BIOS.photos;
    showToast("Sample bio & photos loaded!");
}

// TAB 1: Live Wingman Analysis
async function runAnalysis() {
    const chatHistory = document.getElementById('chat-history-input').value.trim();
    const targetName = document.getElementById('match-name-input').value.trim() || "Match";
    const btn = document.getElementById('btn-run-analysis');

    if (!chatHistory) {
        showToast("Please paste a conversation first.");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = "<span>Analyzing Dynamics...</span>";

    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_history: chatHistory, target_name: targetName })
        });
        const data = await res.json();

        // Render results
        document.getElementById('wingman-empty-state').classList.add('hidden');
        const results = document.getElementById('wingman-results');
        results.classList.remove('hidden');

        document.getElementById('report-interest-score').textContent = data.interest_score;
        document.getElementById('report-interest-level').textContent = data.interest_level;
        document.getElementById('report-subtext').textContent = data.subtext_translation;
        document.getElementById('report-frame').textContent = `Frame: ${data.frame_holder}`;
        document.getElementById('report-investment').textContent = `Investment: ${data.investment_ratio}`;

        // Warnings
        const warningsList = document.getElementById('report-warnings-list');
        warningsList.innerHTML = '';
        (data.cringe_warnings || []).forEach(w => {
            const li = document.createElement('li');
            li.textContent = w;
            warningsList.appendChild(li);
        });

        // Tactical Moves
        const movesList = document.getElementById('report-moves-list');
        movesList.innerHTML = '';

        data.tactical_moves.forEach(move => {
            let catClass = 'cat-banter';
            if (move.category.includes('Escalation')) catClass = 'cat-escalate';
            if (move.category.includes('Reset')) catClass = 'cat-reset';

            const card = document.createElement('div');
            card.className = 'move-card';
            card.innerHTML = `
                <div class="move-header">
                    <span class="move-category ${catClass}">${move.category}</span>
                    <span class="move-rizz-score">Rizz: ${move.rizz_score}/100</span>
                </div>
                <div class="move-text-box">
                    <div class="move-text">${escapeHtml(move.text)}</div>
                    <button class="btn-copy" onclick="copyToClipboard('${escapeJs(move.text)}')">Copy</button>
                </div>
                <div class="move-rationale">💡 ${escapeHtml(move.rationale)}</div>
            `;
            movesList.appendChild(card);
        });

        showToast("Conversation decoded!");
    } catch (err) {
        showToast("Error analyzing conversation.");
        console.error(err);
    } finally {
        btn.disabled = false;
        btn.innerHTML = "<span>🔥 Decode Subtext & Generate Moves</span>";
    }
}

// Quick Draft Scorer
async function testDraft() {
    const draft = document.getElementById('draft-test-input').value.trim();
    const context = document.getElementById('chat-history-input').value.trim();
    const resultBox = document.getElementById('draft-score-result');

    if (!draft) {
        showToast("Type a draft message first.");
        return;
    }

    resultBox.classList.remove('hidden');
    resultBox.innerHTML = "Evaluating draft...";

    try {
        const res = await fetch('/api/score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draft_message: draft, context_message: context })
        });
        const score = await res.json();

        let badgeColor = score.score >= 80 ? '#34d399' : (score.score >= 65 ? '#fbbf24' : '#f87171');
        let flagsHtml = (score.cringe_flags || []).map(f => `<span style="color:#f87171;">⚠️ ${f}</span>`).join('<br>');

        resultBox.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <strong>Rizz Score: <span style="color:${badgeColor}; font-size:16px;">${score.score}/100 (${score.letter_grade})</span></strong>
                <span style="font-size:11px; color:#94a3b8;">Pacing: ${score.pacing_rating}</span>
            </div>
            <p style="margin-bottom:6px; color:#cbd5e1;">${escapeHtml(score.why_it_scored)}</p>
            ${flagsHtml ? `<div style="margin-bottom:8px;">${flagsHtml}</div>` : ''}
            ${score.suggested_rewrite ? `
                <div style="background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.3); border-radius:6px; padding:8px 10px; margin-top:8px;">
                    <div style="font-size:11px; font-weight:700; color:#c4b5fd;">Coach Rewrite (+20 Rizz):</div>
                    <div style="font-size:13px; color:#fff; margin-top:2px;">"${escapeHtml(score.suggested_rewrite)}"</div>
                </div>
            ` : ''}
        `;
    } catch (err) {
        resultBox.innerHTML = "Error evaluating draft.";
    }
}

// TAB 2: The Rizz Gym Simulator
function selectArchetype(archetypeId) {
    currentArchetype = archetypeId;
    document.querySelectorAll('.archetype-card').forEach(c => c.classList.remove('active'));
    event.currentTarget.classList.add('active');

    resetGym();
}

function resetGym() {
    gymHistory = [];
    const chatLog = document.getElementById('gym-chat-log');
    chatLog.innerHTML = '';

    const starters = {
        chloe: { name: "Chloe", opener: "Your profile looks like a curated advertisement for a good boy. Are you actually fun or just well-behaved?" },
        elena: { name: "Elena", opener: "I usually delete this app after 5 minutes. Convince me why I shouldn't." },
        mia: { name: "Mia", opener: "hey" },
        sofia: { name: "Sofia", opener: "If we were skipping town right now, what's our first terrible spontaneous decision?" }
    };

    const starter = starters[currentArchetype] || starters.chloe;
    document.getElementById('active-char-name').textContent = `${starter.name}`;
    
    appendGymMessage(starter.name, starter.opener, 'incoming');
    gymHistory.push({ role: starter.name, content: starter.opener });

    document.getElementById('gym-sideline-text').textContent = "Sparring started! Read her opener, match her tone, and don't qualify yourself.";
    document.getElementById('gym-turn-score').textContent = "Ready";
}

function appendGymMessage(sender, text, type) {
    const chatLog = document.getElementById('gym-chat-log');
    const msg = document.createElement('div');
    msg.className = `chat-msg msg-${type}`;
    msg.innerHTML = `
        <div class="msg-sender">${sender}</div>
        <div class="msg-bubble">${escapeHtml(text)}</div>
    `;
    chatLog.appendChild(msg);
    chatLog.scrollTop = chatLog.scrollHeight;
}

async function sendGymMessage() {
    const input = document.getElementById('gym-user-input');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    appendGymMessage('You', text, 'outgoing');
    gymHistory.push({ role: 'User', content: text });

    const btn = document.getElementById('btn-gym-send');
    btn.disabled = true;

    try {
        const res = await fetch('/api/gym/turn', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                archetype_id: currentArchetype,
                user_message: text,
                history: gymHistory
            })
        });
        const data = await res.json();

        // Append character reply
        appendGymMessage(data.character_name, data.character_reply, 'incoming');
        gymHistory.push({ role: data.character_name, content: data.character_reply });

        // Update sideline feedback
        document.getElementById('gym-turn-score').textContent = `Move Score: ${data.coach_feedback.turn_rizz_score}/100`;
        document.getElementById('gym-sideline-text').innerHTML = `
            <strong>${escapeHtml(data.coach_feedback.what_worked)}</strong><br>
            <span style="color:#c4b5fd;">Coach tip: ${escapeHtml(data.coach_feedback.coaching_tip)}</span>
        `;
    } catch (err) {
        showToast("Error in sparring round.");
    } finally {
        btn.disabled = false;
        input.focus();
    }
}

// TAB 3: Profile Auditor
async function auditProfile() {
    const bio = document.getElementById('profile-bio-input').value.trim();
    const prompts = document.getElementById('profile-prompts-input').value.trim();
    const photos = document.getElementById('profile-photos-input').value.trim();
    const btn = document.getElementById('btn-audit-profile');

    if (!bio) {
        showToast("Please enter a bio to audit.");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = "<span>Auditing Profile...</span>";

    try {
        const res = await fetch('/api/profile/audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bio: bio, prompts_text: prompts, photo_descriptions: photos })
        });
        const data = await res.json();

        document.getElementById('profile-empty-state').classList.add('hidden');
        document.getElementById('profile-results').classList.remove('hidden');

        document.getElementById('profile-overall-score').textContent = data.overall_score;
        document.getElementById('profile-score-badge').textContent = `Score: ${data.overall_score}/100`;
        document.getElementById('profile-bio-critique').textContent = data.bio_critique;

        // Photos
        const photoList = document.getElementById('profile-photo-list');
        photoList.innerHTML = '';
        data.photo_audit.forEach(p => {
            const item = document.createElement('div');
            item.className = 'photo-item';
            item.innerHTML = `
                <div><strong>Photo ${p.photo_num}:</strong> ${escapeHtml(p.verdict)}</div>
                <span class="badge" style="background:rgba(255,255,255,0.06);">${p.score}/100</span>
            `;
            photoList.appendChild(item);
        });

        // Cliches
        const clichesList = document.getElementById('profile-cliches-list');
        clichesList.innerHTML = '';
        data.cliches_detected.forEach(c => {
            const li = document.createElement('li');
            li.textContent = c;
            clichesList.appendChild(li);
        });

        // Bio Rewrites
        const biosList = document.getElementById('profile-bios-list');
        biosList.innerHTML = '';
        data.improved_bios.forEach(b => {
            const card = document.createElement('div');
            card.className = 'bio-card';
            card.innerHTML = `
                <div class="bio-style-tag">${escapeHtml(b.style)}</div>
                <div class="bio-text-content">"${escapeHtml(b.bio)}"</div>
                <button class="btn-copy" onclick="copyToClipboard('${escapeJs(b.bio)}')">Copy Bio</button>
            `;
            biosList.appendChild(card);
        });

        showToast("Profile audit complete!");
    } catch (err) {
        showToast("Error auditing profile.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = "<span>🔍 Audit Profile & Generate 3 High-Value Bios</span>";
    }
}

// TAB 4: Chat Autopsy
async function runAutopsy() {
    const history = document.getElementById('autopsy-history-input').value.trim();
    const btn = document.getElementById('btn-run-autopsy');

    if (!history) {
        showToast("Please paste the dead conversation.");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = "<span>Analyzing Point of Failure...</span>";

    try {
        const res = await fetch('/api/autopsy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_history: history })
        });
        const data = await res.json();

        document.getElementById('autopsy-empty-state').classList.add('hidden');
        document.getElementById('autopsy-results').classList.remove('hidden');

        document.getElementById('autopsy-status-badge').textContent = data.status;
        document.getElementById('autopsy-fatal-turn').textContent = data.fatal_turn;
        document.getElementById('autopsy-root-cause').textContent = data.root_cause;
        document.getElementById('autopsy-recovery-prob').textContent = data.recovery_probability;

        const revivalsList = document.getElementById('autopsy-revival-list');
        revivalsList.innerHTML = '';
        data.revival_texts.forEach(r => {
            const card = document.createElement('div');
            card.className = 'revival-card';
            card.innerHTML = `
                <div class="revival-name">${escapeHtml(r.name)}</div>
                <div class="move-text-box">
                    <div class="move-text">"${escapeHtml(r.text)}"</div>
                    <button class="btn-copy" onclick="copyToClipboard('${escapeJs(r.text)}')">Copy</button>
                </div>
                <div class="move-rationale">💡 ${escapeHtml(r.why_it_works)}</div>
            `;
            revivalsList.appendChild(card);
        });

        showToast("Autopsy complete!");
    } catch (err) {
        showToast("Error running autopsy.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = "<span>🩻 Run Post-Mortem & Get Revival Texts</span>";
    }
}

// TAB 5: Automation Simulator
function setAutoTest(type) {
    const input = document.getElementById('auto-incoming-input');
    if (type === 'number') {
        input.value = "Sounds fun! Here's my number 310-555-0199, text me there.";
    } else if (type === 'date') {
        input.value = "Thursday works for drinks! What time were you thinking?";
    } else if (type === 'ongoing') {
        input.value = "Haha you are so ridiculous. What do you do on weekends?";
    } else if (type === 'rejection') {
        input.value = "Please stop texting me, not interested.";
    }
}

async function runAutomationTest() {
    const input = document.getElementById('auto-incoming-input').value.trim();
    const box = document.getElementById('auto-decision-box');

    try {
        const res = await fetch('/api/automation/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ incoming_text: input })
        });
        const decision = await res.json();

        box.classList.remove('hidden');
        document.getElementById('auto-action-label').textContent = decision.action;
        document.getElementById('auto-status-label').textContent = decision.outcome_status;
        document.getElementById('auto-reason-text').textContent = decision.reason;
        document.getElementById('auto-delay-text').textContent = `Calculated Anti-Detection Delay: ${decision.scheduled_delay_seconds}s`;

        showToast(`Automation event: ${decision.action}`);
    } catch (err) {
        showToast("Error processing automation.");
    }
}

// Helpers
function escapeHtml(text) {
    if (!text) return '';
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function escapeJs(text) {
    if (!text) return '';
    return text.replace(/'/g, "\\'").replace(/"/g, '\\"');
}

// =========================================================
// Outreach & Approval Queue Controller
// =========================================================

async function loadOutreachQueue() {
    const emptyState = document.getElementById('outreach-empty-state');
    const queueList = document.getElementById('outreach-queue-list');
    if (!queueList) return;

    try {
        const res = await fetch('/api/outreach/pending');
        const items = await res.json();

        if (!items || items.length === 0) {
            emptyState.classList.remove('hidden');
            queueList.classList.add('hidden');
            queueList.innerHTML = '';
            return;
        }

        emptyState.classList.add('hidden');
        queueList.classList.remove('hidden');
        queueList.innerHTML = '';

        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'outreach-item-card';
            card.id = `outreach-card-${item.id}`;

            const mins = Math.floor(item.scheduled_delay_seconds / 60);
            const secs = item.scheduled_delay_seconds % 60;
            const delayStr = mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;

            card.innerHTML = `
                <div class="outreach-header">
                    <span class="outreach-target">👤 ${escapeHtml(item.match_name)}</span>
                    <span class="badge badge-gradient">${escapeHtml(item.platform.toUpperCase())}</span>
                </div>
                <div class="outreach-bio">${escapeHtml(item.match_bio || 'No bio provided')}</div>
                <label style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px; display: block;">Proposed Opener (You can edit before approving):</label>
                <textarea class="outreach-edit-textarea" id="outreach-text-${item.id}" rows="2">${escapeHtml(item.proposed_text)}</textarea>
                <div class="outreach-meta-bar">
                    <span class="outreach-delay-tag">⏱️ Scheduled Delay: ${delayStr} (Human Anti-Detection Jitter)</span>
                    <div class="outreach-actions-row">
                        <button class="btn-approve" onclick="approveOutreach('${item.id}', false)">✅ Approve & Schedule</button>
                        <button class="btn-send-now" onclick="approveOutreach('${item.id}', true)">⚡ Send Now</button>
                        <button class="btn-reject" onclick="rejectOutreach('${item.id}')">❌ Skip</button>
                    </div>
                </div>
            `;
            queueList.appendChild(card);
        });
    } catch (err) {
        console.error("Error loading outreach queue:", err);
    }
}

async function syncOutreach(platform) {
    showToast(`Scanning for new ${platform.toUpperCase()} matches...`);
    try {
        const res = await fetch('/api/outreach/sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ platform: platform })
        });
        const data = await res.json();
        if (data.status === 'success') {
            showToast(`Found & queued ${data.queued_count} matches for approval!`);
            await loadOutreachQueue();
        } else if (data.status === 'rate_limited') {
            showToast(`Safety limit reached: ${data.message}`);
        } else {
            showToast("Sync finished.");
        }
    } catch (err) {
        showToast("Error syncing matches.");
    }
}

async function approveOutreach(itemId, instant) {
    const textArea = document.getElementById(`outreach-text-${itemId}`);
    const editedText = textArea ? textArea.value.trim() : null;

    try {
        const res = await fetch('/api/outreach/approve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                item_id: itemId,
                instant: instant,
                edited_text: editedText
            })
        });
        const result = await res.json();

        if (result.status === 'sent') {
            showToast("⚡ Dispatched text to match immediately!");
        } else {
            showToast(`✅ Approved! Scheduled with human delay (${result.scheduled_delay}s).`);
        }

        // Animate card removal from queue
        const card = document.getElementById(`outreach-card-${itemId}`);
        if (card) {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.remove();
                const remaining = document.querySelectorAll('.outreach-item-card');
                if (remaining.length === 0) {
                    loadOutreachQueue();
                }
            }, 250);
        }
    } catch (err) {
        showToast("Error approving outreach.");
    }
}

async function rejectOutreach(itemId) {
    try {
        await fetch('/api/outreach/reject', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_id: itemId })
        });
        showToast("Match outreach skipped.");

        const card = document.getElementById(`outreach-card-${itemId}`);
        if (card) {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.remove();
                const remaining = document.querySelectorAll('.outreach-item-card');
                if (remaining.length === 0) {
                    loadOutreachQueue();
                }
            }, 250);
        }
    } catch (err) {
        showToast("Error rejecting outreach.");
    }
}

