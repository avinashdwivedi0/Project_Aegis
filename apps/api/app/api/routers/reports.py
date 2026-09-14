from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.analysis_run import AnalysisRun
from app.models.user import User
from app.repositories.finding_repository import FindingRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.report_repository import ReportRepository
from app.schemas.report_schemas import ReportRead
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/projects/{project_id}", response_model=dict, status_code=201)
async def generate_report(
	project_id: UUID,
	run_id: UUID,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	project = await ProjectRepository(session).get_for_user(project_id, user.id)
	if project is None:
		raise HTTPException(status_code=404, detail="project not found")
	run = await session.scalar(select(AnalysisRun).where(AnalysisRun.id == run_id, AnalysisRun.project_id == project_id))
	if run is None:
		raise HTTPException(status_code=404, detail="analysis not found")
	findings = await FindingRepository(session).list_for_user(user.id)
	findings = [finding for finding in findings if finding.analysis_run_id == run_id]
	report = await ReportService(ReportRepository(session)).generate(project_id, run_id, findings)
	return {"success": True, "data": ReportRead.model_validate(report, from_attributes=True).model_dump(mode="json")}


@router.get("/{report_id}", response_model=dict)
async def get_report(
	report_id: UUID,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	report = await ReportRepository(session).get_for_user(report_id, user.id)
	if report is None:
		raise HTTPException(status_code=404, detail="report not found")
	return {"success": True, "data": ReportRead.model_validate(report, from_attributes=True).model_dump(mode="json")}
