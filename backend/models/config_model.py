from sqlalchemy import Column, String
from .base import Base

class AppConfig(Base):
    __tablename__ = "configs"
    key = Column(String, primary_key=True)
    value = Column(String)
