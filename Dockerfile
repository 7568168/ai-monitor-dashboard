# Stage 1: Build frontend
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Build backend
FROM python:3.14-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY backend/pyproject.toml ./
RUN pip install --no-cache-dir .
COPY backend/app/ ./app/
COPY backend/run.py ./
COPY --from=frontend-build /app/frontend/dist ./frontend_dist
EXPOSE 8089
ENV PORT=8089 HOST=0.0.0.0
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 CMD curl -f http://localhost:8089/api/metrics || exit 1
CMD ["python", "run.py"]
