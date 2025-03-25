from sqlalchemy.orm import Session
from models.chat_log import ChatLog

def get_recent_context(user_id: int, db: Session, limit=5):
    logs = (
        db.query(ChatLog)
        .filter(ChatLog.user_id == user_id)
        .order_by(ChatLog.timestamp.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(logs))
