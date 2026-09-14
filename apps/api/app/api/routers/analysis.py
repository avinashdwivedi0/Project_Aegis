from typing import Literal
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import async_session_factory, get_session
from app.models.analysis_run import AnalysisRun
from app.models.project import Project
from app.models.user import User
from app.repositories.analysis_run_repository import AnalysisRunRepository
from app.repositories.finding_repository import FindingRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.schemas.analysis_schemas import AnalysisRunRead
from app.services.analysis_service import AnalysisService

router = APIRouter(tags=["analysis"])


async def run_in_background(run_id: UUID, project_id: UUID, mode: str) -> None:
	async with async_session_factory() as session:
		run = await session.get(AnalysisRun, run_id)
		project = await session.get(Project, project_id)
		if run is not None and project is not None:
			service = AnalysisService(
				AnalysisRunRepository(session),
				FindingRepository(session),
				RecommendationRepository(session),
			)
			if mode == "single-agent-baseline":
				await service.execute_baseline(run, project)
			else:
				await service.execute(run, project)


@router.post("/projects/{project_id}/analysis", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def start_analysis(
	project_id: UUID,
	background_tasks: BackgroundTasks,
	mode: Literal["multi-agent", "single-agent-baseline"] = "multi-agent",
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	project = await ProjectRepository(session).get_for_user(project_id, user.id)
	if project is None:
		raise HTTPException(status_code=404, detail="project not found")
	run = await AnalysisService(AnalysisRunRepository(session)).create_run(project)
	background_tasks.add_task(run_in_background, run.id, project.id, mode)
	return {"success": True, "data": AnalysisRunRead.model_validate(run, from_attributes=True).model_dump(mode="json")}


@router.get("/analysis/{run_id}", response_model=dict)
async def get_analysis(
	run_id: UUID,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	run = await AnalysisService(AnalysisRunRepository(session)).get_run(run_id, user.id)
	if run is None:
		raise HTTPException(status_code=404, detail="analysis not found")
	return {"success": True, "data": AnalysisRunRead.model_validate(run, from_attributes=True).model_dump(mode="json")}


@router.get("/analysis/{run_id}/findings", response_model=dict)
async def get_findings(
	run_id: UUID,
	severity: str | None = None,
	category: str | None = None,
	component: str | None = None,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	if await AnalysisService(AnalysisRunRepository(session)).get_run(run_id, user.id) is None:
		raise HTTPException(status_code=404, detail="analysis not found")
	findings = await FindingRepository(session).list_for_run(run_id, user.id, severity, category, component)
	return {"success": True, "data": [finding.model_dump(mode="json") for finding in findings]}
