from typing import Annotated

from fastapi import Security
from fastapi.security import (
    SecurityScopes,
)
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from app.auth.exceptions import NotAuthorizedException
from app.auth.schemas import CurrentUser
from app.auth.services import get_user_info
from app.config.settings import settings
from app.core.dependencies import DBSession
from app.core.exceptions import ForbiddenException
from app.core.utils import oauth2_scheme

ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Security(oauth2_scheme)],
    db: DBSession,
) -> CurrentUser:
    """Check"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise NotAuthorizedException("Not Authorized.")

    except JWTError as err:
        raise err
    except ExpiredSignatureError:
        raise

    user = await get_user_info(db, user_id)
    user_scopes = [user.role]
    for scope in security_scopes.scopes:
        if scope not in user_scopes:
            raise ForbiddenException("Forbidden")

    current_user = CurrentUser(id=user_id, scopes=user_scopes, token=token)
    return current_user


user_auth = Annotated[dict, Security(get_current_user)]
