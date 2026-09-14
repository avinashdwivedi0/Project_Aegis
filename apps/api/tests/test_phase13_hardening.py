import asyncio
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.infrastructure.analyzers.project_context import build_context
from app.infrastructure.analyzers.security_scan import security_scan
from app.models import Project, User
from app.repositories.project_repository import ProjectRepository


def test_scanning_uploaded_code_never_executes(tmp_path: Path) -> None:
    marker = tmp_path / "executed.txt"
    (tmp_path / "payload.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n")
    context = build_context(tmp_path)
    security_scan(tmp_path, context)
    assert not marker.exists()


def test_agent_failure_isolation_is_covered() -> None:
    from app.infrastructure.ai.orchestrator import execute_agents
    from tests.test_orchestrator import failing_agent, passing_agent

    results = asyncio.run(execute_agents({}, {"failed": failing_agent, "passed": passing_agent}))
    assert isinstance(results["failed"], RuntimeError)
    assert not isinstance(results["passed"], Exception)


@pytest.mark.asyncio
async def test_project_repository_enforces_user_isolation() -> None:
    engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
    async with async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)() as session:
        owner = User(email="owner@example.com", password_hash="hash")
        other = User(email="other@example.com", password_hash="hash")
        session.add_all([owner, other])
        await session.commit()
        project = Project(user_id=owner.id, name="private", source_type="UPLOAD", source_ref="/tmp/private")
        session.add(project)
        await session.commit()
        assert await ProjectRepository(session).get_for_user(project.id, other.id) is None
        assert await ProjectRepository(session).get_for_user(project.id, owner.id) is not None
    await engine.dispose()
