#!/usr/bin/env bash
set -e

# ==============================================================================
# 🔥 RizzCoach - 1-Click Launch Script
# ==============================================================================

echo ""
echo "  ██████╗ ██╗███████╗███████╗ ██████╗ ██████╗  █████╗  ██████╗██╗  ██╗"
echo "  ██╔══██╗██║╚══███╔╝╚══███╔╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██║  ██║"
echo "  ██████╔╝██║  ███╔╝   ███╔╝ ██║     ██║   ██║███████║██║     ███████║"
echo "  ██╔══██╗██║ ███╔╝   ███╔╝  ██║     ██║   ██║██╔══██║██║     ██╔══██║"
echo "  ██║  ██║██║███████╗███████╗╚██████╗╚██████╔╝██║  ██║╚██████╗██║  ██║"
echo "  ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝"
echo "         Autonomous Text Game Copilot & Phone Wingman Engine"
echo ""

# 1. Check Python version
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD=python
else
    echo "❌ Error: Python 3.10+ is required but not installed."
    exit 1
fi

# 2. Virtual environment setup
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment (.venv)..."
    $PYTHON_CMD -m venv .venv
fi

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Install dependencies if needed
echo "⚡ Checking dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# 5. Ensure .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
fi

# 6. Optional: Detect Local IP for Phone Access
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 RIZZCOACH IS RUNNING!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💻 Web Workstation:       http://localhost:8000"
echo "📱 Mobile Local Network:  http://${LOCAL_IP}:8000"
echo "⚡ iPhone Quick Action:   http://${LOCAL_IP}:8000/api/mobile/quick-coach"
echo "💬 iMessage Bridge:       http://localhost:8000/api/mobile/imessage/recent"
echo ""
echo "💡 To share with friends on their phones via free public tunnel:"
echo "   npx cloudflared tunnel --url http://localhost:8000"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 7. Start server
exec python -m rizz_coach.server
