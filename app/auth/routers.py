from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.schemas import Token
from app.auth.services import authenticate_user, create_access_token, logout_user
from app.core.dependencies import DBSession
from app.core.utils import oauth2_scheme

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTE = 20


@router.post("/token")
async def access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DBSession
) -> Token:
    """Login token"""
    try:
        user = await authenticate_user(form_data.username, form_data.password, db)
        if user:
            user_id = user.id
            user_role = "admin" if user.role == "admin" else "user"

        access_token = await create_access_token(
            data={"sub": str(user_id), "scope": user_role},
            expires_in=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE),
        )

        return Token(access_token=access_token, token_type="bearer", user_id=user_id)

    except HTTPException as err:
        raise err


@router.post("/logout")
async def logout(db: DBSession, token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    await logout_user(token, db)
    return {"message": "Logged Out"}
