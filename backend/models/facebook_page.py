from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime
from database import Base

class FacebookPage(Base):
    __tablename__ = "facebook_pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    agent_id = Column(UUID(as_uuid=True), nullable=False)  # Bỏ ForeignKey
    page_id = Column(String, unique=True)
    page_name = Column(String)
    access_token = Column(String)
    webhook_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
