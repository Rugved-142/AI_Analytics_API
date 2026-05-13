from sqlalchemy.orm import Session

from app.api.schemas import LoginRequest, TokenResponse, UserCreate
from app.core.errors import ProblemException
from app.core.security import create_access_token, create_refresh_token, decode_refresh_token, hash_password, verify_password
from app.db.models.user import User


def register_user(db: Session, payload: UserCreate) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise ProblemException(status_code=409, title="Conflict", detail="Email already registered")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, payload: LoginRequest) -> TokenResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise ProblemException(status_code=401, title="Unauthorized", detail="Invalid credentials")

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


def refresh_tokens(_: Session, refresh_token: str) -> TokenResponse:
    subject = decode_refresh_token(refresh_token)
    return TokenResponse(access_token=create_access_token(subject), refresh_token=create_refresh_token(subject))
