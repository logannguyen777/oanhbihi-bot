import os
from sqlalchemy.orm import Session
from database import SessionLocal
from models.web_page import WebPage
from models.document import Document
from models.document_chunk import DocumentChunk
from services.utils.embedding import generate_embedding
from routers.logs_ws import broadcast_log

TEXT_FILE_TYPES = [".txt", ".md"]
PDF_FILE_TYPES = [".pdf"]
DOC_FILE_TYPES = [".doc", ".docx"]
DOWNLOADS_FOLDER = "downloads"

def split_text(text, max_tokens=500):
    paragraphs = text.split("\\n")
    chunks, current = [], ""
    for para in paragraphs:
        if len((current + para).split()) < max_tokens:
            current += para + "\\n"
        else:
            chunks.append(current.strip())
            current = para + "\\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks

async def train_all():
    await broadcast_log("🚀 Bắt đầu huấn luyện toàn bộ dữ liệu...")
    await train_from_web_pages()
    await train_from_uploaded_files()
    await broadcast_log("✅ Hoàn tất huấn luyện!")

async def train_from_web_pages():
    db: Session = SessionLocal()
    try:
        await broadcast_log("🌐 Huấn luyện từ dữ liệu web đã crawl...")
        pages = db.query(WebPage).all()
        for page in pages:
            chunks = split_text(page.content)
            doc = Document(filename=page.url, source="web")
            db.add(doc)
            db.flush()
            for chunk in chunks:
                emb = generate_embedding(chunk)
                doc_chunk = DocumentChunk(content=chunk, embedding=emb, document_id=doc.id)
                db.add(doc_chunk)
        db.commit()
        await broadcast_log(f"✅ Đã huấn luyện {len(pages)} trang web")
    finally:
        db.close()

async def train_from_uploaded_files():
    db: Session = SessionLocal()
    try:
        await broadcast_log("📄 Huấn luyện từ tài liệu đã upload...")
        files = os.listdir(DOWNLOADS_FOLDER)
        for file in files:
            path = os.path.join(DOWNLOADS_FOLDER, file)
            ext = os.path.splitext(file)[1].lower()
            content = ""

            try:
                if ext in TEXT_FILE_TYPES:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                elif ext in PDF_FILE_TYPES:
                    import fitz
                    doc = fitz.open(path)
                    content = "\\n".join([page.get_text() for page in doc])
                elif ext in DOC_FILE_TYPES:
                    import docx
                    doc = docx.Document(path)
                    content = "\\n".join([p.text for p in doc.paragraphs])
                else:
                    await broadcast_log(f"⚠️ Không hỗ trợ file: {file}")
                    continue
            except Exception as e:
                await broadcast_log(f"❌ Lỗi đọc file {file}: {e}")
                continue

            chunks = split_text(content)
            doc = Document(filename=file, source="upload")
            db.add(doc)
            db.flush()
            for chunk in chunks:
                emb = generate_embedding(chunk)
                doc_chunk = DocumentChunk(content=chunk, embedding=emb, document_id=doc.id)
                db.add(doc_chunk)
        db.commit()
        await broadcast_log(f"✅ Đã huấn luyện {len(files)} tài liệu")
    finally:
        db.close()