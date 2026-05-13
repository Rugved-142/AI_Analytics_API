from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class APIKeyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class APIKeyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    revoked: bool
    created_at: datetime


class EventIngestRequest(BaseModel):
    user_id: int | None = None
    session_id: str
    event_type: str
    properties: dict[str, Any] = Field(default_factory=dict)


class EventResponse(BaseModel):
    id: int
    message: str


class TopPage(BaseModel):
    page: str
    count: int


class SummaryResponse(BaseModel):
    total_events: int
    unique_users: int
    top_pages: list[TopPage]
    pagination: Pagination


class TimeSeriesPoint(BaseModel):
    bucket: datetime
    count: int


class TimeSeriesResponse(BaseModel):
    granularity: str
    data: list[TimeSeriesPoint]
    pagination: Pagination


class FunnelStep(BaseModel):
    step: str
    users: int
    conversion_rate: float


class FunnelResponse(BaseModel):
    funnel: list[FunnelStep]
    pagination: Pagination


class HealthResponse(BaseModel):
    status: str
    checks: dict[str, str]
