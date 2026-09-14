from datetime import timedelta

from app.core.config import settings
from app.core.security import create_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schemas import LoginRequest, RegisterRequest, TokenResponse, UserRead


class AuthService:
	def __init__(self, repository: UserRepository) -> None:
		self.repository = repository

	async def register(self, request: RegisterRequest) -> TokenResponse:
		if await self.repository.get_by_email(request.email):
			raise ValueError("email already registered")
		user = await self.repository.create(
			User(email=request.email, password_hash=hash_password(request.password), name=request.name)
		)
		return self._tokens(user)

	async def login(self, request: LoginRequest) -> TokenResponse:
		user = await self.repository.get_by_email(request.email)
		if user is None or not verify_password(request.password, user.password_hash):
			raise ValueError("invalid credentials")
		return self._tokens(user)

	def _tokens(self, user: User) -> TokenResponse:
		return TokenResponse(
			user=UserRead.model_validate(user, from_attributes=True),
			access_token=create_token(
				user.id,
				"access",
				timedelta(minutes=settings.access_token_expire_minutes),
			),
			refresh_token=create_token(
				user.id,
				"refresh",
				timedelta(days=settings.refresh_token_expire_days),
			),
		)
