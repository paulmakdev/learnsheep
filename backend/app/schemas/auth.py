from pydantic import BaseModel, EmailStr
from pydantic_settings import SettingsConfigDict

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class UserResponse(BaseModel):

    model_config = SettingsConfigDict(from_attributes=True)

    id: str
    email: str
    role: str
    display_name: str | None
