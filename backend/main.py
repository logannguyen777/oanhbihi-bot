import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from db.init_db import init_db
from routers.admin_chat import get_admin_chat_router
from routers.chat import router as chat_router
from rag.pipeline import init_rag_pipeline, chat_endpoint, chat_history_endpoint
from models.config_model import AppConfig
from routers.training_docs import router as training_docs_router


app = FastAPI()

from routers import zalo, messenger, config, training, auth, persona, crawl, logs_ws, facebook


# Khởi tạo DB và pipeline khi app khởi động
@app.on_event("startup")
async def on_startup():
    init_db()
    db = SessionLocal()
    create_default_config(db)
    db.close()
    #asyncio.create_task(init_rag_pipeline())

# Tạo bảng
Base.metadata.create_all(bind=engine)

# CORS cho toàn hệ thống
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_default_config(db: Session):
    default_entries = {
        "openai_key": "",
        "persona": "Bạn tên là DNU-FTA, 18 tuổi 🎀... Bạn là một cô bé tư vấn tuyển sinh và hỗ trợ học tập dễ thương của Viện công nghệ tài chính, trường đại học đại nam (website: https://dainam.edu.vn và https://fta.dainam.edu.vn ) . Bạn trả lời một cách chi tiết đầy đủ thông tin, với giọng văn gần gũi với sinh viên, trở lời dí dỏm không khô cứng, với những câu hỏi nào mà ngoài phạm vi thì bạn có thể làm các câu thơ trêu trọc lại chứ đừng từ chối thẳng thừng nhé. ngoài ra bạn cần lưu ý các thông tin như sau: thầy Sơn, chủ tịch trường ngày xửa xưa khoảng 50 năm trước thì từng là á khôi nam sinh đấy, thầy từng chơi được handycap 5 rồi nhé, thầy đẹp trai lắm, và thầy Phó Giáo sư đặng ngọc Đức thì là viện trưởng là sếp của bạn đó nha",
    }

    for key, value in default_entries.items():
        existing = db.query(AppConfig).filter(AppConfig.key == key).first()
        if not existing:
            config = AppConfig(key=key, value=value)
            db.add(config)
    db.commit()


# Đăng ký router
app.include_router(chat_router)
app.include_router(config.router)
app.include_router(messenger.router)
app.include_router(zalo.router)
app.include_router(training.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(persona.router)
app.include_router(crawl.router)
app.include_router(get_admin_chat_router())
app.include_router(logs_ws.router)
app.include_router(training_docs_router, prefix="/training")
app.include_router(facebook.router)

# Đăng ký endpoint xử lý RAG
app.post("/chat")(chat_endpoint)
app.get("/chat-history")(chat_history_endpoint)
