from fastapi import APIRouter
from app.agent.collector import SystemMetricsCollector
from app.models.metrics import SystemMetrics, HealthResponse

router = APIRouter()

@router.get("/api/metrics", response_model=SystemMetrics)
async def get_metrics():
    collector = SystemMetricsCollector()
    return collector.collect_all()

@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok")
