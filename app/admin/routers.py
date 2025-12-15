from fastapi import APIRouter

router = APIRouter(prefix="/admin", responses={404: {"description": "Not Found"}})


@router.get("/{user_id}")
async def profile(db: DBSession, user: user_auth) -> dict[str:Any]:
    """property"""
    pass
