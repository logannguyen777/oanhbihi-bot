import requests
import os
import time
import psycopg2
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ==========================
# 🚀 Cấu hình database
# ==========================
DB_CONFIG = {
    "dbname": "chatbot_db",
    "user": "chatbot_user",
    "password": "secretpassword",
    "host": "oanhbihi-postgres",  # Hoặc "localhost" nếu chạy ngoài Docker
    "port": "5432"
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# ==========================
# 🚀 Tạo bảng web_pages để lưu dữ liệu crawl
# ==========================
CREATE_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS web_pages (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE NOT NULL,
            title TEXT,
            content TEXT,
            file_path TEXT,
            last_crawled TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            embedding vector(1536)
        );
"""
cursor.execute(CREATE_TABLE_QUERY)
conn.commit()
print("✅ Bảng `web_pages` đã được tạo hoặc đã tồn tại.")

# ==========================
# 🚀 Cấu hình Crawler
# ==========================
BASE_URL = "https://fta.dainam.edu.vn"
VISITED_URLS = set()
DOWNLOAD_FOLDER = "downloads"

# Tạo thư mục lưu file
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# ==========================
# 🚀 Hàm tải file nếu có
# ==========================
def download_file(file_url):
    file_name = file_url.split("/")[-1]
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    
    try:
        response = requests.get(file_url, headers=HEADERS, stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"📂 Đã tải: {file_name}")
            return file_path
    except Exception as e:
        print(f"❌ Lỗi tải file {file_url}: {e}")
    
    return None

# ==========================
# 🚀 Hàm Crawl trang web
# ==========================
def crawl_page(url):
    if url in VISITED_URLS:
        return
    VISITED_URLS.add(url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Lỗi {response.status_code} - Bỏ qua: {url}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "Không có tiêu đề"
        
        # Lấy nội dung chính
        content = " ".join([p.text.strip() for p in soup.find_all("p")])

        # Lưu vào database
        cursor.execute(
            "INSERT INTO web_pages (url, title, content) VALUES (%s, %s, %s) ON CONFLICT (url) DO NOTHING;",
            (url, title, content)
        )
        conn.commit()
        print(f"✅ Đã lưu: {url}")

        # Tải xuống các file PDF, DOCX
        for link in soup.find_all("a", href=True):
            file_url = urljoin(url, link["href"])
            if file_url.endswith((".pdf", ".docx", ".xls", ".xlsx")):
                file_path = download_file(file_url)
                if file_path:
                    cursor.execute(
                        "UPDATE web_pages SET file_path = %s WHERE url = %s;",
                        (file_path, url)
                    )
                    conn.commit()

        # Crawl tiếp các link trong trang (chỉ link nội bộ)
        for a_tag in soup.find_all("a", href=True):
            next_url = urljoin(url, a_tag["href"])
            if urlparse(next_url).netloc == urlparse(BASE_URL).netloc:
                crawl_page(next_url)

    except Exception as e:
        print(f"❌ Lỗi crawl {url}: {e}")

# ==========================
# 🚀 Chạy crawler
# ==========================
if __name__ == "__main__":
    print(f"🚀 Bắt đầu crawl từ {BASE_URL}")
    crawl_page(BASE_URL)

    cursor.close()
    conn.close()
    print("🚀 Hoàn thành quá trình crawl và lưu dữ liệu!")
