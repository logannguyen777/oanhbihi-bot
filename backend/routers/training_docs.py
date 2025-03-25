from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.trained_document import TrainedDocument
from models.web_page import WebPage

router = APIRouter(prefix="/api/training", tags=["Training"])

@router.get("/docs")
def get_all_trained_docs(db: Session = Depends(get_db)):
    upload_docs = db.query(TrainedDocument).all()
    web_docs = db.query(WebPage).all()

    uploads = [{
        "type": "upload",
        "id": doc.id,
        "filename": doc.filename,
        "chunk_count": doc.chunk_count,
        "created_at": doc.created_at
    } for doc in upload_docs]

    crawled = [{
        "type": "web",
        "id": doc.id,
        "url": doc.url,
        "content": doc.content[:200],
        "created_at": doc.created_at
    } for doc in web_docs]

    return {
        "uploads": uploads,
        "web": crawled
    }