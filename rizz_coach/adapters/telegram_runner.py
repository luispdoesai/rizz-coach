import asyncio
import httpx
from rizz_coach.config import settings
from rizz_coach.adapters.telegram_bot import telegram_bot

async def run_telegram_polling():
    """
    Runs Telegram Bot in long-polling mode.
    Allows 100% phone-based usage without needing any public IP, ngrok, or webhook setup!
    Users simply text their bot from their phone.
    """
    token = settings.telegram_bot_token
    if not token or token == "mock_telegram_token":
        print("\n=======================================================")
        print("📱 RIZZCOACH TELEGRAM MOBILE WINGMAN (PHONE INTEGRATION)")
        print("=======================================================")
        print("To control RizzCoach from your phone via Telegram:")
        print("1. Open Telegram on your phone and search for '@BotFather'")
        print("2. Send '/newbot' and choose a name (e.g. MyRizzCoachBot)")
        print("3. Copy the HTTP API token into your .env file:")
        print("   TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWXyz")
        print("4. Restart this runner:")
        print("   python -m rizz_coach.adapters.telegram_runner")
        print("=======================================================\n")
        return

    url = f"https://api.telegram.org/bot{token}"
    print(f"🚀 [Telegram Mobile Wingman] Polling started! Text your bot directly on your phone.")

    offset = 0
    async with httpx.AsyncClient(timeout=35.0) as client:
        while True:
            try:
                poll_url = f"{url}/getUpdates?offset={offset}&timeout=25"
                resp = await client.get(poll_url)
                if resp.status_code == 200:
                    data = resp.json()
                    for update in data.get("result", []):
                        offset = update["update_id"] + 1
                        asyncio.create_task(telegram_bot.handle_update(update))
                else:
                    await asyncio.sleep(3)
            except Exception as e:
                print(f"[Telegram Polling Notice] {e}")
                await asyncio.sleep(4)

if __name__ == "__main__":
    asyncio.run(run_telegram_polling())
