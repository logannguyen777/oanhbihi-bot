#!/bin/bash

echo "🔹 Đợi PostgreSQL sẵn sàng..."
until pg_isready -h oanhbihi-postgres -p 5432 -U chatbot_user; do
    sleep 2
done

echo "✅ PostgreSQL đã sẵn sàng!"

echo "🔹 Cài extension vector..."
PGPASSWORD=secretpassword psql -h oanhbihi-postgres -U chatbot_user -d chatbot_db -c "CREATE EXTENSION IF NOT EXISTS vector;"

echo "🚀 Chạy migrate database..."
python -c "from db.init_db import init_db; init_db()" || echo "❌ Migrate lỗi!"

echo "🚀 Tạo tài khoản admin..."
python init_superadmin.py || echo "❌ Không tạo được admin!"

echo "🚀 Khởi động backend..."
uvicorn main:app --host 0.0.0.0 --port 8000
