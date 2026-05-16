from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.db.models import User, UserRole, RolePermission, Permission
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

async def _load_user(user_id: str) -> User:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return await _load_user(user_id)

async def get_user_permissions(user_id: str) -> set[str]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Permission.name)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .where(UserRole.user_id == user_id)
        )
        return set(result.scalars().all())

def require_permission(permission: str):
    async def checker(user: User = Depends(get_current_user)) -> User:
        permissions = await get_user_permissions(user.id)
        if permission not in permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return checker

async def authenticate_websocket_token(token: str | None) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return await _load_user(user_id)
