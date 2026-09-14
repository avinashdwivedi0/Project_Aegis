import asyncio
import io
import zipfile
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.api.deps import get_session
from app.main import app


@pytest.fixture
def client() -> TestClient:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
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


def test_register_login_and_protected_route(client: TestClient) -> None:
    register = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "correct horse", "name": "User"},
    )
    assert register.status_code == 200
    tokens = register.json()["data"]

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "correct horse"},
    )
    assert login.status_code == 200

    protected = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert protected.status_code == 200
    assert protected.json()["data"]["email"] == "user@example.com"

    refresh = client.post("/api/v1/auth/refresh", params={"token": tokens["refresh_token"]})
    assert refresh.status_code == 200


def test_analysis_and_report_generation(client: TestClient) -> None:
    register = client.post(
        "/api/v1/auth/register",
        json={"email": "analysis@example.com", "password": "correct horse", "name": "Analyst"},
    )
    assert register.status_code == 200
    token = register.json()["data"]["access_token"]

    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as zip_file:
        zip_file.writestr("src/app.py", "print('hello')\n")
        zip_file.writestr("README.md", "# sample\n")
    archive.seek(0)

    project = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        data={"name": "Analysis Sample"},
        files={"upload": ("sample.zip", archive, "application/zip")},
    )
    assert project.status_code == 201
    project_id = project.json()["data"]["id"]

    analysis = client.post(
        f"/api/v1/projects/{project_id}/analysis",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert analysis.status_code == 202
    run_id = analysis.json()["data"]["id"]

    report = client.post(
        f"/api/v1/reports/projects/{project_id}?run_id={run_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert report.status_code == 201
    assert report.json()["data"]["project_id"] == project_id
    assert report.json()["data"]["analysis_run_id"] == run_id