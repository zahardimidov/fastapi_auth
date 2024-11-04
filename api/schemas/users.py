from pydantic import BaseModel
from datetime import datetime


### REQUESTS

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

### RESPONSES

class UserResponse(BaseModel):
    username: str
    registered_at: datetime

class LoginResponse(BaseModel):
    access_token: str
    jwt_token: str = 'bearer'