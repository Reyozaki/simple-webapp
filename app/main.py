from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.admin.routers import router as admin_router
from app.auth.routers import router as auth_router
from app.user.routers import router as user_router

app = FastAPI(title="webapp")

app.include_router(auth_router, prefix="/auth")
app.include_router(admin_router, prefix="/admin")
app.include_router(user_router, prefix="/user")

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "healthy"}
