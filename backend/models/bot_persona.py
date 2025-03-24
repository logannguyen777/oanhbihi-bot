from sqlalchemy import Column, Integer, String
from .base import Base

class BotPersona(Base):
    __tablename__ = "bot_persona"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(String)
    gender = Column(String)
    tone = Column(String)
    greeting = Column(String)
    style = Column(String)
