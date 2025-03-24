# Stage: Dev runtime with Vite
FROM node:18-alpine

WORKDIR /app

# Copy and install dependencies
COPY package*.json ./
RUN npm install

# Copy toàn bộ source code vào container
COPY . .

# Expose Vite dev port
EXPOSE 3000

# Start Vite dev server (bind all interfaces)
CMD ["npm", "run", "dev", "--", "--host"]
