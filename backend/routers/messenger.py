from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import requests
from services.config_service import get_config
from database import get_db

router = APIRouter()

@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(request: Request, db: Session = Depends(get_db)):
    params = dict(request.query_params)
    VERIFY_TOKEN = get_config(db, "fb_verify_token")
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return params.get("hub.challenge")
    return "Verification failed"

@router.post("/webhook")
async def receive_message(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    PAGE_ACCESS_TOKEN = get_config(db, "fb_page_token")

    for entry in data.get("entry", []):
        for message_event in entry.get("messaging", []):
            sender_id = message_event["sender"]["id"]
            if "message" in message_event:
                user_message = message_event["message"].get("text", "")
                bot_reply = "Oanh Bihi đang phản hồi bạn nè 🎀"
                requests.post(
                    f"https://graph.facebook.com/v15.0/me/messages?access_token={PAGE_ACCESS_TOKEN}",
                    json={
                        "recipient": {"id": sender_id},
                        "message": {"text": bot_reply},
                    }
                )
    return {"status": "ok"}