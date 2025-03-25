from pydantic import BaseModel
from fastapi import Request
from openai import OpenAI
import json
import os
import psycopg2
from psycopg2.extras import Json
from pgvector.psycopg2 import register_vector
from bs4 import BeautifulSoup
import requests
from sqlalchemy.orm import Session
from models import CrawlConfig
from database import get_db
from routers.logs_ws import broadcast_log

# ============================
# 🚀 Khởi tạo pipeline RAG
# ============================

DB_CONFIG = {
    "dbname": "chatbot_db",
    "user": "chatbot_user",
    "password": "secretpassword",
    "host": "oanhbihi-postgres",
    "port": "5432"
}

client = None
conn = None
cursor = None
BOT_PERSONA = ""

async def init_rag_pipeline():
    global client, conn, cursor, BOT_PERSONA

    try:
        from services.config_service import get_config
        from database import get_db
        from sqlalchemy.orm import Session

        db: Session = next(get_db())
        api_key = get_config(db, "openai_key")
        BOT_PERSONA = get_config(db, "persona") or "Bạn là Oanh Bihi, 18 tuổi 🎀..."

        if api_key:
            from services.openai_client import get_openai_client
            client = get_openai_client(db)
            print("✅ OpenAI API Key hợp lệ")
            await broadcast_log("✅ OpenAI API Key hợp lệ")  # ✅ thay sio.emit
        else:
            print("⚠️ Không tìm thấy OpenAI API Key!")
            await broadcast_log("⚠️ Không tìm thấy OpenAI API Key!")
    except Exception as e:
        print(f"⚠️ Lỗi OpenAI: {e}")
        await broadcast_log(f"⚠️ Lỗi OpenAI: {e}")

    # Kết nối DB
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        register_vector(conn)

        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cursor.execute("""CREATE TABLE IF NOT EXISTS web_pages (...);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS chat_logs (...);""")
        conn.commit()

        crawl_data()
        train_data()
    except Exception as e:
        print(f"⚠️ Lỗi DB pipeline: {e}")
        await broadcast_log(f"⚠️ Lỗi DB pipeline: {e}")

# ============================
# 🔍 Crawl dữ liệu
# ============================

CRAWL_URL = "https://fta.dainam.edu.vn"

def crawl_data():
    if not conn or not cursor:
        print("⚠️ DB chưa sẵn sàng")
        return

    try:
        db: Session = next(get_db())
        config = db.query(CrawlConfig).first()
        if not config:
            print("⚠️ Không tìm thấy CrawlConfig")
            return

        urls = json.loads(config.urls or "[]")
        if not isinstance(urls, list):
            print("⚠️ CrawlConfig.urls không hợp lệ")
            return

        for url in urls:
            crawl_single_url(url)

    except Exception as e:
        print(f"⚠️ Lỗi crawl_data: {e}")

def crawl_single_url(url: str):
    try:
        print(f"🔎 Đang crawl: {url}")
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"⚠️ Không truy cập được {url}")
            return

        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("div.item")  # TODO: tuỳ chỉnh selector phù hợp

        data_to_insert = []
        for it in items:
            link = it.select_one("a")
            content = it.text.strip()
            item_url = link["href"].strip() if link else None
            if item_url:
                data_to_insert.append((item_url, content))

        for (u, c) in data_to_insert:
            cursor.execute("""
                INSERT INTO web_pages (url, content)
                VALUES (%s, %s)
                ON CONFLICT (url) DO NOTHING
            """, (u, c))

        conn.commit()
        print(f"✅ Đã crawl {len(data_to_insert)} nội dung từ {url}")
    except Exception as e:
        print(f"⚠️ Lỗi crawl từ {url}: {e}")

# ============================
# 🧠 Train embedding
# ============================

def train_data():
    if not conn or not cursor or not client:
        print("⚠️ Thiếu điều kiện train.")
        return

    try:
        cursor.execute("SELECT id, content FROM web_pages WHERE embedding IS NULL LIMIT 100;")
        rows = cursor.fetchall()

        for (page_id, content) in rows:
            try:
                embed_resp = client.embeddings.create(
                    input=content,
                    model="text-embedding-ada-002"
                )
                vector = embed_resp.data[0].embedding
                cursor.execute(
                    "UPDATE web_pages SET embedding = %s WHERE id = %s;",
                    (Json(vector), page_id)
                )
            except Exception as e:
                print(f"⚠️ Lỗi embedding {page_id}: {e}")

        conn.commit()
        print(f"✅ Đã train {len(rows)} rows.")
    except Exception as e:
        print(f"⚠️ Lỗi train_data: {e}")

# ============================
# 💬 Chat Endpoint
# ============================

class ChatRequest(BaseModel):
    input_text: str

async def chat_endpoint(request: ChatRequest):
    try:
        db: Session = next(get_db())
        api_key = get_config(db, "openai_key")
        persona = get_config(db, "persona") or "Bạn là Oanh Bihi, 18 tuổi 🎀..."
        model = get_config(db, "openai_model") or "gpt-3.5-turbo"

        if not api_key:
            return {"error": "⚠️ Thiếu OpenAI API Key"}

        client = OpenAI(api_key=api_key)
        conn = psycopg2.connect(
            dbname="chatbot_db",
            user="chatbot_user",
            password="secretpassword",
            host="oanhbihi-postgres",
            port="5432"
        )
        cursor = conn.cursor()
        register_vector(conn)

        # 🔎 Get embedding for user input
        embed_resp = client.embeddings.create(
            input=request.input_text,
            model="text-embedding-ada-002"
        )
        query_vector = embed_resp.data[0].embedding

        # 🔍 Query both web_pages and document_chunks
        cursor.execute("SELECT content FROM web_pages ORDER BY embedding <-> %s LIMIT 3;", (Json(query_vector),))
        web_results = cursor.fetchall()

        cursor.execute("SELECT text FROM document_chunks ORDER BY embedding <-> %s LIMIT 3;", (Json(query_vector),))
        doc_results = cursor.fetchall()

        context_parts = [r[0] for r in web_results] + [r[0] for r in doc_results]
        context = "\\n\\n".join(context_parts)

        # 💬 Chat completion
        messages = [
            {"role": "system", "content": f"{persona}\\n\\n{context}"},
            {"role": "user", "content": request.input_text}
        ]

        chat_resp = client.chat.completions.create(
            model=model,
            messages=messages
        )
        bot_response = chat_resp.choices[0].message.content

        # 💾 Optional: Save chat to DB if needed
        return {"response": bot_response}

    except Exception as e:
        print(f"⚠️ Lỗi chat: {e}")
        return {"error": str(e)}

# ============================
# 📜 Lịch sử chat
# ============================

async def chat_history_endpoint():
    try:
        cursor.execute("""
            SELECT user_message, bot_response, created_at
            FROM chat_logs
            ORDER BY created_at DESC
            LIMIT 50;
        """)
        logs = cursor.fetchall()
        return [
            {
                "user_message": row[0],
                "bot_response": row[1],
                "timestamp": row[2]
            } for row in logs
        ]
    except Exception as e:
        print(f"⚠️ Lỗi lịch sử chat: {e}")
        return {"error": str(e)}