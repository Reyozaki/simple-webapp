import asyncio
import os
import sys

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config.database import async_engine
from app.core.dependencies import DBSession
from app.shared.models.base import Users

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_admin(db: DBSession) -> None:
    admin = Users(
        fname="admin",
        lname="admin",
        role="admin",
        address="Kathmandu",
        contact="admin@email.com",
        username="admin",
        password=bcrypt_context.hash("password"),
    )
    db.add(admin)
    await db.flush()
    await db.commit()
    print("Added admin to the database.\nUsername: admin\nPassword: password")


async def main() -> None:
    async with AsyncSession(async_engine) as db:
        await create_admin(db)


if __name__ == "__main__":
    asyncio.run(main())
