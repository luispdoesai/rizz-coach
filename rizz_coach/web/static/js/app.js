// =========================================================
// RizzCoach - Client Interactive Controller & Ergonomics Engine
// Architecture: Studio UX, Keyboard Accelerators, Tactile Feedback
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

// ----------------------------------------------------
// Navigation & Tab Switching
// ----------------------------------------------------
function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.setAttribute('aria-selected', 'false');
    });
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    const activeBtn = document.getElementById(`tab-${tabId}-btn`);
    const activeContent = document.getElementById(`tab-${tabId}`);

    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.setAttribute('aria-selected', 'true');
    }
    if (activeContent) {
        activeContent.classList.add('active');
    }

    if (tabId === 'automation') {
        loadOutreachQueue();
    }
}

// ----------------------------------------------------
// Tactile Toast Notifications
// ----------------------------------------------------
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';

    let iconSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`;
    if (type === 'success') {
        iconSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent-emerald)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>`;
    } else if (type === 'warn') {
        iconSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent-amber)" stroke-width="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
    }

    toast.innerHTML = `<span>${iconSvg}</span><span>${escapeHtml(message)}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(8px)';
        toast.style.transition = 'all 160ms ease';
        setTimeout(() => toast.remove(), 180);
    }, 2800);
}

// ----------------------------------------------------
// Tactile Clipboard Copy
// ----------------------------------------------------
function copyToClipboard(text, btnElement) {
    navigator.clipboard.writeText(text).then(() => {
        if (btnElement) {
            const originalHtml = btnElement.innerHTML;
            btnElement.classList.add('copied');
            btnElement.innerHTML = `
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Copied!</span>
            `;
            setTimeout(() => {
                btnElement.classList.remove('copied');
                btnElement.innerHTML = originalHtml;
            }, 1800);
        }
        showToast("Copied to clipboard!", "success");
    }).catch(() => {
        showToast("Copied!", "success");
    });
}

// ----------------------------------------------------
// Sample Preset Loaders
// ----------------------------------------------------
function loadSampleChat() {
    document.getElementById('chat-history-input').value = SAMPLE_CHATS.chloe;
    document.getElementById('match-name-input').value = "Chloe";
    showToast("Loaded sample banter conversation", "info");
}

function loadSampleDeadChat() {
    document.getElementById('autopsy-history-input').value = SAMPLE_CHATS.dead_chat;
    showToast("Loaded dead chat sample", "info");
}

function loadSampleBio() {
    document.getElementById('profile-bio-input').value = SAMPLE_BIOS.bio;
    document.getElementById('profile-prompts-input').value = SAMPLE_BIOS.prompts;
    document.getElementById('profile-photos-input').value = SAMPLE_BIOS.photos;
    showToast("Loaded sample bio & photo cues", "info");
}

// ----------------------------------------------------
// TAB 1: Live Wingman Analysis
// ----------------------------------------------------
async function runAnalysis() {
    const chatHistory = document.getElementById('chat-history-input').value.trim();
    const targetName = document.getElementById('match-name-input').value.trim() || "Match";
    const btn = document.getElementById('btn-run-analysis');

    if (!chatHistory) {
        showToast("Paste a conversation first.", "warn");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = `<span>Decoding Dynamics...</span>`;

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

        document.getElementById('report-interest-score').textContent = `${data.interest_score}/100`;
        document.getElementById('report-interest-level').textContent = data.interest_level;
        document.getElementById('report-subtext').textContent = data.subtext_translation;
        document.getElementById('report-frame').textContent = data.frame_holder;
        document.getElementById('report-investment').textContent = data.investment_ratio;

        // Warnings List
        const warningsList = document.getElementById('report-warnings-list');
        const warningsBox = document.getElementById('report-warnings-box');
        warningsList.innerHTML = '';
        if (data.cringe_warnings && data.cringe_warnings.length > 0) {
            warningsBox.classList.remove('hidden');
            data.cringe_warnings.forEach(w => {
                const li = document.createElement('li');
                li.textContent = w;
                warningsList.appendChild(li);
            });
        } else {
            warningsBox.classList.add('hidden');
        }

        // Tactical Moves Deck
        const movesList = document.getElementById('report-moves-list');
        movesList.innerHTML = '';

        data.tactical_moves.forEach(move => {
            const card = document.createElement('div');
            card.className = 'move-card';
            card.innerHTML = `
                <div class="move-header">
                    <span class="move-category">${escapeHtml(move.category)}</span>
                    <span class="move-score">Rizz ${move.rizz_score}/100</span>
                </div>
                <div class="move-text-row">
                    <span class="move-text">"${escapeHtml(move.text)}"</span>
                    <button class="btn-copy" onclick="copyToClipboard('${escapeJs(move.text)}', this)">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                        <span>Copy</span>
                    </button>
                </div>
                <div class="move-rationale">Tactical Rationale: ${escapeHtml(move.rationale)}</div>
            `;
            movesList.appendChild(card);
        });

        showToast("Conversation decoded successfully!", "success");
    } catch (err) {
        showToast("Error analyzing conversation.", "warn");
        console.error(err);
    } finally {
        btn.disabled = false;
        btn.innerHTML = `
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            <span>Decode Subtext & Generate Moves</span>
        `;
    }
}

// Quick Draft Scorer
async function testDraft() {
    const draft = document.getElementById('draft-test-input').value.trim();
    const context = document.getElementById('chat-history-input').value.trim();
    const resultBox = document.getElementById('draft-score-result');
    const btn = document.getElementById('btn-test-draft');

    if (!draft) {
        showToast("Type a draft message first.", "warn");
        return;
    }

    resultBox.classList.remove('hidden');
    resultBox.innerHTML = "<span style='color: var(--text-muted);'>Evaluating draft tension...</span>";
    btn.disabled = true;

    try {
        const res = await fetch('/api/score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draft_message: draft, context_message: context })
        });
        const score = await res.json();

        let badgeColor = score.score >= 80 ? 'var(--accent-emerald-text)' : (score.score >= 65 ? 'var(--accent-amber-text)' : 'var(--accent-rose-text)');
        let flagsHtml = (score.cringe_flags || []).map(f => `<div style="color: var(--accent-rose-text); font-size: 11.5px; margin-top: 3px;">• ${escapeHtml(f)}</div>`).join('');

        resultBox.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-family: var(--font-mono); font-weight:700; font-size:15px; color:${badgeColor};">${score.score}/100</span>
                    <span style="font-size: 11px; font-weight:600; padding: 2px 6px; border-radius: var(--radius-xs); background: var(--bg-surface); border: 1px solid var(--border-subtle); color: var(--text-secondary);">${score.letter_grade}</span>
                </div>
                <span style="font-size:11px; font-family: var(--font-mono); color:var(--text-muted);">Pacing: ${escapeHtml(score.pacing_rating)}</span>
            </div>
            <p style="margin-bottom:6px; color:var(--text-primary); font-size:12.5px; line-height:1.45;">${escapeHtml(score.why_it_scored)}</p>
            ${flagsHtml ? `<div style="margin-bottom:8px;">${flagsHtml}</div>` : ''}
            ${score.suggested_rewrite ? `
                <div style="background:var(--bg-surface); border:1px solid var(--border-default); border-radius:var(--radius-sm); padding:10px 12px; margin-top:8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.04em; color:var(--accent-primary);">Calibrated Rewrite (+20 Rizz)</span>
                        <button class="btn-copy" onclick="copyToClipboard('${escapeJs(score.suggested_rewrite)}', this)">
                            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                            <span>Copy</span>
                        </button>
                    </div>
                    <div style="font-size:13px; color:var(--text-primary);">"${escapeHtml(score.suggested_rewrite)}"</div>
                </div>
            ` : ''}
        `;
    } catch (err) {
        resultBox.innerHTML = "<span style='color: var(--accent-rose-text);'>Error evaluating draft.</span>";
    } finally {
        btn.disabled = false;
    }
}

// ----------------------------------------------------
// TAB 2: The Rizz Gym Simulator
// ----------------------------------------------------
function selectArchetype(archetypeId) {
    currentArchetype = archetypeId;
    document.querySelectorAll('.archetype-chip').forEach(c => c.classList.remove('active'));
    if (window.event && window.event.currentTarget) {
        window.event.currentTarget.classList.add('active');
    }
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

    document.getElementById('gym-sideline-text').textContent = "Sparring match started. Match her frame, avoid qualifying yourself, and keep banter high.";
    document.getElementById('gym-turn-score').textContent = "Awaiting Round";
}

function appendGymMessage(sender, text, type) {
    const chatLog = document.getElementById('gym-chat-log');
    const wrap = document.createElement('div');
    wrap.className = `chat-bubble-wrap ${type}`;
    wrap.innerHTML = `
        <div class="bubble-sender">${escapeHtml(sender)}</div>
        <div class="chat-bubble">${escapeHtml(text)}</div>
    `;
    chatLog.appendChild(wrap);
    chatLog.scrollTop = chatLog.scrollHeight;
}

function showGymTypingIndicator(senderName) {
    const chatLog = document.getElementById('gym-chat-log');
    const wrap = document.createElement('div');
    wrap.className = 'chat-bubble-wrap incoming';
    wrap.id = 'gym-typing-bubble';
    wrap.innerHTML = `
        <div class="bubble-sender">${escapeHtml(senderName)}</div>
        <div class="typing-indicator">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    `;
    chatLog.appendChild(wrap);
    chatLog.scrollTop = chatLog.scrollHeight;
}

function removeGymTypingIndicator() {
    const bubble = document.getElementById('gym-typing-bubble');
    if (bubble) bubble.remove();
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

    // Show simulated typing indicator for natural conversational pacing
    const currentName = document.getElementById('active-char-name').textContent.split(' ')[0] || "Match";
    showGymTypingIndicator(currentName);

    try {
        const [res] = await Promise.all([
            fetch('/api/gym/turn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    archetype_id: currentArchetype,
                    user_message: text,
                    history: gymHistory
                })
            }),
            new Promise(r => setTimeout(r, 650)) // realistic typing pacing
        ]);

        const data = await res.json();
        removeGymTypingIndicator();

        // Append character reply
        appendGymMessage(data.character_name, data.character_reply, 'incoming');
        gymHistory.push({ role: data.character_name, content: data.character_reply });

        // Update sideline feedback
        document.getElementById('gym-turn-score').textContent = `Move Score: ${data.coach_feedback.turn_rizz_score}/100`;
        document.getElementById('gym-sideline-text').innerHTML = `
            <strong>${escapeHtml(data.coach_feedback.what_worked)}</strong><br>
            <span style="color:var(--accent-sky-text); margin-top: 3px; display: block;">Coach Tip: ${escapeHtml(data.coach_feedback.coaching_tip)}</span>
        `;
    } catch (err) {
        removeGymTypingIndicator();
        showToast("Error in sparring round.", "warn");
    } finally {
        btn.disabled = false;
        input.focus();
    }
}

// ----------------------------------------------------
// TAB 3: Profile Lab & Bio Auditor
// ----------------------------------------------------
async function auditProfile() {
    const bio = document.getElementById('profile-bio-input').value.trim();
    const prompts = document.getElementById('profile-prompts-input').value.trim();
    const photos = document.getElementById('profile-photos-input').value.trim();
    const btn = document.getElementById('btn-audit-profile');

    if (!bio) {
        showToast("Enter a bio to audit.", "warn");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = "<span>Auditing Profile Assets...</span>";

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
        document.getElementById('profile-score-badge').textContent = `Rating: ${data.overall_score}/100`;
        document.getElementById('profile-bio-critique').textContent = data.bio_critique;

        // Photos critique
        const photoList = document.getElementById('profile-photo-list');
        photoList.innerHTML = '';
        data.photo_audit.forEach(p => {
            const item = document.createElement('div');
            item.className = 'photo-item';
            item.innerHTML = `
                <div><strong>Photo ${p.photo_num}:</strong> ${escapeHtml(p.verdict)}</div>
                <span class="telemetry-chip">${p.score}/100</span>
            `;
            photoList.appendChild(item);
        });

        // Clichés
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
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span class="bio-style-tag">${escapeHtml(b.style)}</span>
                    <button class="btn-copy" onclick="copyToClipboard('${escapeJs(b.bio)}', this)">
                        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                        <span>Copy Bio</span>
                    </button>
                </div>
                <div class="bio-text-content">"${escapeHtml(b.bio)}"</div>
            `;
            biosList.appendChild(card);
        });

        showToast("Profile audit completed!", "success");
    } catch (err) {
        showToast("Error auditing profile.", "warn");
    } finally {
        btn.disabled = false;
        btn.innerHTML = `
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <span>Audit Profile & Generate High-Value Bios</span>
        `;
    }
}

// ----------------------------------------------------
// TAB 4: Chat Autopsy
// ----------------------------------------------------
async function runAutopsy() {
    const history = document.getElementById('autopsy-history-input').value.trim();
    const btn = document.getElementById('btn-run-autopsy');

    if (!history) {
        showToast("Paste the stalled conversation first.", "warn");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = "<span>Analyzing Fatal Point...</span>";

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
                <div class="move-text-row">
                    <span class="move-text">"${escapeHtml(r.text)}"</span>
                    <button class="btn-copy" onclick="copyToClipboard('${escapeJs(r.text)}', this)">
                        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                        <span>Copy</span>
                    </button>
                </div>
                <div class="move-rationale">Strategic Rationale: ${escapeHtml(r.why_it_works)}</div>
            `;
            revivalsList.appendChild(card);
        });

        showToast("Autopsy report ready!", "success");
    } catch (err) {
        showToast("Error running autopsy.", "warn");
    } finally {
        btn.disabled = false;
        btn.innerHTML = `
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
            <span>Run Post-Mortem & Generate Revival Moves</span>
        `;
    }
}

// ----------------------------------------------------
// TAB 5: Automation Simulator
// ----------------------------------------------------
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

        showToast(`Intake Pipeline: ${decision.action}`, "info");
    } catch (err) {
        showToast("Error processing automation.", "warn");
    }
}

// ----------------------------------------------------
// Outreach & Approval Queue Controller
// ----------------------------------------------------
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
                    <span class="outreach-name">Match: ${escapeHtml(item.match_name)}</span>
                    <span class="outreach-platform-badge">${escapeHtml(item.platform.toUpperCase())}</span>
                </div>
                <div class="outreach-bio">Profile Cue: ${escapeHtml(item.match_bio || 'No bio provided')}</div>
                <label style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px; display: block;">Proposed Opener (Edit before approving):</label>
                <textarea class="outreach-edit-textarea" id="outreach-text-${item.id}" rows="2">${escapeHtml(item.proposed_text)}</textarea>
                <div class="outreach-meta-bar">
                    <span class="outreach-delay-tag">Anti-Detection Pacing Delay: ${delayStr}</span>
                    <div class="btn-group-row">
                        <button class="btn-approve" onclick="approveOutreach('${item.id}', false)">Approve & Schedule</button>
                        <button class="btn-send-now" onclick="approveOutreach('${item.id}', true)">Send Now</button>
                        <button class="btn-reject" onclick="rejectOutreach('${item.id}')">Skip</button>
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
    showToast(`Scanning for new ${platform.toUpperCase()} matches...`, "info");
    try {
        const res = await fetch('/api/outreach/sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ platform: platform })
        });
        const data = await res.json();
        if (data.status === 'success') {
            showToast(`Found & queued ${data.queued_count} matches for approval!`, "success");
            await loadOutreachQueue();
        } else if (data.status === 'rate_limited') {
            showToast(`Safety limit reached: ${data.message}`, "warn");
        } else {
            showToast("Sync finished.", "info");
        }
    } catch (err) {
        showToast("Error syncing matches.", "warn");
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
            showToast("Dispatched text immediately!", "success");
        } else {
            showToast(`Approved! Scheduled with ${result.scheduled_delay}s delay.`, "success");
        }

        const card = document.getElementById(`outreach-card-${itemId}`);
        if (card) {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.97)';
            card.style.transition = 'all 200ms ease';
            setTimeout(() => {
                card.remove();
                const remaining = document.querySelectorAll('.outreach-item-card');
                if (remaining.length === 0) {
                    loadOutreachQueue();
                }
            }, 200);
        }
    } catch (err) {
        showToast("Error approving outreach.", "warn");
    }
}

async function rejectOutreach(itemId) {
    try {
        await fetch('/api/outreach/reject', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_id: itemId })
        });
        showToast("Match outreach skipped.", "info");

        const card = document.getElementById(`outreach-card-${itemId}`);
        if (card) {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.97)';
            card.style.transition = 'all 200ms ease';
            setTimeout(() => {
                card.remove();
                const remaining = document.querySelectorAll('.outreach-item-card');
                if (remaining.length === 0) {
                    loadOutreachQueue();
                }
            }, 200);
        }
    } catch (err) {
        showToast("Error rejecting outreach.", "warn");
    }
}

// ----------------------------------------------------
// Global Keyboard Shortcuts
// ----------------------------------------------------
document.addEventListener('keydown', (e) => {
    const isModifier = e.metaKey || e.ctrlKey;
    const activeEl = document.activeElement;
    const isInputActive = activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA');

    // Cmd+Enter / Ctrl+Enter shortcuts for rapid submission
    if (isModifier && e.key === 'Enter') {
        e.preventDefault();
        if (activeEl && activeEl.id === 'draft-test-input') {
            testDraft();
        } else if (activeEl && (activeEl.id === 'profile-bio-input' || activeEl.id === 'profile-prompts-input' || activeEl.id === 'profile-photos-input')) {
            auditProfile();
        } else if (activeEl && activeEl.id === 'autopsy-history-input') {
            runAutopsy();
        } else if (activeEl && activeEl.id === 'gym-user-input') {
            sendGymMessage();
        } else {
            // Default action: decode wingman
            runAnalysis();
        }
        return;
    }

    // Number keys 1-5 for switching tabs when NOT in text input
    if (!isInputActive && !isModifier) {
        if (e.key === '1') switchTab('wingman');
        else if (e.key === '2') switchTab('gym');
        else if (e.key === '3') switchTab('profile');
        else if (e.key === '4') switchTab('autopsy');
        else if (e.key === '5') switchTab('automation');
    }
});

// Helpers
function escapeHtml(text) {
    if (!text) return '';
    return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function escapeJs(text) {
    if (!text) return '';
    return String(text).replace(/'/g, "\\'").replace(/"/g, '\\"');
}
