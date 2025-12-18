from uuid import UUID

from pydantic import BaseModel


class UserList(BaseModel):
    id: UUID
    name: str
    role: str
    address: str
    contact: str


class UserDetails(BaseModel):
    fname: str | None = None
    lname: str | None = None
    role: str | None = None
    address: str | None = None
    contact: str | None = None
    username: str | None = None
    password: str | None = None
