from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService
from app.services.auth_service import get_optional_user, require_permission

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(payload: UserCreate, user=Depends(get_optional_user)) -> UserRead:
    if user:
        await require_permission("user:create")(user)
        return await UserService().create_user(payload, actor_id=user.id)
    has_users = await UserService().has_users()
    if has_users:
        raise HTTPException(status_code=401, detail="Authentication required")
    return await UserService().create_user(payload)

@router.get("/me", response_model=UserRead)
async def get_me(user=Depends(require_permission("access"))) -> UserRead:
    return user
