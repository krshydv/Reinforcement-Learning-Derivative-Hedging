import uuid
from fastapi import HTTPException
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import User, Role, Permission, UserRole, RolePermission
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import pwd_context

class UserService:
    async def create_user(self, payload: UserCreate) -> UserRead:
        async with AsyncSessionLocal() as session:
            existing = await session.execute(select(User).where(User.email == payload.email))
            if existing.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="User already exists")
            role = await session.execute(select(Role).where(Role.name == "user"))
            role_entry = role.scalar_one_or_none()
            if not role_entry:
                role_entry = Role(id=str(uuid.uuid4()), name="user")
                session.add(role_entry)
            permission = await session.execute(select(Permission).where(Permission.name == "access"))
            permission_entry = permission.scalar_one_or_none()
            if not permission_entry:
                permission_entry = Permission(id=str(uuid.uuid4()), name="access")
                session.add(permission_entry)
            session.add(RolePermission(role_id=role_entry.id, permission_id=permission_entry.id))
            user = User(id=str(uuid.uuid4()), email=payload.email, hashed_password=pwd_context.hash(payload.password), is_active=True)
            session.add(user)
            session.add(UserRole(user_id=user.id, role_id=role_entry.id))
            await session.commit()
            return UserRead(id=user.id, email=user.email, is_active=user.is_active)
