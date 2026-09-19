# ==========================================
# Stage 1: Build Frontend Single Page App
# ==========================================
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --prefer-offline || npm install
COPY . .
RUN npm run build

# ==========================================
# Stage 2: Python FastAPI Production Server
# ==========================================
FROM python:3.12-slim
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=3000

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY backend/ ./backend/
COPY host.py ./

# Copy compiled frontend from Stage 1
COPY --from=frontend-builder /app/dist ./dist

# Expose server port
EXPOSE 3000

# Start FastAPI server
CMD uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-3000}
