import os
import httpx
from fastapi import FastAPI, Request

BOT_TOKEN = os.environ["BOT_TOKEN"]

# जहाँ तुम पोस्ट डालोगे
SOURCE_CHANNEL = -1003458574167

# जहाँ पोस्ट अपने आप कॉपी होगी
TARGET_CHANNEL = -1002454087643

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "Telegram copy bot is running"}


@app.post("/telegram")
async def telegram_webhook(request: Request):
    update = await request.json()

    channel_post = update.get("channel_post")

    if channel_post:
        message_id = channel_post.get("message_id")

        if message_id:
            api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage"

            data = {
                "chat_id": TARGET_CHANNEL,
                "from_chat_id": SOURCE_CHANNEL,
                "message_id": message_id
            }

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(api_url, json=data)
                print(response.text)

    return {"ok": True}


@app.on_event("startup")
async def set_webhook():
    render_url = os.environ.get("RENDER_EXTERNAL_URL")

    if not render_url:
        print("RENDER_EXTERNAL_URL not found")
        return

    webhook_url = f"{render_url}/telegram"

    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            api_url,
            json={"url": webhook_url}
        )

        print("Webhook:", response.text)
