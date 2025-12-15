from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.shared.models.mixin import BaseModelMixin


class Base(DeclarativeBase):
    """Base class for overall connection and model mapping."""

    pass


class Users(Base, BaseModelMixin):
    __tablename__ = "users"

    fname: Mapped[str] = mapped_column(String(50), nullable=False)
    lname: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(20), nullable=False)
    contact: Mapped[str] = mapped_column(String(30), nullable=False)
