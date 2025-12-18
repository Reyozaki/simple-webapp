from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy import select

from app.admin.schemas import UserDetails, UserList
from app.admin.services import get_user_list
from app.auth.dependencies import user_auth
from app.auth.exceptions import NotAuthorizedException
from app.core.dependencies import DBSession, Pagination, get_pagination
from app.core.exceptions import NotFoundException
from app.core.utils import hash_password
from app.shared.models.base import Users
from app.shared.schemas.responses import PaginationOut
from app.shared.services.pdf_generation import render_pdf

router = APIRouter()


@router.get("/users")
async def view_users(
    db: DBSession,
    user: user_auth,
    pagination: Annotated[Pagination, Depends(get_pagination)],
    filter_address: str | None = Query(None),
) -> tuple[PaginationOut[UserList], dict[str, int]]:
    """View all User"""

    if "admin" not in user.scopes:
        raise NotAuthorizedException()

    try:
        user_details, total = await get_user_list(db, pagination, filter_address)
        return user_details, {"total": total}

    except HTTPException as err:
        raise err


@router.get("/users/pdf")
async def generate_users_pdf(db: DBSession, user: user_auth):
    if "admin" not in user.scopes:
        raise NotAuthorizedException()
    try:
        query = await db.execute(select(Users))
        users = query.scalars().all()

        pdf_bytes = await render_pdf("users.html", {"users": users})

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=users.pdf"},
        )

    except HTTPException as err:
        raise err


@router.post("/create-user")
async def create_user(
    db: DBSession,
    user: user_auth,
    user_details: UserDetails,
) -> dict[str, str]:
    """Create a user with form data"""

    if "admin" not in user.scopes:
        raise NotAuthorizedException()

    try:
        hashed_password = await hash_password(user_details.password)
        new_user = Users(
            fname=user_details.fname,
            lname=user_details.lname,
            role=user_details.role,
            address=user_details.address,
            contact=user_details.contact,
            username=user_details.username,
            password=hashed_password,
        )
        db.add(new_user)
        await db.commit()

        return {"message": f"User {user_details.username} successfully created."}

    except HTTPException as err:
        raise err


@router.patch("/update-user")
async def update_user(
    db: DBSession,
    user: user_auth,
    user_data: UserDetails,
    user_id: str = Query(...),
) -> dict[str, str]:
    """Update selected user"""

    if "admin" not in user.scopes:
        raise NotAuthorizedException()

    try:
        existing_user = await db.get(Users, user_id)
        if not existing_user:
            raise NotFoundException("User not found.")

        if user_data.password:
            user_data.password = await hash_password(user_data.password)
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(existing_user, field, value)
        await db.commit()
        await db.refresh(existing_user)
        return {"message": f"Updated user {existing_user.username} successfully."}

    except HTTPException as err:
        raise err


@router.delete("/delete-user")
async def delete_user(
    db: DBSession,
    user: user_auth,
    user_id: str = Query(...),
) -> dict[str, str]:
    """Update selected user"""

    if "admin" not in user.scopes:
        raise NotAuthorizedException()

    try:
        existing_user = await db.get(Users, user_id)
        if not existing_user:
            raise NotFoundException("User not found.")
        else:
            await db.delete(existing_user)
            await db.commit()

        return {"message": "User Deleted."}

    except HTTPException as err:
        raise err
