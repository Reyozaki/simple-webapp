from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={"admin": "Admin access", "user": "User access"},
    scheme_name="UserToken",
)


async def hash_password(password: str) -> str:
    return str(bcrypt_context.hash(password))
