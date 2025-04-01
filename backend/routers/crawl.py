from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db
from models import CrawlConfig
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from sqlalchemy import text
from services.training_service import train_from_web_pages
from routers.logs_ws import broadcast_log
from schemas.crawl import CrawlConfigSchema 
from services.spider_crawler import crawl_and_download_files
from services.training_service import train_from_uploaded_files
import urllib.parse
from urllib.parse import urlparse, unquote


router = APIRouter(prefix="/crawl", tags=["crawl"])

# ✅ Schema Pydantic để nhận request
class CrawlIn(BaseModel):
    url: str
    selector: str
    label: str = ""

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

# ================================
# 🔍 Lấy danh sách cấu hình crawl
# ================================
@router.get("", response_model=List[CrawlIn])
def get_all_crawls(db: Session = Depends(get_db)):
    return db.query(CrawlConfig).all()

# ================================
# ➕ Thêm cấu hình crawl
# ================================
@router.post("")
def add_crawl(config: CrawlConfigSchema, db: Session = Depends(get_db)):
    try:
        crawl = CrawlConfig(
            url=config.url,
            depth=config.depth,
            use_browser=config.use_browser
        )
        db.add(crawl)
        db.commit()
        return {"message": "✅ Đã thêm crawl config!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi thêm config: {e}")


# ================================
# ❌ Xoá cấu hình crawl
# ================================
@router.delete("/{id}")
def delete_crawl(id: int, db: Session = Depends(get_db)):
    crawl = db.query(CrawlConfig).filter(CrawlConfig.id == id).first()
    if not crawl:
        raise HTTPException(status_code=404, detail="Không tìm thấy cấu hình")
    db.delete(crawl)
    db.commit()
    return {"message": "🗑️ Đã xoá config crawl"}

# ================================
# 🚀 Chạy crawl tất cả config
# ================================
@router.post("/run")
async def run_crawl_all(db: Session = Depends(get_db)):
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
                db.execute(
                    text("""
                        INSERT INTO web_pages (url, content)
                        VALUES (:url, :content)
                        ON CONFLICT (url) DO NOTHING
                    """), {"url": url, "content": content}
                )
                count += 1
            db.commit()
            await broadcast_log(f"🌐 Crawled {conf.label or conf.url} - Thêm {count} bản ghi.")
        except Exception as e:
            await broadcast_log(f"⚠️ Lỗi crawl {conf.url}: {e}")
    return {"message": f"✅ Đã crawl {len(configs)} config, thêm {count} bản ghi."}

# ================================
# ⚡ Crawl & huấn luyện tức thì
# ================================
@router.post("/instant")
async def instant_crawl(payload: dict, db: Session = Depends(get_db)):
    url = payload.get("url")
    url = urllib.parse.unquote(url)

    url = unquote(payload.get("url", "").strip())
    if not url:
        raise HTTPException(status_code=400, detail="Thiếu URL")

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise HTTPException(status_code=400, detail="❌ URL không hợp lệ")

    if not url or not url.strip():
        raise HTTPException(status_code=400, detail="Thiếu URL")

    try:
        await broadcast_log(f"🕸️ Đang bắt đầu crawl spider từ: {url}")
        await crawl_and_download_files(url, depth=2)  # 👈 Crawl đệ quy trong domain, độ sâu 2

        await broadcast_log(f"📥 Đã tải xong tài liệu từ {url}")
        await broadcast_log(f"🧠 Đang huấn luyện...")

        await train_from_uploaded_files()

        return {"message": f"✅ Crawl & train từ {url} hoàn tất!"}

    except Exception as e:
        await broadcast_log(f"❌ Lỗi huấn luyện: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi crawl: {e}")