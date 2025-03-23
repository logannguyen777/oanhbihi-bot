# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Cài dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 👇 Fix đúng chỗ copy code:
COPY . .

# Chạy start script
COPY start.sh ./start.sh
RUN chmod +x ./start.sh

CMD ["./start.sh"]
