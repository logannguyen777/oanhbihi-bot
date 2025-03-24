from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import shutil
import subprocess
import openai
#from services.training_service import trigger_training_pipeline
from database import get_db
from models.web_page import WebPage

router = APIRouter(prefix="/api/training", tags=["Training"])
UPLOAD_FOLDER = "downloads"




@router.post("/api/train/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    uploaded = []
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        uploaded.append(file.filename)
    return {"message": "Upload thành công", "files": uploaded}

@router.post("/api/train/start")
def start_training():
    try:
        result = subprocess.run(["python", "train_data.py"], capture_output=True, text=True, timeout=60)
        return {
            "message": "✅ Đã gọi script huấn luyện!",
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"message": "⏱️ Quá thời gian khi train bot!"}
    except Exception as e:
        return {"message": f"Lỗi: {e}"}
    
@router.get("/web-pages")
def get_web_pages(db: Session = Depends(get_db)):
    pages = db.query(WebPage).order_by(WebPage.id.desc()).limit(100).all()
    return [{"id": p.id, "url": p.url, "content": p.content} for p in pages]