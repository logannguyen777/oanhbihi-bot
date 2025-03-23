# File: backend/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Hệ thống
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Đặt đúng lại đường dẫn (KHÔNG có 'backend/' phía trước vì đã ở trong thư mục backend rồi)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./backend

COPY start.sh ./start.sh
RUN chmod +x ./start.sh

CMD ["./start.sh"]
