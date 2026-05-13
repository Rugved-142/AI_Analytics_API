from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from app.api.schemas import FunnelResponse, SummaryResponse, TimeSeriesResponse
from app.core.config import get_settings
from app.db.session import get_db
from app.services.analytics import get_funnels, get_summary, get_timeseries
from app.services.cache import get_or_set_json
from app.services.rate_limit import enforce_rate_limit

router = APIRouter(prefix="/analytics", tags=["analytics"])
settings = get_settings()


def _as_summary(value: dict) -> SummaryResponse:
    return SummaryResponse.model_validate(value)


def _as_timeseries(value: dict) -> TimeSeriesResponse:
    return TimeSeriesResponse.model_validate(value)


def _as_funnels(value: dict) -> FunnelResponse:
    return FunnelResponse.model_validate(value)


@router.get("/summary", response_model=SummaryResponse)
def summary(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    x_api_key: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> SummaryResponse:
    enforce_rate_limit(x_api_key or "")
    key = f"analytics:summary:{page}:{page_size}"
    value = get_or_set_json(key, settings.redis_cache_ttl_seconds, lambda: get_summary(db, page, page_size).model_dump(mode="json"))
    return _as_summary(value)


@router.get("/timeseries", response_model=TimeSeriesResponse)
def timeseries(
    granularity: str = Query(default="1h", pattern="^(1m|5m|1h|1d)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=100, ge=1, le=1000),
    x_api_key: str | None = Header(default=None),
) -> TimeSeriesResponse:
    enforce_rate_limit(x_api_key or "")
    key = f"analytics:timeseries:{granularity}:{page}:{page_size}"
    value = get_or_set_json(key, settings.redis_cache_ttl_seconds, lambda: get_timeseries(granularity, page, page_size).model_dump(mode="json"))
    return _as_timeseries(value)


@router.get("/funnels", response_model=FunnelResponse)
def funnels(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    x_api_key: str | None = Header(default=None),
) -> FunnelResponse:
    enforce_rate_limit(x_api_key or "")
    key = f"analytics:funnels:{page}:{page_size}"
    value = get_or_set_json(key, settings.redis_cache_ttl_seconds, lambda: get_funnels(page, page_size).model_dump(mode="json"))
    return _as_funnels(value)
