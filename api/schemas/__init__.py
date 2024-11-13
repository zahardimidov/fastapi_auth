from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str

    @field_validator("username", mode='before')
    def validate_username(cls, value: str):
        if len(value) < 6:
            raise HTTPException(
                status_code=400, detail='Username should include at least 6 symbols')
        return value

    @field_validator("password", mode='before')
    def validate_password(cls, value: str):
        if len(value) < 6:
            raise HTTPException(
                status_code=400, detail='Password should include at least 6 symbols')
        if not any([i.isdigit() for i in value]):
            raise HTTPException(
                status_code=400, detail="Password must include numbers")
        if not any([i.isalpha() for i in value]):
            raise HTTPException(
                status_code=400, detail="Password must include letters")
        return value


class UserResponse(BaseModel):
    username: str
    registered_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class DetailResponse(BaseModel):
    detail: str


class ErrorResponse(BaseModel):
    detail: str
