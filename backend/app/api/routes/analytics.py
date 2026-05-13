from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.schemas import FunnelResponse, SummaryResponse, TimeSeriesResponse
from app.db.session import get_db
from app.services.analytics import get_funnels, get_summary, get_timeseries

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=SummaryResponse)
def summary(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> SummaryResponse:
    return get_summary(db, page, page_size)


@router.get("/timeseries", response_model=TimeSeriesResponse)
def timeseries(
    granularity: str = Query(default="1h", pattern="^(1m|5m|1h|1d)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=100, ge=1, le=1000),
) -> TimeSeriesResponse:
    return get_timeseries(granularity, page, page_size)


@router.get("/funnels", response_model=FunnelResponse)
def funnels(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> FunnelResponse:
    return get_funnels(page, page_size)
