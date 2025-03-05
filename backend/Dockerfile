# Dockerfile cho Backend
FROM python:3.10

# Thiết lập thư mục làm việc trong container
WORKDIR /app/backend/

# Copy file yêu cầu cài đặt thư viện trước
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn backend vào container
COPY . .

RUN apt-get update && apt-get install -y postgresql-client

COPY start.sh /app/start.sh
# Đảm bảo script start.sh có thể chạy
RUN chmod +x /app/start.sh

# Chạy script start.sh để khởi động server
CMD ["/bin/bash", "/app/start.sh"]
