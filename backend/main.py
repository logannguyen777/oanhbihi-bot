from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from database import Base, engine
from db.init_db import init_db
from routers.admin_chat import get_admin_chat_router
from routers.chat import router as chat_router
from rag.pipeline import init_rag_pipeline, chat_endpoint, chat_history_endpoint
from routers import logs_ws


app = FastAPI()

from routers import zalo, messenger, config, training, auth, persona, crawl


# Khởi tạo DB và pipeline khi app khởi động
@app.on_event("startup")
def on_startup():
    init_db()
    init_rag_pipeline(sio)

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

# Đăng ký router
app.include_router(chat_router)
app.include_router(config.router)
app.include_router(messenger.router)
app.include_router(zalo.router)
app.include_router(training.router)
app.include_router(auth.router)
app.include_router(persona.router)
app.include_router(crawl.router)
app.include_router(get_admin_chat_router())
app.include_router(logs_ws.router)

# Đăng ký endpoint xử lý RAG
app.post("/chat")(chat_endpoint)
app.get("/chat-history")(chat_history_endpoint)
