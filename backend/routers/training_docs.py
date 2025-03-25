from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.trained_document import TrainedDocument
from models.web_page import WebPage
from models.document import Document
from models.document_chunk import DocumentChunk

router = APIRouter(prefix="/api/training", tags=["Training"])

@router.get("/docs")
def get_all_trained_docs(db: Session = Depends(get_db)):
    # Upload tài liệu (đã huấn luyện)
    upload_docs = db.query(TrainedDocument).all()
    uploads = [{
        "type": "upload",
        "id": doc.id,
        "filename": doc.filename,
        "chunk_count": doc.chunk_count,
        "created_at": doc.created_at
    } for doc in upload_docs]

    # Dữ liệu crawl từ web (đã train)
    web_docs = db.query(Document).filter(Document.source == "web").all()
    crawled = []
    for doc in web_docs:
        chunk_count = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).count()
        crawled.append({
            "type": "web",
            "id": doc.id,
            "url": doc.filename,  # với web, filename = URL
            "chunk_count": chunk_count,
            "created_at": doc.created_at
        })

    total_chunks = sum([doc["chunk_count"] for doc in uploads]) + sum([doc["chunk_count"] for doc in crawled])

    return {
        "uploads": uploads,
        "web": crawled,
        "total_chunks": total_chunks
    }
