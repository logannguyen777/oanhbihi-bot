from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, ChatLog, ChannelEnum, RoleEnum, DocumentChunk, WebPage
from datetime import datetime
import openai
import json
import os
from sqlalchemy import text
from services.openai_client import get_openai_client
from openai import OpenAI


chat_router = APIRouter(prefix="/api", tags=["Chat"])

# ===== Models =====
class ChatRequest(BaseModel):
    sender_id: str
    channel: ChannelEnum
    message: str
    session_id: str | None = None

class ChatWithRAGContextRequest(ChatRequest):
    pass

class RAGRequest(BaseModel):
    input_text: str

# ===== DB Session =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== Utility =====
def get_or_create_user(sender_id: str, channel: ChannelEnum, db: Session):
    query_field = {
        ChannelEnum.web: User.phone,
        ChannelEnum.messenger: User.messenger_psid,
        ChannelEnum.zalo: User.zalo_id,
    }[channel]

    user = db.query(User).filter(query_field == sender_id).first()
    if user:
        return user

    user = User()
    if channel == ChannelEnum.web:
        user.phone = sender_id
    elif channel == ChannelEnum.messenger:
        user.messenger_psid = sender_id
    elif channel == ChannelEnum.zalo:
        user.zalo_id = sender_id

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_recent_context(user_id: int, db: Session, limit=5):
    logs = (
        db.query(ChatLog)
        .filter(ChatLog.user_id == user_id)
        .order_by(ChatLog.timestamp.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(logs))

def get_embedding(text: str, client: OpenAI) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def search_chunks_from_documents(embedding: list[float], db: Session, k=3):
    # ✅ Convert list[float] thành chuỗi vector đúng định dạng PGVector
    embedding_str = "[" + ", ".join(str(x) for x in embedding) + "]"

    # ✅ Gắn trực tiếp vào câu query vì không thể bind kiểu vector
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

# ===== Chat Endpoints =====
@chat_router.post("/chat")
def chat_with_context(payload: ChatRequest, db: Session = Depends(get_db)):
    user = get_or_create_user(payload.sender_id, payload.channel, db)

    print("📥 Nhận được câu hỏi:", payload.question)
    print("📜 Lịch sử:", payload.history)

    db.add(ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.user,
        message=payload.message,
        timestamp=datetime.utcnow(),
    ))
    db.commit()

    context_logs = get_recent_context(user.id, db)
    messages = [{"role": log.role.value, "content": log.message} for log in context_logs]
    messages.append({"role": "user", "content": payload.message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    db.add(ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.bot,
        message=bot_reply,
        timestamp=datetime.utcnow(),
    ))
    db.commit()

    return {"reply": bot_reply}


@chat_router.post("/chat-rag")
def chat_with_rag(payload: RAGRequest):
    print("📥 Nhận được input:", payload.input_text)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là Oanh Bihi, một cô bé tư vấn tuyển sinh dễ thương."},
                {"role": "user", "content": payload.input_text}
            ]
        )
        bot_reply = response["choices"][0]["message"]["content"]
        return {"reply": bot_reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.post("/chat-rag-context")
def chat_with_rag_and_context(payload: ChatWithRAGContextRequest, db: Session = Depends(get_db)):
    user = get_or_create_user(payload.sender_id, payload.channel, db)

    db.add(ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.user,
        message=payload.message,
        timestamp=datetime.utcnow(),
    ))
    db.commit()
    print("📥 Nhận được input:", payload.input_text)
    # Lấy context hội thoại
    context_logs = get_recent_context(user.id, db)
    messages = [{"role": log.role.value, "content": log.message} for log in context_logs]
    messages.append({"role": "user", "content": payload.message})

    # Lấy client OpenAI từ service
    client = get_openai_client(db) 

    # Lấy embedding và tìm tài liệu liên quan
    embedding = get_embedding(payload.message, client)
    doc_chunks = search_chunks_from_documents(embedding, db)
    web_chunks = search_chunks_from_web(embedding, db)

    retrieved_knowledge = "\n".join(doc_chunks + web_chunks)

    messages.insert(0, {
        "role": "system",
        "content": f"Oanh Bihi có tri thức từ tài liệu và website như sau:\n{retrieved_knowledge}"
    })

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    db.add(ChatLog(
        user_id=user.id,
        session_id=payload.session_id,
        channel=payload.channel,
        role=RoleEnum.bot,
        message=bot_reply,
        timestamp=datetime.utcnow(),
    ))
    db.commit()

    return {"reply": bot_reply}


# ✅ Export router
router = chat_router
