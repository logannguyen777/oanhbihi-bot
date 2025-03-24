from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, ChatLog, RoleEnum
from datetime import datetime

from routers.logs_ws import broadcast_chat_update  # ✅ dùng WebSocket thay vì socketio

bot_control = {}

class TogglePayload(BaseModel):
    user_id: int

class AdminReplyPayload(BaseModel):
    user_id: int
    message: str

class UserID(BaseModel):
    user_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_admin_chat_router():
    router = APIRouter()

    @router.get("/api/admin/conversations")
    def list_conversations(db: Session = Depends(get_db)):
        users = db.query(User).all()
        data = []
        for user in users:
            last = (
                db.query(ChatLog)
                .filter(ChatLog.user_id == user.id)
                .order_by(ChatLog.timestamp.desc())
                .first()
            )
            unread_count = (
                db.query(ChatLog)
                .filter(ChatLog.user_id == user.id, ChatLog.role == RoleEnum.user, ChatLog.is_read == False)
                .count()
            )
            data.append({
                "id": user.id,
                "name": user.name or user.phone or user.messenger_psid,
                "channel": "web" if user.phone else "messenger" if user.messenger_psid else "zalo",
                "lastMessage": last.message if last else "(chưa có)",
                "botEnabled": bot_control.get(user.id, {"bot_enabled": True})["bot_enabled"],
                "unread": unread_count
            })
        return {"users": data}

    @router.get("/api/admin/conversations/{user_id}")
    def get_user_conversation(user_id: int, db: Session = Depends(get_db)):
        logs = (
            db.query(ChatLog)
            .filter(ChatLog.user_id == user_id)
            .order_by(ChatLog.timestamp.asc())
            .all()
        )
        conversation = [
            {
                "id": log.id,
                "role": log.role,
                "message": log.message,
                "timestamp": log.timestamp.isoformat(),
                "channel": log.channel
            } for log in logs
        ]
        return {"user_id": user_id, "conversation": conversation}

    @router.post("/api/admin/toggle-bot")
    async def toggle_bot(payload: TogglePayload):
        status = bot_control.get(payload.user_id, {"bot_enabled": True})
        status["bot_enabled"] = not status["bot_enabled"]
        bot_control[payload.user_id] = status
        await broadcast_chat_update()  # ✅ emit bằng WebSocket
        return {"message": f"Đã cập nhật trạng thái bot cho user {payload.user_id}"}

    @router.post("/api/admin/reply")
    async def admin_reply(payload: AdminReplyPayload, db: Session = Depends(get_db)):
        log = ChatLog(
            user_id=payload.user_id,
            role=RoleEnum.admin,
            message=payload.message,
            timestamp=datetime.utcnow(),
            channel="web",
        )
        db.add(log)
        db.commit()
        await broadcast_chat_update()  # ✅ emit bằng WebSocket
        return {"message": "Đã lưu phản hồi từ admin"}

    return router
