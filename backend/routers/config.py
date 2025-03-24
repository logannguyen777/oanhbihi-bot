from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import MessengerConfig as MessengerModel
from models import BotPersona, CrawlConfig


router = APIRouter()

class MessengerConfig(BaseModel):
    pageToken: str
    verifyToken: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/config/messenger")
def save_messenger_config(config: MessengerConfig, db: Session = Depends(get_db)):
    existing = db.query(MessengerModel).first()
    if existing:
        existing.page_token = config.pageToken
        existing.verify_token = config.verifyToken
    else:
        new_config = MessengerModel(
            page_token=config.pageToken,
            verify_token=config.verifyToken
        )
        db.add(new_config)
    db.commit()
    return {"message": "Đã lưu cấu hình Messenger vào DB!"}


# ---------- CẤU HÌNH BOT PERSONA ----------
class PersonaConfig(BaseModel):
    name: str
    age: str
    gender: str
    tone: str
    greeting: str
    style: str

@router.post("/api/config/persona")
def save_bot_persona(config: PersonaConfig, db: Session = Depends(get_db)):
    existing = db.query(BotPersona).first()
    if existing:
        for field, value in config.dict().items():
            setattr(existing, field, value)
    else:
        new_config = BotPersona(**config.dict())
        db.add(new_config)
    db.commit()
    return {"message": "Đã lưu cấu hình Bot & Persona vào DB!"}

# ---------- CẤU HÌNH CRAWL ----------
from typing import List
import json
from models import CrawlConfig as CrawlModel

class CrawlConfigRequest(BaseModel):
    urls: List[str]
    fileTypes: List[str]
    schedule: str

@router.post("/api/config/crawl")
def save_crawl_config(config: CrawlConfigRequest, db: Session = Depends(get_db)):
    existing = db.query(CrawlModel).first()
    if existing:
        existing.urls = json.dumps(config.urls)
        existing.file_types = json.dumps(config.fileTypes)
        existing.schedule = config.schedule
    else:
        new_config = CrawlModel(
            urls=json.dumps(config.urls),
            file_types=json.dumps(config.fileTypes),
            schedule=config.schedule
        )
        db.add(new_config)
    db.commit()
    return {"message": "Đã lưu cấu hình crawl vào DB!"}