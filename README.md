# AI Monitor Dashboard

![Python 3.14+](https://img.shields.io/badge/Python-3.14+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![React 19](https://img.shields.io/badge/React-19-61dafb.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

AI-powered operations monitoring dashboard with real-time system metrics, intelligent diagnostics, and three switchable themes (Datadog/Vercel/Grafana).

## Features

- **Real-time Monitoring** - Live CPU, memory, disk, network, and process metrics with 3-second auto-refresh
- **AI Agent Diagnostics** - Intelligent 6-step diagnostic workflow for automated system health analysis
- **3 Themes** - Switch between Datadog (dark), Vercel (light), and Grafana (data-dense) themes
- **SSE Streaming** - Server-Sent Events for real-time diagnostic output
- **Alert Detection** - Automatic alert detection with one-click AI diagnosis

## Tech Stack

### Frontend
- React 19
- TypeScript
- Vite 6
- Recharts 2

### Backend
- FastAPI
- psutil
- Python 3.14

## Quick Start

### Backend
```bash
cd backend
pip install -e .
python run.py
```

### Frontend (Production Build)
```bash
cd frontend
npm install
npm run build
cp -r dist/* ../backend/frontend_dist/
```

Then start the backend server on port 8089.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/metrics` | System overview (CPU, memory, disk, network, processes) |
| GET | `/api/health` | Health check |
| POST | `/api/diagnose` | Start AI diagnostic workflow (SSE streaming) |
| GET | `/` | Frontend dashboard (production) |

## License

MIT
