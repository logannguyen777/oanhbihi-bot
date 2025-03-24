from sqlalchemy import Column, Integer, String
from .base import Base

class MessengerConfig(Base):
    __tablename__ = "messenger_config"

    id = Column(Integer, primary_key=True, index=True)
    page_token = Column(String, nullable=False)
    verify_token = Column(String, nullable=False)
