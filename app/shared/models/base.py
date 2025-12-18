import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.shared.models.mixin import BaseModelMixin


class Base(DeclarativeBase):
    """Base class for overall connection and model mapping."""

    pass


class Users(Base, BaseModelMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False, deferred=True)
    role: Mapped[str] = mapped_column(String, default="user", nullable=False)
    fname: Mapped[str] = mapped_column(String(50), nullable=False)
    lname: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(20), nullable=False)
    contact: Mapped[str] = mapped_column(String(30), nullable=False)


class RefreshToken(Base, BaseModelMixin):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
