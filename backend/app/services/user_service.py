import uuid
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import User
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import pwd_context

class UserService:
    async def create_user(self, payload: UserCreate) -> UserRead:
        async with AsyncSessionLocal() as session:
            user = User(id=str(uuid.uuid4()), email=payload.email, hashed_password=pwd_context.hash(payload.password), is_active=True)
            session.add(user)
            await session.commit()
            return UserRead(id=user.id, email=user.email, is_active=user.is_active)
