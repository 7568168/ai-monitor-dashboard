# AI Monitor Dashboard - Deployment Guide

## Prerequisites

- **Python**: 3.14+
- **Node.js**: 18+
- **npm**: 9+

## Local Development

### 1. Clone
```bash
git clone https://github.com/7568168/ai-monitor-dashboard.git
cd ai-monitor-dashboard
```

### 2. Backend
```bash
cd backend
pip install -e .
python run.py
```
Server starts at `http://localhost:8089`

### 3. Frontend (dev)
```bash
cd frontend
npm install
npm run dev
```
Dev server at `http://localhost:5173`

## Production

### Option 1: Direct
```bash
cd frontend && npm install && npm run build
cp -r dist ../backend/frontend_dist
cd ../backend && python run.py
```

### Option 2: Docker Compose
```bash
docker compose up -d --build
```

### Option 3: Docker
```bash
docker build -t ai-monitor-dashboard .
docker run -d -p 8089:8089 --restart unless-stopped ai-monitor-dashboard
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 8089 | Server port |
| HOST | 0.0.0.0 | Bind address |
| LOG_LEVEL | INFO | Logging level |
| DIAGNOSIS_TIMEOUT | 300 | Diagnosis timeout (s) |

## Troubleshooting

- **Port in use**: `lsof -i :8089` then `kill -9 <PID>`
- **Build fails**: Clear node_modules and reinstall
- **Import errors**: `pip install -e .`
- **Docker fails**: `docker system prune -af` then rebuild
