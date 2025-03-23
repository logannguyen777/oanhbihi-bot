import psycopg2
import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", None))
import numpy as np
from pgvector.psycopg2 import register_vector
import openai

# ==========================
# 🚀 Cấu hình database
# ==========================
DB_CONFIG = {
    "dbname": "chatbot_db",
    "user": "chatbot_user",
    "password": "secretpassword",
    "host": "oanhbihi-postgres",
    "port": "5432"
}

# Kết nối DB
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()
register_vector(conn)

# ==========================
# 🚀 Cấu hình OpenAI API
# ==========================
#openai.api_key = os.environ.get("OPENAI_API_KEY", None)

# Kiểm tra nhanh xem API key có hợp lệ không (tuỳ chọn)
try:
    if openai.api_key:
        #_ = openai.Engine.list()
        # T ODO: The resource 'Engine' has been deprecated
        # _ = openai.Engine.list()
        print("✅ OpenAI API Key hợp lệ, sẵn sàng embedding!")
    else:
        print("⚠️ Chưa có OpenAI API Key, không thể train.")
except Exception as e:
    print(f"⚠️ Lỗi OpenAI API Key: {e}")

# ==========================
# 🚀 Hàm lấy dữ liệu chưa embedding
# ==========================
def get_unembedded_data():
    cursor.execute("SELECT id, content FROM web_pages WHERE embedding IS NULL LIMIT 100;")
    return cursor.fetchall()

# ==========================
# 🚀 Hàm tạo embedding với OpenAI (API mới)
# ==========================
def generate_embedding(text: str):
    """
    Gọi OpenAI Embedding API.
    """
    #response = openai.Embedding.create(
    #    input=text,
    #    model="text-embedding-ada-002"
    #)
    response = client.embeddings.create(input=text,
    model="text-embedding-ada-002")
    # Lấy vector embedding từ response
    #return response["data"][0]["embedding"]
    return response.data[0].embedding

# ==========================
# 🚀 Hàm cập nhật vector vào DB
# ==========================
def update_embedding():
    data = get_unembedded_data()

    if not data:
        print("✅ Không có dữ liệu cần embedding.")
        return

    for record in data:
        page_id, text = record
        print(f"📌 Đang embedding: ID {page_id}...")

        # Tạo vector embedding
        try:
            vector = generate_embedding(text)
        except Exception as e:
            print(f"⚠️ Lỗi khi tạo embedding cho ID={page_id}: {e}")
            continue

        # Lưu vào PostgreSQL
        cursor.execute(
            "UPDATE web_pages SET embedding = %s WHERE id = %s;",
            (np.array(vector).tolist(), page_id)
        )

    conn.commit()
    print(f"✅ Đã embedding {len(data)} mẫu dữ liệu!")

# ==========================
# 🚀 Chạy Train
# ==========================
if __name__ == "__main__":
    # Nếu chưa có API Key, dừng luôn
    if not client or not client.api_key:
        print("⚠️ Không thể train do thiếu OpenAI API Key.")
    else:
        update_embedding()

    cursor.close()
    conn.close()
    print("🚀 Hoàn thành quá trình train dữ liệu!")
