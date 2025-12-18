import math
from typing import Annotated, cast

from fastapi import Depends, Query
from sqlalchemy import asc, func, select

from app.admin.schemas import UserList
from app.core.dependencies import DBSession, Pagination, get_pagination
from app.shared.models.base import Users
from app.shared.schemas.responses import PaginationOut


async def get_user_list(
    db: DBSession,
    pagination: Annotated[Pagination, Depends(get_pagination)],
    filter_address: str | None = Query(None),
) -> tuple[PaginationOut[UserList], int]:
    """List User details"""

    stmt = select(Users).order_by(asc(Users.fname))
    # query condition for address filtering
    if filter_address:
        stmt = stmt.where(Users.address.ilike(f"%{filter_address}%"))

    # for total count
    total_stmt = select(func.count()).select_from(stmt.subquery())
    total_count = await db.execute(total_stmt)
    total = cast(int, total_count.scalar() or 0)  # noqa

    # applying pagination
    pag_stmt = stmt.offset(pagination.offset).limit(pagination.size)
    result = await db.execute(pag_stmt)
    results = result.scalars().all()

    user_list: list[UserList] = []
    for user in results:
        user_obj = UserList(
            id=user.id,
            name=user.fname + " " + user.lname,
            role=user.role,
            address=user.address,
            contact=user.contact,
        )
        user_list.append(user_obj)
    paginated_list: PaginationOut[UserList] = PaginationOut(
        page=pagination.page,
        total_page=math.ceil(total / pagination.size) if total > 0 else 0,
        items=user_list,
    )
    return paginated_list, total
