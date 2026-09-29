# 🔥 OpenWingman (RizzCoach)

> **The Open-Source AI Dating Coach & Autonomous Rizz Engine.**  
> *Stop paying $3,000 for dating coaches and $10/week for predatory rizz apps.*

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Privacy: 100% BYOK](https://img.shields.io/badge/Privacy-100%25%20Self--Hosted-orange.svg)](#privacy--byok)

---

## ⚡ Why OpenWingman?

| Feature | Human Dating Coaches | Proprietary Rizz Apps | OpenWingman |
| :--- | :--- | :--- | :--- |
| **Cost** | $1,500 – $5,000+ | $10/week ($520/yr) | **$0 (Free & Open Source)** |
| **Privacy** | Zero (You tell a human) | Sold to ad networks / trained on | **100% Local / Self-Hosted (Zero Telemetry)** |
| **Availability** | Hourly calls / Scheduling | Slow & rigid | **Instant 24/7 (Web, Telegram, SMS)** |
| **Sparring Practice** | Roleplay over Zoom | None | **Interactive "Rizz Gym" Simulator** |
| **Profile Auditing** | $300 single review | None | **Instant Photo & Bio Rewriter** |
| **Automation & Filters**| None | None | **Auto-Pacing, Ghost Detection, Number Scraping** |

---

## 🚀 Key Modules

### 1. 🎯 Live Wingman & Subtext Decoder
- **Subtext Translation**: Unmasks what she actually meant (*"She's matching your playful energy but testing to see if you can hold frame"*).
- **Cringe Interceptor**: Automatically warns you if you are double-texting too fast, over-apologizing, or writing essays when she replies with 3 words.
- **3 Tactical Moves**:
  - `Banter / Push-Pull`: Creates sexual/conversational tension.
  - `Direct Escalation`: Moves smoothly to drinks or getting her phone number.
  - `Low-Investment Reset`: Deals with dry/lukewarm replies without losing frame.

### 2. 🥊 The Rizz Gym (Interactive Sparring Simulator)
Practice your text game before messaging real matches. Spar against real dating archetypes:
- **Chloe (The Banter Queen)**: Sharp, playful, roasts generic openers on sight.
- **Elena (The Skeptical High-Flyer)**: Corporate consultant; tests whether you fold or qualify yourself.
- **Mia (The Dry Replier)**: Sends 3-word replies; teaches you to lead without over-investing.
- **Sofia (The Adventurous Creative)**: Vibe-focused; loves spontaneous, deep late-night topics.
*Includes real-time sideline coach feedback with a Turn Score (0–100) and actionable tip after each message.*

### 3. 📸 Profile & Bio Auditor
- **Cliche Detection**: Flags bathroom mirror gym selfies, sunglasses hiding eye contact, and resume-style hobby lists.
- **Bio Rewriter**: Generates 3 high-converting bios (*Witty & Polarizing*, *High-Value Minimalist*, and *Playful Storyteller*).

### 4. 🩻 Chat Autopsy (Ghosting Diagnostic)
- Pinpoints the **exact Fatal Turn** where momentum died.
- Identifies the root cause (e.g. conversational overload, asking too many questions).
- Generates **2 high-ROI Revival Texts** ("Hail Mary" ping & playful frame flip).

### 5. 🤖 Automated Messaging & Funnel Filters
- **Anti-Detection Pacing**: Calculates human jitter delays (e.g., 3–12 mins) to avoid bot detection.
- **Success/Fail Classifier**:
  - Automatically extracts phone numbers and Instagram handles (`CONVERTED_NUMBER`).
  - Detects date commitments (`CONVERTED_DATE`).
  - Automatically hands off to the user once the contact info is secured.

---

## 🛠️ Quickstart in 60 Seconds

### Option A: Local Python

```bash
# 1. Clone repo
git clone https://github.com/your-username/rizz-coach.git
cd rizz-coach

# 2. Setup Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Copy Environment & Run
cp .env.example .env
python -m rizz_coach.server
```

Open **`http://localhost:8000`** in your browser to launch the dashboard!

---

### Option B: Docker Compose

```bash
docker compose up -d
```

---

## 🔒 Privacy & BYOK (Bring Your Own Key)

Configure your `.env` file to use any LLM provider:

```bash
# Option 1: Local Ollama (100% Free & Private)
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434

# Option 2: OpenAI / DeepSeek / Groq
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-...

# Option 3: Offline Smart Mock (Runs immediately without any API keys)
LLM_PROVIDER=mock
```

---

## 📱 How to Wire Up Live Messaging

### 1. Telegram Mobile Wingman (In Your Pocket)
Forward texts or upload screenshots directly to your personal Telegram bot:
1. Create a bot with `@BotFather` on Telegram.
2. Put `TELEGRAM_BOT_TOKEN=your_token` in your `.env`.
3. Receive instant coaching reports and copyable replies on your phone in under 2 seconds.

### 2. Virtual SMS via Twilio
1. Add `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER` to `.env`.
2. Set Twilio incoming SMS webhook to:
   ```
   POST http://your-server:8000/webhooks/twilio
   ```

### 3. iOS Shortcuts / Generic Webhook
Trigger coaching breakdowns directly from your phone’s Share Sheet or clipboard:
```bash
curl -X POST http://localhost:8000/webhooks/generic \
  -H "Content-Type: application/json" \
  -d '{"message": "haha nice, what are you up to this weekend?"}'
```

---

## 🧪 Testing

Run the automated test suite with pytest:

```bash
pytest tests/
```

---

## 📜 License & Ethics

- **License**: [MIT License](LICENSE)
- **Disclaimer**: Please read our [DISCLAIMER.md](DISCLAIMER.md). This project is intended for educational and personal communication coaching. Respect third-party platform rules.
