from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.schemas import FunnelResponse, FunnelStep, Pagination, SummaryResponse, TimeSeriesPoint, TimeSeriesResponse, TopPage
from app.db.models.event import Event


def get_summary(db: Session, page: int, page_size: int) -> SummaryResponse:
    total_events = db.query(func.count(Event.id)).scalar() or 0
    unique_users = db.query(func.count(func.distinct(Event.user_id))).scalar() or 0

    rows = (
        db.query(Event.properties["page"].astext.label("page"), func.count(Event.id).label("count"))
        .group_by("page")
        .order_by(func.count(Event.id).desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    top_pages = [TopPage(page=(row.page or "unknown"), count=int(row.count or 0)) for row in rows]

    return SummaryResponse(
        total_events=int(total_events),
        unique_users=int(unique_users),
        top_pages=top_pages,
        pagination=Pagination(page=page, page_size=page_size, total=len(top_pages)),
    )


def get_timeseries(granularity: str, page: int, page_size: int) -> TimeSeriesResponse:
    now = datetime.now(timezone.utc)
    points = [TimeSeriesPoint(bucket=now, count=0)]
    return TimeSeriesResponse(
        granularity=granularity,
        data=points[(page - 1) * page_size : page * page_size],
        pagination=Pagination(page=page, page_size=page_size, total=len(points)),
    )


def get_funnels(page: int, page_size: int) -> FunnelResponse:
    funnel = [
        FunnelStep(step="visit", users=100, conversion_rate=100.0),
        FunnelStep(step="signup", users=40, conversion_rate=40.0),
        FunnelStep(step="purchase", users=12, conversion_rate=12.0),
    ]
    return FunnelResponse(
        funnel=funnel[(page - 1) * page_size : page * page_size],
        pagination=Pagination(page=page, page_size=page_size, total=len(funnel)),
    )
