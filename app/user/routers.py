from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.auth.dependencies import user_auth
from app.auth.services import identify_user
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


@router.get("/pdf")
async def profile_pdf(
    user: user_auth,
    db: DBSession,
    user_id: str = Query(...),
):
    user_info = await identify_user(db, user_id)
    if not user_info:
        raise NotFoundException("Error retrieving User Details")

    if "admin" not in user.scopes and user.id != user_id:
        raise ForbiddenException()

    user_details = await db.get(Users, user_info.id)

    pdf = await render_pdf("profile.html", {"user": user_details})

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=profile.pdf"},
    )
