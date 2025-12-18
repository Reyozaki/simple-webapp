from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationOut(BaseModel, Generic[T]):
    page: int
    total_page: int
    items: list[T]

    class Config:
        from_attributes = True
