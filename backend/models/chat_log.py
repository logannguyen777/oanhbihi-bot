from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from .enum import ChannelEnum, RoleEnum

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(String, nullable=True)
    channel = Column(Enum(ChannelEnum))
    role = Column(Enum(RoleEnum))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_logs")
    is_read = Column(Boolean, default=False)
