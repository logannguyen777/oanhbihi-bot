#!/bin/bash

echo "🔹 Đợi PostgreSQL sẵn sàng..."
until pg_isready -h oanhbihi-postgres -p 5432 -U chatbot_user; do
    sleep 2
done

echo "✅ PostgreSQL đã sẵn sàng!"

echo "🔹 Cài đặt extension vector..."
PGPASSWORD=secretpassword psql -h oanhbihi-postgres -U chatbot_user -d chatbot_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
echo "✅ Extension vector đã được cài đặt!"

#echo "🚀 Chạy migrate database..."
#python migrate.py  # Nếu có script migrate thì thêm dòng này

#echo "🚀 Chạy crawler để thu thập dữ liệu..."
#python crawl_data.py

#echo "🚀 Chạy training để tạo embeddings..."
#python train_data.py

echo "🔹 Cấp quyền thư mục Alembic..."
chmod -R 777 /app/alembic
chmod -R 777 /app/alembic/versions
echo "✅ Đã cấp quyền ghi cho thư mục alembic."

echo "✅ Autogenerate Alembic revision..."
alembic revision --autogenerate -m "auto migrate" || echo "❌ Alembic autogenerate fail"

echo "✅ Alembic upgrade..."
alembic upgrade head || echo "❌ Alembic upgrade fail"

echo "🚀 Tạo Admin..."
python init_superadmin.py || echo "❌ Không tạo được admin!"



echo "🚀 Khởi động Backend..."
# Khởi động server FastAPI bằng Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
