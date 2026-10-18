import os
import time
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

API = f"https://api.telegram.org/bot{TOKEN}/"

def send_message(chat_id, text):
    requests.post(
        API + "sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=15
    )

offset = 0

while True:
    try:
        response = requests.get(
            API + "getUpdates",
            params={"offset": offset, "timeout": 25},
            timeout=30
        ).json()

        for update in response.get("result", []):
            offset = update["update_id"] + 1
            message = update.get("message", {})
            chat = message.get("chat", {})
            text = message.get("text", "")

            if not chat:
                continue

            if text == "/start":
                send_message(
                    chat["id"],
                    "🔥 Welcome to MARK INJECTOR BOT!\n\n"
                    "Piliin ang command:\n"
                    "/help - Tingnan ang commands\n"
                    "/about - Tungkol sa bot"
                )
            elif text == "/help":
                send_message(
                    chat["id"],
                    "📌 COMMANDS\n/start - Simulan\n"
                    "/help - Tulong\n/about - Impormasyon"
                )
            elif text == "/about":
                send_message(
                    chat["id"],
                    "MARK INJECTOR BOT\n"
                    "Official bot information and support."
                )

    except Exception:
        time.sleep(3)
