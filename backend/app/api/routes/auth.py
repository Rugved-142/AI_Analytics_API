from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import LoginRequest, RefreshRequest, TokenResponse, UserCreate, UserRead
from app.db.session import get_db
from app.services.auth import login_user, refresh_tokens, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    return UserRead.model_validate(register_user(db, payload))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return login_user(db, payload)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return refresh_tokens(db, payload.refresh_token)
