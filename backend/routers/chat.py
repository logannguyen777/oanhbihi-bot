from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, ChatLog, ChannelEnum, RoleEnum
from datetime import datetime
import openai

# ✅ Khởi tạo router
chat_router = APIRouter(prefix="/api", tags=["Chat"])

# ✅ Request model
class ChatRequest(BaseModel):
    sender_id: str
    channel: ChannelEnum
    message: str
    session_id: str | None = None

# ✅ DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Hàm phụ trợ: tạo hoặc lấy user
def get_or_create_user(sender_id: str, channel: ChannelEnum, db: Session):
    query_field = {
        ChannelEnum.web: User.phone,
        ChannelEnum.messenger: User.messenger_psid,
        ChannelEnum.zalo: User.zalo_id,
    }[channel]

    user = db.query(User).filter(query_field == sender_id).first()
    if user:
        return user

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

# ✅ Hàm phụ trợ: lấy context gần nhất
def get_recent_context(user_id: int, db: Session, limit=5):
    logs = (
        db.query(ChatLog)
        .filter(ChatLog.user_id == user_id)
        .order_by(ChatLog.timestamp.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(logs))

# ✅ Route chính: /api/chat
@chat_router.post("/chat")
def chat_with_context(payload: ChatRequest, db: Session = Depends(get_db)):
    user = get_or_create_user(payload.sender_id, payload.channel, db)

    db.add(ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.user,
        message=payload.message,
        timestamp=datetime.utcnow(),
    ))
    db.commit()

    context_logs = get_recent_context(user.id, db)
    messages = [{"role": log.role.value, "content": log.message} for log in context_logs]
    messages.append({"role": "user", "content": payload.message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    db.add(ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.bot,
        message=bot_reply,
        timestamp=datetime.utcnow(),
    ))
    db.commit()

    return {"reply": bot_reply}

# ✅ Export đúng router
router = chat_router
