from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(payload: UserCreate) -> UserRead:
    return await UserService().create_user(payload)

@router.get("/me", response_model=UserRead)
async def get_me(user=Depends(get_current_user)) -> UserRead:
    return user
