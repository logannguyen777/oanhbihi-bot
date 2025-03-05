# Sử dụng Node.js chính thức
FROM node:18

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file package.json và package-lock.json trước
COPY package.json package-lock.json ./

# Cài đặt dependencies
RUN npm install

# Sao chép toàn bộ mã nguồn
COPY . .

# Build dự án (tùy chọn nếu bạn dùng Next.js production)
RUN npm run build

# Mở cổng 3000
EXPOSE 3000

# Lệnh khởi chạy container
CMD ["npm", "run", "dev"]
