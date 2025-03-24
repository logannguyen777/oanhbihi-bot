from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db
from models import CrawlConfig
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from services.config_service import set_config
from pgvector.psycopg2 import register_vector
from fastapi_socketio import SocketManager
from services.crawl_service import get_crawl_config, update_crawl_config
from services.socket import sio

router = APIRouter(prefix="/api/crawl", tags=["crawl"])

class CrawlIn(BaseModel):
    url: str
    selector: str
    label: str = ""

@router.get("", response_model=List[CrawlIn])
def get_all_crawls(db: Session = Depends(get_db)):
    return db.query(CrawlConfig).all()

@router.post("")
def add_crawl(config: CrawlIn, db: Session = Depends(get_db)):
    crawl = CrawlConfig(**config.dict())
    db.add(crawl)
    db.commit()
    return {"message": "✅ Đã thêm crawl config!"}

@router.delete("/{id}")
def delete_crawl(id: int, db: Session = Depends(get_db)):
    crawl = db.query(CrawlConfig).filter(CrawlConfig.id == id).first()
    if not crawl:
        raise HTTPException(status_code=404, detail="Không tìm thấy cấu hình")
    db.delete(crawl)
    db.commit()
    return {"message": "🗑️ Đã xoá config crawl"}

@router.post("/run")
def run_crawl_all(db: Session = Depends(get_db)):
    configs = db.query(CrawlConfig).all()
    count = 0
    for conf in configs:
        try:
            r = requests.get(conf.url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.select(conf.selector)
            for it in items:
                link = it.select_one("a")
                content = it.text.strip()
                url = link["href"].strip() if link else None
                if not url:
                    continue
                cursor.execute("""
                    INSERT INTO web_pages (url, content)
                    VALUES (%s, %s)
                    ON CONFLICT (url) DO NOTHING
                """, (url, content))
                count += 1
            conn.commit()
            sio.emit("log", f"🌐 Crawled {conf.label or conf.url} - Thêm {count} bản ghi.")
        except Exception as e:
            sio.emit("log", f"⚠️ Lỗi crawl {conf.url}: {e}")
    return {"message": f"✅ Đã crawl {len(configs)} config, thêm {count} bản ghi."}