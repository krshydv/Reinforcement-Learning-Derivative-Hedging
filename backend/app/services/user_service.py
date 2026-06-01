from __future__ import annotations

import uuid
from fastapi import HTTPException
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import User, Role, Permission, UserRole, RolePermission, AuditLog
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import pwd_context

class UserService:
    async def create_user(self, payload: UserCreate, actor_id: str | None = None) -> UserRead:
        async with AsyncSessionLocal() as session:
            email = payload.email.lower()
            if len(payload.password) < 8:
                raise HTTPException(status_code=400, detail="Password too short")
            existing = await session.execute(select(User).where(User.email == email))
            if existing.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="User already exists")
            role = await session.execute(select(Role).where(Role.name == "user"))
            role_entry = role.scalar_one_or_none()
            if not role_entry:
                role_entry = Role(name="user")
                session.add(role_entry)
            permission = await session.execute(select(Permission).where(Permission.name == "access"))
            permission_entry = permission.scalar_one_or_none()
            if not permission_entry:
                permission_entry = Permission(name="access")
                session.add(permission_entry)
            session.add(RolePermission(role_id=role_entry.id, permission_id=permission_entry.id))
            user = User(email=email, hashed_password=pwd_context.hash(payload.password), is_active=True)
            session.add(user)
            session.add(UserRole(user_id=user.id, role_id=role_entry.id))
            session.add(AuditLog(user_id=user.id, action="user:create" if actor_id is None else f"user:create:{actor_id}"))
            await session.commit()
            return UserRead(id=user.id, email=user.email, is_active=user.is_active)

    async def has_users(self) -> bool:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User.id))
            return result.scalar_one_or_none() is not None
