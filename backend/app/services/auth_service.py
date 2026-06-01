from __future__ import annotations

from datetime import datetime, timedelta
import uuid
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.db.models import User, UserRole, RolePermission, Permission, RefreshToken
from app.schemas.auth import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_str}/auth/token", auto_error=False)

class AuthService:
    async def authenticate(self, email: str, password: str) -> Token | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            if not user or not pwd_context.verify(password, user.hashed_password):
                return None
            access_token, access_expires = self._create_access_token(user.id)
            refresh_token = await self._create_refresh_token(session, user.id)
            await session.commit()
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=int(access_expires.timestamp()),
            )

    def _create_access_token(self, user_id: str) -> tuple[str, datetime]:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        token = jwt.encode(
            {"sub": user_id, "exp": expire, "type": "access"},
            settings.secret_key,
            algorithm=settings.jwt_algorithm,
        )
        return token, expire

    async def _create_refresh_token(self, session, user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        jti = str(uuid.uuid4())
        token = jwt.encode(
            {"sub": user_id, "exp": expire, "jti": jti, "type": "refresh"},
            settings.secret_key,
            algorithm=settings.jwt_algorithm,
        )
        session.add(
            RefreshToken(
                user_id=user_id,
                token_jti=jti,
                expires_at=expire,
            )
        )
        return token

    async def refresh_access(self, refresh_token: str) -> Token:
        payload = self._decode_token(refresh_token, expected_type="refresh")
        user_id = payload.get("sub")
        jti = payload.get("jti")
        if not user_id or not jti:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(RefreshToken).where(RefreshToken.token_jti == jti))
            stored = result.scalar_one_or_none()
            if not stored or stored.revoked_at is not None or stored.expires_at < datetime.utcnow():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            stored.revoked_at = datetime.utcnow()
            access_token, access_expires = self._create_access_token(user_id)
            new_refresh = await self._create_refresh_token(session, user_id)
            await session.commit()
            return Token(
                access_token=access_token,
                refresh_token=new_refresh,
                token_type="bearer",
                expires_in=int(access_expires.timestamp()),
            )

    async def revoke_refresh(self, refresh_token: str) -> None:
        payload = self._decode_token(refresh_token, expected_type="refresh")
        jti = payload.get("jti")
        if not jti:
            return
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(RefreshToken).where(RefreshToken.token_jti == jti))
            stored = result.scalar_one_or_none()
            if stored and stored.revoked_at is None:
                stored.revoked_at = datetime.utcnow()
                await session.commit()

    def _decode_token(self, token: str, expected_type: str) -> dict:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        if payload.get("type") != expected_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return payload

async def _load_user(user_id: str) -> User:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user

async def get_current_user(token: str | None = Depends(oauth2_scheme)) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return await _load_user(user_id)

async def get_optional_user(token: str | None = Depends(oauth2_scheme)) -> User | None:
    if not token:
        return None
    return await get_current_user(token)

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
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return await _load_user(user_id)
