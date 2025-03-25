import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from models.web_page import WebPage

def search_chunks_from_documents(embedding: list[float], db: Session, k=3):
    # Convert list[float] thành chuỗi vector đúng định dạng PGVector
    embedding_str = "[" + ", ".join(str(x) for x in embedding) + "]"

    # Gắn trực tiếp vào câu query vì không thể bind kiểu vector
    sql = text(f"""
        SELECT content
        FROM document_chunks
        ORDER BY embedding <#> '{embedding_str}'::vector
        LIMIT :limit
    """)
    result = db.execute(sql, {"limit": k})
    return [row[0] for row in result.fetchall()]

def search_chunks_from_web(embedding: list[float], db: Session, k=3):
    pages = db.query(WebPage).filter(WebPage.embedding != None).all()
    results = []

    for page in pages:
        try:
            page_vector = json.loads(page.embedding)
            sim = sum(a * b for a, b in zip(page_vector, embedding))
            results.append((sim, page.content))
        except:
            continue

    results.sort(reverse=True, key=lambda x: x[0])
    return [content for _, content in results[:k]]