from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
import requests
import json
import os

router = APIRouter()

VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "oanhbihi-verify")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN", "your-page-token")

@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return params.get("hub.challenge")
    return "Verification failed"

@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    for entry in data.get("entry", []):
        for message_event in entry.get("messaging", []):
            sender_id = message_event["sender"]["id"]
            if "message" in message_event:
                user_message = message_event["message"].get("text", "")
                bot_reply = generate_reply(user_message)
                send_message(sender_id, bot_reply)
    return {"status": "ok"}

def generate_reply(user_input: str) -> str:
    return f"Oanh Bihi chào bạn yêu! Bạn vừa nói: {user_input} ✨"

def send_message(recipient_id: str, message_text: str):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("🔁 Facebook API Response:", response.text)