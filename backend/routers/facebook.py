from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import requests
from models.facebook_page import FacebookPage
from schemas.facebook import FacebookPageCreate
from database import get_db
from settings.facebook_config import *

router = APIRouter()

# 1. Webhook verification
@router.get("/facebook/webhook", response_class=PlainTextResponse)
def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("🔎 FACEBOOK_VERIFY_TOKEN:", FACEBOOK_VERIFY_TOKEN)
    print("🌐 Received mode/token/challenge:", mode, token, challenge)

    if mode == "subscribe" and token == FACEBOOK_VERIFY_TOKEN:
        return Response(content=str(challenge), media_type="text/plain", status_code=200)

    return Response(content="Verification failed", media_type="text/plain", status_code=403)

# 2. Nhận tin nhắn
@router.post("/facebook/webhook")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    for entry in data.get("entry", []):
        page_id = entry["id"]
        for event in entry.get("messaging", []):
            sender = event["sender"]["id"]
            if "message" in event and "text" in event["message"]:
                text = event["message"]["text"]
                page = db.query(FacebookPage).filter_by(page_id=page_id).first()
                if page:
                    reply = await run_rag_on_agent(page.agent_id, text)
                    send_fb_message(sender, reply, page.access_token)
    return {"status": "ok"}

# 3. OAuth callback
@router.get("/facebook/oauth/callback")
def facebook_oauth_callback(code: str, state: str):
    # 1. Exchange code for access token
    token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "client_id": FACEBOOK_APP_ID,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "client_secret": FACEBOOK_APP_SECRET,
        "code": code,
    }
    token_res = requests.get(token_url, params=params).json()
    user_access_token = token_res.get("access_token")

    # 2. Get pages
    accounts_url = "https://graph.facebook.com/v18.0/me/accounts"
    pages = requests.get(accounts_url, params={"access_token": user_access_token}).json()
    return pages["data"]  # frontend sẽ hiển thị list page cho user chọn

# 4. Lưu page đã chọn
@router.post("/api/facebook/pages")
def save_facebook_page(data: FacebookPageCreate, db: Session = Depends(get_db)):
    page = FacebookPage(
        agent_id=data.agent_id,
        page_id=data.page_id,
        page_name=data.page_name,
        access_token=data.access_token,
        webhook_verified=True,
    )
    db.add(page)
    db.commit()

    # Subscribed webhook
    url = f"https://graph.facebook.com/v18.0/me/subscribed_apps"
    params = {"access_token": data.access_token}
    requests.post(url, params=params)
    return {"status": "connected"}
