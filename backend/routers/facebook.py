from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.orm import Session
import requests
from schemas.facebook import FacebookPageCreate
from services.facebook_service import send_message_to_user
from services.chat_service import chat_with_context_service
from schemas.chat import ChatRequest
import json
from database import get_db
from settings.facebook_config import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_REDIRECT_URI, FACEBOOK_VERIFY_TOKEN

router = APIRouter(prefix="/facebook", tags=["Facebook"])

# 1. Webhook verification
@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("🔎 FACEBOOK_VERIFY_TOKEN:", FACEBOOK_VERIFY_TOKEN)
    print("🌐 Received mode/token/challenge:", mode, token, challenge)

    if mode == "subscribe" and token == FACEBOOK_VERIFY_TOKEN:
        return Response(content=str(challenge), media_type="text/plain", status_code=200)

    return Response(content="Verification failed", media_type="text/plain", status_code=403)

# 2. Nhận tin nhắn từ Facebook Messenger
@router.post("/webhook")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    print("📥 Facebook Webhook Received Data:", json.dumps(data, indent=2, ensure_ascii=False))

    for entry in data.get("entry", []):
        page_id = entry["id"]
        for event in entry.get("messaging", []):
            sender_id = event["sender"]["id"]
            if "message" in event and "text" in event["message"]:
                user_message = event["message"]["text"]
                print(f"💬 Tin nhắn từ người dùng ({sender_id}): {user_message}")

                # Hardcode fix cứng không dùng DB
                if page_id == "574045595797104":
                    page = {
                        "agent_id": "default_agent",
                        "page_id": "574045595797104",
                        "page_name": "FTA DNU Page",
                        "access_token": "EAAHsXFhBuPsBO9W6wwOAZCH9HsI3S92paoCim2EFOyWv8Kdido3AhldeCxwLYmEkKJDGZB5HeFZBZANnofRkj9IawLRrM2oIoSxRs0hWBMqF2uSYJ1ZClYCOSKOe1MHpgZCddcj4ILrJw6ZBjwPZAFWqGGFw8mcEZCBMZCiEaUozUkuZBRA686BTilkZBFZBOVDfJyRzK7bO1fdK0ShfuY0lWNQZDZD"
                    }
                else:
                    print(f"❌ Không tìm thấy page_id {page_id}")
                    continue

                chat_request = ChatRequest(
                    sender_id=sender_id,
                    session_id=f"fb_{sender_id}",
                    channel="facebook",
                    message=user_message
                )

                try:
                    bot_reply = chat_with_context_service(chat_request, db)
                    print(f"🤖 AI đã phản hồi: {bot_reply}")
                except Exception as e:
                    print(f"❌ Lỗi khi gọi AI: {e}")
                    bot_reply = "Ui, Oanh gặp chút xíu trục trặc rồi, chờ Oanh chút nhé!"

                try:
                    send_message_to_user(sender_id, bot_reply, page["access_token"])
                    print("✅ Đã gửi trả lời cho người dùng qua Messenger!")
                except Exception as e:
                    print(f"❌ Lỗi khi gửi tin nhắn Facebook: {e}")

    return {"status": "ok"}

# 3. OAuth callback từ Facebook (để frontend lấy danh sách page)
@router.get("/oauth/callback")
def facebook_oauth_callback(code: str, state: str):
    token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "client_id": FACEBOOK_APP_ID,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "client_secret": FACEBOOK_APP_SECRET,
        "code": code,
    }
    token_res = requests.get(token_url, params=params).json()
    user_access_token = token_res.get("access_token")

    accounts_url = "https://graph.facebook.com/v18.0/me/accounts"
    pages = requests.get(accounts_url, params={"access_token": user_access_token}).json()
    return pages.get("data", [])

# 4. Lưu page đã chọn (optional nếu sau này anh cần lưu vào DB)
@router.post("/pages")
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

    subscribe_url = f"https://graph.facebook.com/v18.0/me/subscribed_apps"
    params = {"access_token": data.access_token}
    requests.post(subscribe_url, params=params)
    return {"status": "connected"}
