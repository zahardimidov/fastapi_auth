
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.schemas import *
from database.models import User
from database.requests import create_user, get_user
from ext import create_jwt_token, pwd_context, verify_jwt_token

router = APIRouter(prefix='/auth', tags=['Авторизация'])
auth_scheme = HTTPBearer()


@router.post("/register", response_model=DetailResponse)
async def register_user(username: str, password: str):
    if await get_user(username=username):
        raise HTTPException(
            status_code=400, detail='This username is already taken')

    await create_user(username=username, password=password)

    return DetailResponse(detail='Successfully registered')


@router.post("/login", response_model=LoginResponse)
async def login(username: str, password: str):
    user = await get_user(username)  # Получите пользователя из базы данных
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(password, user.password)

    if not is_password_correct:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt_token({"sub": user.username})
    return LoginResponse(access_token=jwt_token)


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    decoded_data = verify_jwt_token(token.credentials)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = await get_user(decoded_data["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user


@router.get("/me", response_model=UserResponse)
async def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user