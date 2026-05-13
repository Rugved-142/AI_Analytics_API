from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    session_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    properties: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="events")
