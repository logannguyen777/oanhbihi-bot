from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import shutil
import subprocess
import openai
from database import get_db
from models.web_page import WebPage
from models.trained_document import TrainedDocument
from routers.logs_ws import broadcast_log
from services.training_service import train_all

router = APIRouter(prefix="/train", tags=["Train"])
UPLOAD_FOLDER = "downloads"


@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    uploaded = []
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        uploaded.append(file.filename)

        # Lưu thông tin vào bảng TrainedDocument
        doc = TrainedDocument(filename=file.filename, source="upload", chunk_count=0)
        db.add(doc)
        await broadcast_log(f"📄 Đã upload tài liệu: {file.filename}")
    
    db.commit()
    return {"message": "Upload thành công", "files": uploaded}

@router.post("/start")
async def start_training():
    await train_all()
    return {"status": "ok", "message": "Đã bắt đầu huấn luyện!"}
    
@router.get("/web-pages")
def get_web_pages(db: Session = Depends(get_db)):
    pages = db.query(WebPage).order_by(WebPage.id.desc()).limit(100).all()
    return [{"id": p.id, "url": p.url, "content": p.content} for p in pages]