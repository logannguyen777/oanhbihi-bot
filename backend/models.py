from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class MessengerConfig(Base):
    __tablename__ = "messenger_config"

    id = Column(Integer, primary_key=True, index=True)
    page_token = Column(String, nullable=False)
    verify_token = Column(String, nullable=False)

class BotPersona(Base):
    __tablename__ = "bot_persona"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(String)
    gender = Column(String)
    tone = Column(String)
    greeting = Column(String)
    style = Column(String)

class CrawlConfig(Base):
    __tablename__ = "crawl_config"

    id = Column(Integer, primary_key=True, index=True)
    urls = Column(String)  # JSON-encoded list
    file_types = Column(String)  # CSV or JSON-encoded list
    schedule = Column(String)


class ChannelEnum(enum.Enum):
    web = "web"
    messenger = "messenger"
    zalo = "zalo"

class RoleEnum(str, enum.Enum):
    admin = "admin"
    superadmin = "superadmin"
    bot = "bot"
    user = "user"

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum), default="admin")
    created_at = Column(DateTime, default=datetime.utcnow)

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

    chat_logs = relationship("ChatLog", back_populates="user")


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