from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
from .base import Base
from .enum import RoleEnum

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum), default="admin")
    created_at = Column(DateTime, default=datetime.utcnow)
