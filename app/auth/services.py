from datetime import datetime, timedelta
from typing import Annotated, Any

from fastapi import Security
from jose import jwt
from sqlalchemy import delete, select
from sqlalchemy.orm import undefer

from app.auth.schemas import UserOut
from app.config.settings import settings
from app.core.dependencies import DBSession
from app.core.utils import bcrypt_context, oauth2_scheme
from app.shared.models.base import RefreshToken, Users

# jwt encoding config
ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key


async def authenticate_user(
    username: str, password: str, db: DBSession
) -> UserOut | bool:
    stmt = (
        select(Users).options(undefer(Users.password)).where(Users.username == username)
    )
    result = await db.execute(stmt)
    user_info = result.scalar_one_or_none()
    if not user_info:
        return False
    if not bcrypt_context.verify(password, user_info.password):
        return False

    return UserOut(
        id=str(user_info.id),
        role=user_info.role,
    )


async def create_access_token(
    data: dict[str, Any], expires_in: timedelta | None = None
) -> str:
    to_encode = data.copy()
    now = datetime.now()

    expire = now + expires_in if expires_in else now + timedelta(minutes=10)

    to_encode.update(
        {
            "exp": expire,
        }
    )
    token: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def get_user_info(db: DBSession, user_id: str) -> UserOut | bool:
    stmt = select(Users).where(Users.id == user_id)
    result = await db.execute(stmt)
    user_info = result.scalar_one()
    if not user_info:
        return False

    return UserOut(
        id=str(user_info.id),
        role=user_info.role,
    )


async def logout_user(
    token: Annotated[str, Security(oauth2_scheme)],
    db: DBSession,
) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        user_id: str = payload.get("sub")

        stmt = delete(RefreshToken).where(RefreshToken.user_id == user_id)
        await db.execute(stmt)
        await db.commit()
        return True

    except Exception as err:
        await db.rollback()
        raise err
