from pathlib import Path
from uuid import UUID

from app.core.config import settings
from app.infrastructure.analyzers.project_context import build_context
from app.infrastructure.storage.git_cloner import clone_repo
from app.infrastructure.storage.upload_handler import extract_zip
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository


class ProjectService:
	def __init__(self, repository: ProjectRepository) -> None:
		self.repository = repository

	async def create_from_git(self, name: str, git_url: str, user_id: UUID) -> Project:
		Path(settings.upload_tmp_dir).mkdir(parents=True, exist_ok=True)
		root = clone_repo(git_url, settings.upload_tmp_dir)
		return await self._create(name, "GIT_URL", str(root), user_id, root)

	async def create_from_upload(self, name: str, content: bytes, user_id: UUID) -> Project:
		Path(settings.upload_tmp_dir).mkdir(parents=True, exist_ok=True)
		root = extract_zip(content, settings.upload_tmp_dir)
		return await self._create(name, "UPLOAD", str(root), user_id, root)

	async def _create(self, name: str, source_type: str, source_ref: str, user_id: UUID, root: Path) -> Project:
		context = build_context(root)
		stack = {
			"languages": context.languages,
			"frameworks": context.frameworks,
			"package_managers": context.package_managers,
		}
		inventory = context.model_dump()
		inventory["source_root"] = str(root)
		return await self.repository.create(
			Project(
				user_id=user_id,
				name=name,
				source_type=source_type,
				source_ref=source_ref,
				detected_stack=stack,
				inventory=inventory,
			)
		)

	async def list_projects(self, user_id: UUID) -> list[Project]:
		return await self.repository.list_for_user(user_id)

	async def get_project(self, project_id: UUID, user_id: UUID) -> Project | None:
		return await self.repository.get_for_user(project_id, user_id)

	async def delete_project(self, project_id: UUID, user_id: UUID) -> bool:
		project = await self.repository.get_for_user(project_id, user_id)
		if project is None:
			return False
		await self.repository.delete(project)
		return True
