from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    token = await AuthService().authenticate(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token
