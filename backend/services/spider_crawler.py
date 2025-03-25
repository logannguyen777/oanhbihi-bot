import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
from routers.logs_ws import broadcast_log
from sqlalchemy import text
from database import SessionLocal

DOWNLOAD_FOLDER = "downloads"
ALLOWED_FILE_TYPES = [".pdf", ".doc", ".docx", ".txt"]

visited = set()

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def is_file_url(url):
    return any(url.lower().endswith(ext) for ext in ALLOWED_FILE_TYPES)

async def download_file(url):
    local_filename = url.split("/")[-1]
    save_path = os.path.join(DOWNLOAD_FOLDER, local_filename)

    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    try:
        r = requests.get(url, timeout=10)
        with open(save_path, "wb") as f:
            f.write(r.content)
        await broadcast_log(f"✅ Đã tải file: {local_filename}")
        return save_path
    except Exception as e:
        await broadcast_log(f"❌ Lỗi tải file {url}: {e}")
        return None

async def crawl_and_download_files(start_url, depth=1):
    global visited
    visited = set()

    async def crawl(url, level):
        if level > depth or url in visited:
            return
        visited.add(url)

        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            await broadcast_log(f"🌐 Crawled URL: {url}")

            # ✅ Lưu nội dung trang web vào DB
            body = soup.select_one("body")
            if body:
                text_content = body.get_text(separator="\n").strip()
                if text_content:
                    db = SessionLocal()
                    try:
                        db.execute(text("""
                            INSERT INTO web_pages (url, content)
                            VALUES (:url, :content)
                            ON CONFLICT (url) DO NOTHING
                        """), {"url": url, "content": text_content})
                        db.commit()
                        await broadcast_log(f"📝 Đã lưu nội dung trang: {url} ({len(text_content.split())} từ)")
                    finally:
                        db.close()

            # ✅ Tiếp tục xử lý các link trên trang
            for link in soup.find_all("a", href=True):
                href = link["href"]
                full_url = urljoin(url, href)

                if not is_valid_url(full_url):
                    continue

                if is_file_url(full_url):
                    await broadcast_log(f"📥 Đang tải file: {full_url}")
                    await download_file(full_url)
                elif urlparse(full_url).netloc == urlparse(start_url).netloc:
                    await crawl(full_url, level + 1)

        except Exception as e:
            await broadcast_log(f"⚠️ Lỗi crawl {url}: {e}")

    await crawl(start_url, 0)
