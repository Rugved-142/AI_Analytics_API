from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest

from app.api.schemas import HealthResponse

router = APIRouter(tags=["platform"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", checks={"database": "unknown", "redis": "unknown"})


@router.get("/metrics")
def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest().decode("utf-8"), media_type="text/plain; version=0.0.4")
