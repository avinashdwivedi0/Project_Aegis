from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
	email: EmailStr
	password: str
	name: str | None = None


class LoginRequest(BaseModel):
	email: EmailStr
	password: str


class UserRead(BaseModel):
	id: UUID
	email: EmailStr
	name: str | None
	created_at: datetime


class TokenResponse(BaseModel):
	user: UserRead
	access_token: str
	refresh_token: str
	token_type: str = "bearer"
