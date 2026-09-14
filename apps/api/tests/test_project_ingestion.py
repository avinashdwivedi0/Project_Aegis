import asyncio
import io
from collections.abc import AsyncGenerator
from zipfile import ZipFile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.api.deps import get_session
from app.infrastructure.analyzers.project_context import build_context
from app.main import app


@pytest.fixture
def client(tmp_path) -> TestClient:
    engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    async def create_tables() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.create_all)

    asyncio.run(create_tables())
    app.dependency_overrides[get_session] = override_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    asyncio.run(engine.dispose())


def test_scanner_builds_project_context(tmp_path) -> None:
    (tmp_path / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n@app.get('/health')\ndef health(): pass\n")
    (tmp_path / "requirements.txt").write_text("fastapi==0.115.0\n")
    (tmp_path / "README.md").write_text("# sample")
    context = build_context(tmp_path)
    assert context.languages == {"Python": 1}
    assert context.frameworks == ["fastapi"]
    assert context.apis[0]["path"] == "/health"


def test_upload_creates_project_with_inventory(client: TestClient, tmp_path) -> None:
    archive = io.BytesIO()
    with ZipFile(archive, "w") as zip_file:
        zip_file.writestr("src/app.py", "print('inspect me')")
        zip_file.writestr("README.md", "# sample")
    archive.seek(0)

    register = client.post("/api/v1/auth/register", json={"email": "project@example.com", "password": "password"})
    token = register.json()["data"]["access_token"]
    response = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        data={"name": "Sample"},
        files={"upload": ("sample.zip", archive, "application/zip")},
    )
    assert response.status_code == 201
    assert response.json()["data"]["inventory"]["languages"] == {"Python": 1}
