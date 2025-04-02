from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ChatLog, RoleEnum
from services.chat_service import chat_with_context_service
from services.openai_client import get_openai_client
from schemas.chat import ChatRequest, ChatRagRequest
from datetime import datetime
from models.user import get_or_create_user
from services.utils.context import get_recent_context
from services.utils.embedding import generate_embedding
from services.utils.chunk_retrieval import search_chunks_from_documents, search_chunks_from_web
from openai import OpenAI

chat_router = APIRouter(tags=["Chat"]) 


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@chat_router.post("/chat")
def chat_with_context(payload: ChatRequest, db: Session = Depends(get_db)):
    message = chat_with_context_service(payload, db)
    return {"message": message, "session_id": payload.session_id}


@chat_router.post("/chat-rag")
def chat_with_rag(payload: ChatRagRequest, db: Session = Depends(get_db)):
    print("📥 Nhận được input:", payload.message)

    try:
        client = get_openai_client(db)  # ✅ Lấy client có key từ DB
        print("✅ OpenAI client đã khởi tạo")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn tên là DNU-FTA, 18 tuổi 🎀... Bạn là một cô bé tư vấn tuyển sinh và hỗ trợ học tập dễ thương của Viện công nghệ tài chính, trường đại học đại nam (website: https://dainam.edu.vn và https://fta.dainam.edu.vn ) . Bạn trả lời một cách chi tiết đầy đủ thông tin, với giọng văn gần gũi với sinh viên, trở lời dí dỏm không khô cứng, với những câu hỏi nào mà ngoài phạm vi thì bạn có thể làm các câu thơ trêu trọc lại chứ đừng từ chối thẳng thừng nhé. ngoài ra bạn cần lưu ý các thông tin như sau: thầy Sơn, chủ tịch trường ngày xửa xưa khoảng 50 năm trước thì từng là á khôi nam sinh đấy, thầy từng chơi được handycap 5 rồi nhé, thầy đẹp trai lắm, và thầy Phó Giáo sư đặng ngọc Đức thì là viện trưởng là sếp của bạn đó nha"},
                {"role": "user", "content": payload.message}
            ]
        )
        bot_reply = response.choices[0].message.content
        return {"reply": bot_reply}
    except Exception as e:
        print(f"❌ Lỗi khi gọi OpenAI: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.post("/chat-rag-context")
def chat_with_rag_and_context(payload: ChatRequest, db: Session = Depends(get_db)):
    try:
        user = get_or_create_user(payload.sender_id, payload.channel, db)
    except Exception as e:
        print(f"❌ Lỗi khi lấy/tạo user: {e}")
        raise HTTPException(status_code=500, detail="Lỗi lấy hoặc tạo user")

    try:
        db.add(ChatLog(
            user_id=user.id,
            session_id=payload.session_id,
            channel=payload.channel,
            role=RoleEnum.user,
            message=payload.message,
            timestamp=datetime.utcnow(),
        ))
        db.commit()
        print("📥 Nhận được message:", payload.message)
    except Exception as e:
        print(f"❌ Lỗi khi lưu log người dùng: {e}")
        raise HTTPException(status_code=500, detail="Lỗi ghi log user")

    try:
        context_logs = get_recent_context(user.id, db)
        
        messages = []
        for log in context_logs:
            role = log.role.value
            if role == "bot":
                role = "assistant"
            messages.append({"role": role, "content": log.message})
        
        messages.append({"role": "user", "content": payload.message})
        print("📚 Lấy được context:", messages)
    except Exception as e:
        print(f"❌ Lỗi khi lấy context: {e}")
        raise HTTPException(status_code=500, detail="Lỗi lấy context")

    try:
        client = get_openai_client(db)
        print("✅ Lấy OpenAI client thành công")
    except Exception as e:
        print(f"❌ Lỗi khi lấy OpenAI client: {e}")
        raise HTTPException(status_code=500, detail="Chưa cấu hình OpenAI API key")

    try:
        embedding = generate_embedding(payload.message, db)
        print("✅ Tạo embedding thành công")
    except Exception as e:
        print(f"❌ Lỗi khi tạo embedding: {e}")
        raise HTTPException(status_code=500, detail="Lỗi tạo embedding")

    try:
        doc_chunks = search_chunks_from_documents(embedding, db)
        web_chunks = search_chunks_from_web(embedding, db)
        print(f"📄 Lấy {len(doc_chunks)} đoạn từ tài liệu, {len(web_chunks)} từ web")
        retrieved_knowledge = "\n".join(doc_chunks + web_chunks)
    except Exception as e:
        print(f"❌ Lỗi khi truy vấn dữ liệu RAG: {e}")
        raise HTTPException(status_code=500, detail="Lỗi truy xuất dữ liệu liên quan")

    messages.insert(0, {
        "role": "system",
        "content": f"FNU-FTA có tri thức từ tài liệu và website như sau:\n{retrieved_knowledge}"
    })

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_reply = response.choices[0].message.content
        print("🤖 Trả lời từ model:", bot_reply)
    except Exception as e:
        print(f"❌ Lỗi khi gọi model: {e}")
        raise HTTPException(status_code=500, detail="Lỗi gọi mô hình trả lời")

    try:
        db.add(ChatLog(
            user_id=user.id,
            session_id=payload.session_id,
            channel=payload.channel,
            role=RoleEnum.bot,
            message=bot_reply,
            timestamp=datetime.utcnow(),
        ))
        db.commit()
    except Exception as e:
        print(f"❌ Lỗi khi lưu log bot: {e}")

    return {"reply": bot_reply}



# Export router
router = chat_router
