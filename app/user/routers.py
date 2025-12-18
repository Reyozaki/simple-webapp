from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from sqlalchemy import select

from app.auth.dependencies import user_auth
from app.core.dependencies import DBSession
from app.core.exceptions import ForbiddenException, NotFoundException
from app.shared.models.base import Users
from app.shared.services.pdf_generation import render_pdf
from app.user.schemas import UserInfo

router = APIRouter()


@router.get("/profile/{user_id}")
async def user_profile(db: DBSession, user: user_auth, user_id: UUID) -> UserInfo:
    if not user:
        raise ForbiddenException()

    try:
        user_details = await db.get(Users, user_id)
        if not user_details:
            raise NotFoundException("Profile not found.")

        if "admin" in user.scopes:
            response = UserInfo(
                id=user_details.id,
                name=f"{user_details.fname} {user_details.lname}",
                role=user_details.role,
                address=user_details.address,
                contact=user_details.contact,
            )

        if "user" in user.scopes:
            response = UserInfo(
                name=f"{user_details.fname} {user_details.lname}",
                address=user_details.address,
                contact=user_details.contact,
            )

        return response

    except HTTPException as err:
        raise err


@router.get("/profile/pdf")
async def profile_pdf(user: user_auth, user_id: str, db: DBSession):
    if "admin" not in user.scopes and user.id != user_id:
        raise ForbiddenException

    uuid = UUID(user_id)
    stmt = select(Users).where(Users.id == uuid)
    result = await db.execute(stmt)
    user_info = result.scalars().first()

    pdf = await render_pdf("profile.html", {"user": user_info})

    return Response(
        pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=profile.pdf"},
    )
