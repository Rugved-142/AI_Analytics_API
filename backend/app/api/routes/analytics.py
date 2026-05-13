from datetime import datetime, timezone

from fastapi import APIRouter, Query

from app.api.schemas import FunnelResponse, FunnelStep, SummaryResponse, TimeSeriesPoint, TimeSeriesResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=SummaryResponse)
def summary() -> SummaryResponse:
    return SummaryResponse(total_events=0, unique_users=0, top_pages=[])


@router.get("/timeseries", response_model=TimeSeriesResponse)
def timeseries(granularity: str = Query(default="1h", pattern="^(1m|5m|1h|1d)$")) -> TimeSeriesResponse:
    return TimeSeriesResponse(granularity=granularity, data=[TimeSeriesPoint(bucket=datetime.now(timezone.utc), count=0)])


@router.get("/funnels", response_model=FunnelResponse)
def funnels() -> FunnelResponse:
    return FunnelResponse(funnel=[FunnelStep(step="visit", users=0, conversion_rate=0.0)])
