from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, ChatLog, ChannelEnum, RoleEnum
from datetime import datetime
import openai

router = APIRouter()

# Fake API Key tạm thời (sẽ được cấu hình sau)
openai.api_key = "YOUR_OPENAI_API_KEY"

class ChatRequest(BaseModel):
    sender_id: str  # phone | psid | zalo_id
    channel: ChannelEnum
    message: str
    session_id: str | None = None  # chỉ cần với web chat

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_user(sender_id: str, channel: ChannelEnum, db: Session):
    query_field = {
        ChannelEnum.web: User.phone,
        ChannelEnum.messenger: User.messenger_psid,
        ChannelEnum.zalo: User.zalo_id,
    }[channel]

    user = db.query(User).filter(query_field == sender_id).first()
    if user:
        return user

    # Tạo user mới nếu chưa tồn tại
    user = User()
    if channel == ChannelEnum.web:
        user.phone = sender_id
    elif channel == ChannelEnum.messenger:
        user.messenger_psid = sender_id
    elif channel == ChannelEnum.zalo:
        user.zalo_id = sender_id

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_recent_context(user_id: int, db: Session, limit=5):
    logs = (
        db.query(ChatLog)
        .filter(ChatLog.user_id == user_id)
        .order_by(ChatLog.timestamp.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(logs))

@router.post("/api/chat")
def chat_with_context(payload: ChatRequest, db: Session = next(get_db())):
    user = get_or_create_user(payload.sender_id, payload.channel, db)

    # Lưu message user
    user_msg = ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.user,
        message=payload.message,
        timestamp=datetime.utcnow(),
    )
    db.add(user_msg)
    db.commit()

    # Lấy context
    context_logs = get_recent_context(user.id, db)
    messages = []
    for log in context_logs:
        messages.append({
            "role": log.role.value,
            "content": log.message
        })
    messages.append({"role": "user", "content": payload.message})

    # Gọi OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Lưu message bot
    bot_log = ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.bot,
        message=bot_reply,
        timestamp=datetime.utcnow(),
    )
    db.add(bot_log)
    db.commit()

    return {"reply": bot_reply}