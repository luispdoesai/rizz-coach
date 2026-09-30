# 🔥 RizzCoach

> **The 100% Free, Open-Source AI Dating Coach & Autonomous Rizz Engine.**  
> *Stop paying $3,000 to "dating gurus" and $10/week for predatory dating apps. Your phone, your rules, your data.*

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Privacy: 100% BYOK](https://img.shields.io/badge/Privacy-100%25%20Self--Hosted-orange.svg)](#-privacy--byok-bring-your-own-key)
[![Dating Science](https://img.shields.io/badge/Methodology-Manson%20%2B%20Ury%20%2B%20Hussey-red.svg)](METHODOLOGY.md)

---

## ⚡ Why Does This Exist?

Most modern dating advice falls into two bad extremes:
1. **Overpriced "Dating Gurus"**: Charging $3,000+ for generic advice over Zoom calls.
2. **Predatory App Subscriptions**: Charging $10 to $15 every single week just to generate 3 cheesy pickup lines, while selling your chat screenshots to ad brokers.

**RizzCoach gives you an elite, private wingman in your pocket for $0.**

| Feature | Human Dating Coaches | Proprietary $10/wk Apps | 🔥 RizzCoach |
| :--- | :--- | :--- | :--- |
| **Cost** | $1,500 – $5,000+ | $10/week ($520/year!) | **$0 (100% Free & Open-Source)** |
| **Privacy** | Zero (You tell a stranger) | Sold to ad networks / logged | **100% Local (Runs on your machine, zero tracking)** |
| **Availability** | Hourly calls / Scheduling | Slow & rigid | **Instant 24/7 (Web, Telegram, SMS)** |
| **Science-Backed** | Often creepy "pickup" tricks | Random GPT wrapper | **Proven Relationship Science (Manson, Ury, Hussey)** |
| **Interactive Sparring**| Awkward roleplay over Zoom | None | **Interactive "Rizz Gym" text simulator** |
| **Outreach & Approvals**| None | None | **Tinder & Instagram match auto-sync with 1-tap approval** |

---

## 🎮 What Can It Do For You?

### 1. 🎯 Live Wingman & Subtext Decoder
*Paste any conversation from Hinge, Tinder, Bumble, or Instagram, and get instant intel:*
* **Subtext Translation**: Tells you what she *actually* means emotional-wise (*"She's playfully testing to see if you can hold frame, or if you'll panic and fold into interview mode"*).
* **The Cringe Interceptor**: Automatically warns you if you're double-texting too fast, apologizing for no reason, or writing 4-sentence essays in response to 3 words.
* **3 Tactical Moves**:
  1. `Banter / Push-Pull`: Creates playful tension without being insulting.
  2. `Direct Escalation`: Smoothly moves the chat toward drinks or getting her number.
  3. `Low-Investment Reset`: Matches her energy if she sent a short or lukewarm text, protecting your frame.

### 2. ⚡ Live Draft Scorer (Check Before You Send!)
Type out what you were *about* to hit send on. RizzCoach gives you:
* A letter grade (`A+` to `F`) and a 0–100 Rizz Score.
* Immediate red flags: `interview_mode` (asking dry resume questions), `pedestalizing` (over-complimenting too early), or `essay_trap`.
* A **+20 Rizz Suggested Rewrite** that upgrades your message into something relaxed and confident.

### 3. 🥊 The Rizz Gym (Interactive Sparring Simulator)
Practice your text game before messaging your real matches! Spar against 4 realistic archetypes:
* **Chloe (The Banter Queen)**: Roasts boring openers on sight; loves sharp teasing.
* **Elena (The Skeptical High-Flyer)**: Corporate consultant in NYC; tests whether you qualify yourself when challenged.
* **Mia (The Dry Replier)**: Sends 3-word texts (`"haha cool"`, `"wyd"`); trains you to lead without over-investing.
* **Sofia (The Adventurous Creative)**: Spontaneous, vibe-focused, loves deep late-night topics.
* *Includes real-time sideline coach feedback with a Turn Score and actionable tactical tips after every single message.*

### 4. 🩻 Chat Autopsy (Ghosting Diagnostic)
Got ghosted or stuck on read? 
* Pinpoints the **exact Fatal Turn** where conversational momentum died.
* Diagnoses the root cause (e.g. asking too many questions, waiting 3 weeks to propose a date).
* Gives you **2 high-ROI Revival Texts** (*The Playful Callout* & *The Curiosity Loop*) that reboot dead conversations with zero bitterness.

### 5. 📸 Profile & Bio Doctor
* Flags profile cliches: bathroom mirror gym selfies, sunglasses hiding eye contact, resume-like lists.
* Generates 3 distinctive, high-converting bios: *Witty & Polarizing*, *High-Value Minimalist*, and *Playful Storyteller*.

### 6. 🤖 Autonomous Outreach with Human Approvals (Copilot Mode)
Connect your Tinder or Instagram account to find matches awaiting an opener:
* RizzCoach reads her bio and photos, crafting a tailored opener using proven dating science.
* Sends an approval card straight to your **Telegram** or **Web Dashboard** with:
  * **`[✅ Approve & Schedule]`**: Sends after a randomized 3–8 minute human delay (so dating apps never detect a bot).
  * **`[⚡ Send Now]`**: Sends immediately.
  * **`[❌ Skip / Reject]`**: Discards the match.
* **Automatic Handoff**: The instant she sends a phone number or agrees to drinks, the bot halts and notifies you to take over!

---

## 🚀 Quickstart: Up and Running in 30 Seconds

> [!NOTE]
> **No API keys or credit cards needed!** RizzCoach comes out-of-the-box with a smart offline mock engine, so you can test every single feature immediately without spending a dime.

### ⚡ 1-Command Launch (Recommended)
Simply clone and run `start.sh` — it automatically creates the virtual environment, installs dependencies, initializes your `.env`, and launches the engine:

```bash
git clone https://github.com/luispdoesai/rizz-coach.git
cd rizz-coach
./start.sh
```

Once running, open **`http://localhost:8000`** in your browser, or hit the endpoints directly from your phone!

<details>
<summary><b>🛠️ Manual Setup (Click to expand if you prefer manual steps)</b></summary>

```bash
# 1. Set up Python environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install requirements
pip install -r requirements.txt

# 3. Copy environment and launch
cp .env.example .env
python -m rizz_coach.server
```
</details>

---

## 🎨 Customize the Coach Without Knowing Any Code!

You don't need to be a programmer to change how RizzCoach talks. All system prompts are plain English markdown files located in [`rizz_coach/prompts/`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/):

| Prompt File | What You Can Tweak In Plain English |
| :--- | :--- |
| [**`prompts/analyzer.md`**](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/analyzer.md) | Adjust the subtext decoder, banter tone, and tactical moves. |
| [**`prompts/scorer.md`**](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/scorer.md) | Make the cringe police stricter, add custom pet peeves, or adjust grade scales. |
| [**`prompts/profile.md`**](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/profile.md) | Change bio rewriter styles and photo critique criteria. |
| [**`prompts/autopsy.md`**](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/autopsy.md) | Customize ghosting diagnosis and revival openers. |
| [**`prompts/gym.md`**](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/gym.md) | Tweak how spicy Chloe's roasts are or add your own custom sparring personas. |

Want the coach to have British dry wit or speak more casually? Just open the `.md` file, type your instructions, and save!

---

## 📚 Grounded in Proven Relationship Science

RizzCoach doesn't use sleazy pickup artist tricks. Every engine strictly enforces proven principles from world-class authors and relationship scientists:

* **Mark Manson (*Models: Attract Women Through Honesty*)**: True confidence is non-neediness (expressing interest without seeking approval) and bold polarization over agreeable small talk.
* **Logan Ury (*How to Not Die Alone*, Director of Relationship Science at Hinge)**: Banning "Interview Mode" questions and applying the 4–8 message momentum rule to lock in in-person dates before texting fatigue sets in.
* **Matthew Hussey (*Get the Guy*)**: "Dropping the Handkerchief" (leaving low-friction conversational runways) and sending unbothered, playful revival texts.
* **Todd V / Modern Communication Coaches**: Calibrated Push-Pull tension, matching conversational investment (word count & pacing), and proposing low-pressure false time constraints.
* **Blaine Anderson (*Dating by Blaine*)**: Strict photo hierarchy (smiling with teeth, direct eye contact, candid lifestyle) and zero gym mirror selfies.

👉 *Read the full scientific breakdown in [**METHODOLOGY.md**](METHODOLOGY.md).*

---

## 📱 The Phone-First Wingman: For You & Other People's Phones

> **"Dating happens on phones, not laptops."**  
> Nobody opens a desktop browser while sitting at a bar or swiping in bed. RizzCoach connects directly to phones so **you or anyone else** can get subtext decoding and top tactical moves without ever touching a web UI.

### 1. ✈️ Telegram Pocket Wingman (Multi-User, Zero-Install)
*The easiest way for ANYONE on iPhone or Android to use RizzCoach:*
* **Zero app install needed**: Works on standard Telegram.
* **Multi-tenant & private**: Every person has their own isolated session based on their Telegram account.
* **How people use it**:
  1. Forward or type any text from Tinder, Hinge, Instagram, or iMessage to `@RizzCoachBot`.
  2. The bot instantly decodes her emotional subtext, checks for cringe/over-investment, and returns **3 tap-to-copy tactical replies** directly to their phone screen.
  3. Commands on the go:
     * `/score <draft>` — Test what you're about to send before sending it.
     * `/sync` — Scan Tinder or Instagram for new matches and get 1-tap approval buttons.
     * `/pending` — Review queue with `[✅ Approve & Schedule]`, `[⚡ Send Now]`, and `[❌ Skip]`.
     * `/imessage` — Inspect recent iMessage threads and dispatch replies.

### 2. ⚡ iPhone 1-Tap Action Button & iOS Shortcuts (Instant Clipboard Copy)
*For iPhone users who want instantaneous replies while inside Tinder, Instagram, or Messages:*
* **How it works**:
  1. Highlight or copy any text message from a match.
  2. Press the **iPhone Action Button** (iPhone 15/16 Pro), double-tap the back of the phone (**Back Tap**), or tap **Share Sheet &rarr; RizzCoach**.
  3. RizzCoach hits `/api/mobile/quick-coach`, calculates the best tactical response, and **copies it directly to your iPhone clipboard** while displaying an iOS notification banner HUD.
  4. Double-tap and paste into your chat! Total time: **0.8 seconds**.
* **Quick Setup for Any iPhone User**:
  1. In the Apple **Shortcuts** app, create a shortcut named `RizzCoach`.
  2. Add Action: `Get Clipboard`.
  3. Add Action: `Get Contents of URL` &rarr; `POST` to `http://<your-host>:8000/api/mobile/quick-coach` with JSON `{ "text": Clipboard }`.
  4. Add Action: `Get Dictionary Value` &rarr; Key `clipboard_text`.
  5. Add Action: `Copy to Clipboard`.
  6. Add Action: `Show Notification` &rarr; Text: `result['ios_hud']`.

### 3. 💬 Apple iMessage Native Connector (macOS Bridge)
*Direct integration with Apple Messages:*
* Reads live conversation threads directly from `~/Library/Messages/chat.db`.
* Dispatches messages seamlessly via AppleScript (`osascript`) with smart mock fallback for cross-platform testing.
* Endpoint: `POST /api/mobile/imessage/send` and `POST /api/mobile/imessage/tactical-reply`.

### 4. 🌐 Sharing With Other People's Phones (Zero-Config Hosting)
Want to give friends or other people access to RizzCoach from their phones?
* **Local Network (Wi-Fi)**: Have them connect to `http://<your-mac-ip>:8000`.
* **Instant Free HTTPS Public URL**: Run a quick tunnel:
  ```bash
  # Using Cloudflare (No account or port-forwarding needed)
  npx cloudflared tunnel --url http://localhost:8000
  ```
  Share the generated `https://xyz.trycloudflare.com` URL. Anyone on earth can now use the mobile web app or configure their iOS Shortcut to point to it!
* **Cloud Deploy (1-Click)**:
  RizzCoach includes a production `Dockerfile` and `docker-compose.yml`. Deploy to Fly.io or Render with `fly launch` in 60 seconds.


## 🔒 Privacy & BYOK (Bring Your Own Key)

You own your data. Configure your [`.env`](file:///Users/luispadilla/Desktop/rizz-coach/.env) file to use whichever LLM you want:

```bash
# Option 1: Offline Smart Mock (Runs immediately with zero keys)
LLM_PROVIDER=mock

# Option 2: 100% Free & Private Local AI (Ollama)
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434

# Option 3: Cloud LLMs (OpenAI, Groq, Anthropic, DeepSeek)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-...
```

---

## 🛡️ Anti-Ban Safety Rules for Tinder & Instagram

Dating apps ban accounts that behave like spambots. RizzCoach has built-in safety guardrails:
1. **Randomized Human Pacing Jitter**: Messages are never sent instantly. RizzCoach randomly waits 3 to 12 minutes before sending, simulating realistic human typing and phone pickup times.
2. **Daily Outreach Caps**: Capped at `MAX_DAILY_OUTREACH=15` per day by default.
3. **Automatic Handoff**: As soon as a match sends a phone number or confirms a date, the bot halts immediately and alerts you to take over.

---

## 🧪 Testing

Run the automated test suite with one command:
```bash
.venv/bin/pytest tests/
```
All 16 unit and integration tests will run in under a second!

---

## 📜 License & Ethical Dating

- **License**: [MIT License](LICENSE) (Free for personal and educational use).
- **Ethics**: Please read [DISCLAIMER.md](DISCLAIMER.md). RizzCoach is built to improve authentic communication, eliminate texting anxiety, and help people meet in the real world. Treat everyone with respect and respect platform guidelines.
