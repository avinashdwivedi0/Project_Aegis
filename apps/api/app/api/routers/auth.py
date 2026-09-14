from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import decode_token
from app.db.session import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schemas import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=dict)
async def register(request: RegisterRequest, session: AsyncSession = Depends(get_session)) -> dict:  # noqa: B008
	try:
		tokens = await AuthService(UserRepository(session)).register(request)
	except ValueError as error:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
	return {"success": True, "data": tokens.model_dump(mode="json")}


@router.post("/login", response_model=dict)
async def login(request: LoginRequest, session: AsyncSession = Depends(get_session)) -> dict:  # noqa: B008
	try:
		tokens = await AuthService(UserRepository(session)).login(request)
	except ValueError as error:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
	return {"success": True, "data": tokens.model_dump(mode="json")}


@router.post("/refresh", response_model=dict)
async def refresh(token: str, session: AsyncSession = Depends(get_session)) -> dict:  # noqa: B008
	try:
		user_id = decode_token(token, "refresh")
	except (JWTError, ValueError, TypeError):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
	user = await UserRepository(session).get_by_id(user_id)
	if user is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
	tokens = AuthService(UserRepository(session))._tokens(user)
	return {"success": True, "data": tokens.model_dump(mode="json")}


@router.get("/me", response_model=dict)
async def me(user: User = Depends(get_current_user)) -> dict:  # noqa: B008
	return {"success": True, "data": {"id": str(user.id), "email": user.email, "name": user.name}}
