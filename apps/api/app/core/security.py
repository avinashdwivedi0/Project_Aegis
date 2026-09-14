from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
	return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
	return password_context.verify(password, password_hash)


def create_token(user_id: UUID, token_type: str, lifetime: timedelta) -> str:
	expires_at = datetime.now(UTC) + lifetime
	return jwt.encode(
		{"sub": str(user_id), "type": token_type, "exp": expires_at},
		settings.jwt_secret_key,
		algorithm=settings.jwt_algorithm,
	)


def decode_token(token: str, expected_type: str) -> UUID:
	payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
	if payload.get("type") != expected_type:
		raise JWTError("invalid token type")
	return UUID(payload["sub"])
