from sqlalchemy import create_engine
from models import (
    User,
    AdminUser,
    ChatLog,
    MessengerConfig,
    BotPersona,
    CrawlConfig,
)
from database import Base, DATABASE_URL

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
