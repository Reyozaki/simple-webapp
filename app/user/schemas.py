from uuid import UUID

from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    address: str
    contact: str
    role: str | None = None
    id: UUID | None = None
