from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import psycopg2
from psycopg2.extras import Json
from pgvector.psycopg2 import register_vector
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from fastapi_socketio import SocketManager


from database import Base, engine
from routers import zalo, messenger, config, training, chat
#from routers.chat import router as chat_router
from models import MessengerConfig, BotPersona, CrawlConfig


app = FastAPI()

sio = SocketManager(app=app)


Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc dùng ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
# 🚀 CẤU HÌNH OPENAI
# =======================
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
client = None

if OPENAI_API_KEY:
    try:
        # Dùng OpenAI Client
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI API Key hợp lệ, chatbot sẵn sàng!")
    except Exception as e:
        print(f"⚠️ Lỗi OpenAI API Key: {e}. Container vẫn chạy nhưng không thể gọi OpenAI.")
else:
    print("⚠️ Không tìm thấy OpenAI API Key! Container vẫn chạy nhưng không gọi OpenAI.")

# =======================
# 🚀 KẾT NỐI POSTGRESQL & PGVECTOR
# =======================
DB_CONFIG = {
    "dbname": "chatbot_db",
    "user": "chatbot_user",
    "password": "secretpassword",
    "host": "oanhbihi-postgres",  # Tên service DB trong docker-compose
    "port": "5432"
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    register_vector(conn)

    # Tạo extension vector (nếu chưa có)
    cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector';")
    if not cursor.fetchone():
        cursor.execute("CREATE EXTENSION vector;")
        print("✅ Đã tạo extension vector!")
    conn.commit()

    # Tạo bảng web_pages nếu chưa có
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS web_pages (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE NOT NULL,
            title TEXT,
            content TEXT,
            file_path TEXT,
            last_crawled TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            embedding vector(1536)
        );
    """)
    conn.commit()

    # Tạo bảng chat_logs để lưu lịch sử chat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id SERIAL PRIMARY KEY,
            user_message TEXT,
            bot_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    print("✅ Kết nối PostgreSQL thành công!")
except Exception as e:
    print(f"⚠️ Lỗi kết nối PostgreSQL: {e}")
    conn, cursor = None, None

# =======================
# 🎀 OANH BIHI - PERSONAS
# =======================
BOT_PERSONA = """
Bạn là Oanh Bihi, 18 tuổi, giới tính nữ 🎀.
Bạn là nhân viên của Viện Công Nghệ Tài Chính - FTA - Trường Đại Học Đại Nam.
Bạn luôn sẵn sàng hỗ trợ sinh viên về tuyển sinh, học tập và lắng nghe tâm sự.
Trả lời thông minh, tinh tế, kèm emoji khi phù hợp.
"""

# =======================
# 🚀 Hàm crawl dữ liệu
# =======================
CRAWL_URL = "https://fta.dainam.edu.vn"  # Thay bằng URL thực tế

def crawl_data():
    """Crawl dữ liệu từ CRAWL_URL và lưu vào bảng web_pages."""
    if not conn or not cursor:
        print("⚠️ DB chưa sẵn sàng, không thể crawl.")
        return

    print(f"🔎 Đang crawl dữ liệu từ: {CRAWL_URL}")
    try:
        resp = requests.get(CRAWL_URL, timeout=10)
        if resp.status_code != 200:
            print(f"⚠️ Không thể truy cập trang, status_code = {resp.status_code}")
            return

        soup = BeautifulSoup(resp.text, "html.parser")

        # Ví dụ: crawl các thẻ <div class="item">, trong đó content = text
        items = soup.select("div.item")  # Cần thay selector phù hợp

        data_to_insert = []
        for it in items:
            link = it.select_one("a")
            content = it.text.strip()

            url = link["href"].strip() if link else None
            if not url:
                continue

            data_to_insert.append((url, content))

        if not data_to_insert:
            print("⚠️ Không tìm thấy dữ liệu để crawl.")
            return

        # Lưu vào DB, ON CONFLICT(url) DO NOTHING
        for (url, content) in data_to_insert:
            try:
                cursor.execute("""
                    INSERT INTO web_pages (url, content) 
                    VALUES (%s, %s)
                    ON CONFLICT (url) DO NOTHING
                """, (url, content))
            except Exception as e:
                print(f"⚠️ Lỗi insert data: {e}")

        conn.commit()
        print(f"✅ Đã crawl và lưu {len(data_to_insert)} dòng vào web_pages!")
    except Exception as e:
        print(f"⚠️ Lỗi crawl_data: {e}")

# =======================
# 🚀 Hàm train embedding
# =======================
def train_data():
    """Tạo embedding cho các row chưa có embedding trong web_pages."""
    if not client or not client.api_key:
        print("⚠️ Chưa có API Key OpenAI, không thể train.")
        return
    if not conn or not cursor:
        print("⚠️ DB chưa sẵn sàng, không thể train.")
        return

    try:
        cursor.execute("SELECT id, content FROM web_pages WHERE embedding IS NULL LIMIT 100;")
        rows = cursor.fetchall()
        if not rows:
            print("✅ Không có dữ liệu mới để embedding.")
            return

        for (page_id, content) in rows:
            try:
                embed_resp = client.embeddings.create(
                    input=content,
                    model="text-embedding-ada-002"
                )
                vector = embed_resp.data[0].embedding

                # Cập nhật embedding
                cursor.execute(
                    "UPDATE web_pages SET embedding = %s WHERE id = %s;",
                    (Json(vector), page_id)
                )
            except Exception as e:
                print(f"⚠️ Lỗi embedding ID={page_id}: {e}")

        conn.commit()
        print(f"✅ Đã train embedding cho {len(rows)} row!")
    except Exception as e:
        print(f"⚠️ Lỗi train_data: {e}")

# =======================
# 🚀 Tự động chạy crawl + train khi container khởi động
# =======================
def init_data_pipeline():
    crawl_data()  # Crawl data
    train_data()  # Train embedding

if conn and cursor and client and client.api_key:
    init_data_pipeline()

# =======================
# 🚀 API CHO CHAT
# =======================
class ChatRequest(BaseModel):
    input_text: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Dùng RAG (Retrieval + GPT-3.5-turbo):
    1) Tạo embedding cho câu hỏi
    2) Tìm TOP 3 kết quả trong web_pages
    3) Gộp context + BOT_PERSONA + câu hỏi vào GPT-3.5-turbo
    4) Trả về câu trả lời + lưu lịch sử
    """
    input_text = request.input_text

    # Kiểm tra OpenAI Client
    if not client or not client.api_key:
        return {"error": "⚠️ OpenAI API Key thiếu hoặc không hợp lệ"}

    # Kiểm tra DB
    if not conn or not cursor:
        return {"error": "⚠️ DB chưa sẵn sàng"}

    try:
        # 1) Tạo embedding cho câu hỏi
        embed_resp = client.embeddings.create(
            input=input_text,
            model="text-embedding-ada-002"
        )
        query_vector = embed_resp.data[0].embedding

        # 2) Tìm top 3 nội dung liên quan trong DB
        cursor.execute("""
            SELECT content
            FROM web_pages
            ORDER BY embedding <-> %s
            LIMIT 3
        """, (Json(query_vector),))
        fetched_rows = cursor.fetchall()

        if fetched_rows:
            context_texts = [row[0] for row in fetched_rows if row[0]]
            context = "\n\n".join(context_texts)
        else:
            context = "No relevant context found in the database."

        # 3) Tạo prompt gửi GPT (gpt-3.5-turbo)
        messages = [
            {
                "role": "system",
                "content": (
                    f"{BOT_PERSONA}\n\n"
                    f"Dưới đây là context lấy từ cơ sở dữ liệu:\n\n{context}\n\n"
                    "Hãy sử dụng thông tin này (nếu phù hợp) để trả lời người dùng một cách tự nhiên."
                )
            },
            {
                "role": "user",
                "content": input_text
            }
        ]

        chat_resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_response = chat_resp.choices[0].message.content

        # 4) Lưu lịch sử chat
        cursor.execute("""
            INSERT INTO chat_logs (user_message, bot_response)
            VALUES (%s, %s)
        """, (input_text, bot_response))
        conn.commit()

        return {"response": bot_response}

    except Exception as e:
        print(f"⚠️ Lỗi xử lý chatbot: {e}")
        return {"error": f"Đã xảy ra lỗi: {e}"}


# =======================
# 🚀 Kết nối router
# =======================


app.include_router(chat.router)
app.include_router(config.router)
app.include_router(messenger.router)
app.include_router(zalo.router)
app.include_router(training.router)

# =======================
# 🚀 API XEM LỊCH SỬ CHAT
# =======================
@app.get("/chat-history")
async def get_chat_history():
    """Trả về lịch sử chat (mới nhất trước)."""
    if not conn or not cursor:
        return {"error": "⚠️ DB chưa sẵn sàng"}

    try:
        cursor.execute("""
            SELECT user_message, bot_response, created_at
            FROM chat_logs
            ORDER BY created_at DESC
            LIMIT 50
        """)
        logs = cursor.fetchall()
        history = [
            {
                "user_message": row[0],
                "bot_response": row[1],
                "timestamp": row[2]
            }
            for row in logs
        ]
        return history
    except Exception as e:
        print(f"⚠️ Lỗi lấy lịch sử chat: {e}")
        return {"error": f"Không thể lấy lịch sử chat: {e}"}

