from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
    user_id: UUID


class UserOut(BaseModel):
    id: str
    role: str


class CurrentUser(BaseModel):
    id: str
    scopes: list[str]
    token: str
