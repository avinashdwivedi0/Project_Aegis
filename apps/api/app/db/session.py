import asyncio
import sys
from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def _async_database_url(database_url: str) -> str:
    if sys.platform == "win32" and settings.environment.lower() in {"development", "local"}:
        if database_url.startswith("postgresql+psycopg://"):
            sqlite_path = Path(__file__).resolve().parents[1] / "aegis_dev.db"
            return f"sqlite+aiosqlite:///{sqlite_path.as_posix()}"
    if database_url.startswith("postgresql+psycopg://"):
        return database_url
    if database_url.startswith("sqlite://"):
        return database_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return database_url


engine = create_async_engine(_async_database_url(settings.database_url), pool_pre_ping=True)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
