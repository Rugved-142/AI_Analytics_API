from fastapi import APIRouter

from app.api.schemas import LoginRequest, RefreshRequest, TokenResponse, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(payload: UserCreate) -> UserRead:
    return UserRead(id=1, email=payload.email, created_at="2025-01-01T00:00:00Z")


@router.post("/login", response_model=TokenResponse)
def login(_: LoginRequest) -> TokenResponse:
    return TokenResponse(access_token="access", refresh_token="refresh")


@router.post("/refresh", response_model=TokenResponse)
def refresh(_: RefreshRequest) -> TokenResponse:
    return TokenResponse(access_token="new-access", refresh_token="new-refresh")
