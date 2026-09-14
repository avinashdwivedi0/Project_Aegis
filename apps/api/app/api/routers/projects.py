from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.datastructures import UploadFile

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_session
from app.models.analysis_run import AnalysisRun
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.project_schemas import ProjectRead
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


def service(session: AsyncSession) -> ProjectService:
	return ProjectService(ProjectRepository(session))


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_project(
	request: Request,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	projects = service(session)
	if request.headers.get("content-type", "").startswith("multipart/form-data"):
		content_length = request.headers.get("content-length")
		if content_length and int(content_length) > settings.max_upload_size_mb * 1024 * 1024:
			raise HTTPException(status_code=413, detail="upload exceeds maximum size")
		form = await request.form()
		upload = form.get("upload")
		name = form.get("name")
		if not isinstance(upload, UploadFile) or not isinstance(name, str):
			raise HTTPException(status_code=400, detail="name and upload are required")
		content = await upload.read()
		if len(content) > settings.max_upload_size_mb * 1024 * 1024:
			raise HTTPException(status_code=413, detail="upload exceeds maximum size")
		project = await projects.create_from_upload(name, content, user.id)
	else:
		payload = await request.json()
		name = payload.get("name")
		git_url = payload.get("git_url")
		if not isinstance(name, str) or not isinstance(git_url, str):
			raise HTTPException(status_code=422, detail="name and git_url are required")
		project = await projects.create_from_git(name, git_url, user.id)
	data = ProjectRead.model_validate(project, from_attributes=True).model_dump(mode="json")
	return {"success": True, "data": data}


@router.get("", response_model=dict)
async def list_projects(
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	projects = await service(session).list_projects(user.id)
	data = [ProjectRead.model_validate(project, from_attributes=True).model_dump(mode="json") for project in projects]
	return {"success": True, "data": data}


@router.get("/{project_id}", response_model=dict)
async def get_project(
	project_id: UUID,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	project = await service(session).get_project(project_id, user.id)
	if project is None:
		raise HTTPException(status_code=404, detail="project not found")
	data = ProjectRead.model_validate(project, from_attributes=True).model_dump(mode="json")
	return {"success": True, "data": data}


@router.get("/{project_id}/dashboard", response_model=dict)
async def get_dashboard(
	project_id: UUID,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	project = await service(session).get_project(project_id, user.id)
	if project is None:
		raise HTTPException(status_code=404, detail="project not found")
	result = await session.execute(
		select(AnalysisRun)
		.where(AnalysisRun.project_id == project_id)
		.options(selectinload(AnalysisRun.findings))
		.order_by(desc(AnalysisRun.started_at))
		.limit(1)
	)
	run = result.scalar_one_or_none()
	findings = run.findings if run else []
	severity_counts = {severity: sum(finding.severity.value == severity for finding in findings) for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")}
	return {"success": True, "data": {"project": ProjectRead.model_validate(project, from_attributes=True).model_dump(mode="json"), "analysis": run, "severity_counts": severity_counts}}


@router.delete("/{project_id}", response_model=dict)
async def delete_project(
	project_id: UUID,
	session: AsyncSession = Depends(get_session),  # noqa: B008
	user: User = Depends(get_current_user),  # noqa: B008
) -> dict:
	if not await service(session).delete_project(project_id, user.id):
		raise HTTPException(status_code=404, detail="project not found")
	return {"success": True, "data": None}
