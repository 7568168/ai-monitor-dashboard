from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.agent.orchestrator import DiagnosisOrchestrator
from app.models.metrics import DiagnosisRequest
import json

router = APIRouter()

@router.post("/api/diagnose")
async def diagnose(request: DiagnosisRequest):
    orchestrator = DiagnosisOrchestrator()
    async def event_generator():
        async for event in orchestrator.run_diagnosis(request):
            yield f"data: {json.dumps(event)}\n\n"
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
    )
