from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
	token: str = Depends(oauth2_scheme),
	session: AsyncSession = Depends(get_session),  # noqa: B008
) -> User:
	try:
		user_id: UUID = decode_token(token, "access")
	except (JWTError, ValueError, TypeError):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
	user = await UserRepository(session).get_by_id(user_id)
	if user is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
	return user
