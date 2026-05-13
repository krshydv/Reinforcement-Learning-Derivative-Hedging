from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.db.models import User
from app.schemas.auth import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_str}/auth/token")

class AuthService:
    async def authenticate(self, email: str, password: str) -> Token | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            if not user or not pwd_context.verify(password, user.hashed_password):
                return None
            return Token(access_token=self._create_token(user.id), token_type="bearer")

    def _create_token(self, user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        return jwt.encode({"sub": user_id, "exp": expire}, settings.secret_key, algorithm=settings.jwt_algorithm)

async def get_current_user(token: str = oauth2_scheme) -> User:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    user_id = payload.get("sub")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one()
