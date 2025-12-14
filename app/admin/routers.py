from fastapi import APIRouter

router = APIRouter(
    prefix="/admin", responses={404:{"description": "Not Found"}}
)
