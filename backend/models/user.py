from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from .base import Base
from .enum import ChannelEnum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, nullable=True)
    messenger_psid = Column(String, unique=True, nullable=True)
    zalo_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    chat_logs = relationship(
    "ChatLog",
    primaryjoin="foreign(ChatLog.user_id) == cast(User.id, String)",
    back_populates="user",
    viewonly=True
    )


def get_or_create_user(sender_id: str, channel: ChannelEnum, db: Session):
    # ✅ Ép kiểu để đảm bảo tương thích với Enum
    channel = ChannelEnum(channel)

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
