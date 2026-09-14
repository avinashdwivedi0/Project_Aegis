from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


class ProjectRepository:
	def __init__(self, session: AsyncSession) -> None:
		self.session = session

	async def create(self, project: Project) -> Project:
		self.session.add(project)
		await self.session.commit()
		await self.session.refresh(project)
		return project

	async def list_for_user(self, user_id: UUID) -> list[Project]:
		result = await self.session.execute(select(Project).where(Project.user_id == user_id))
		return list(result.scalars().all())

	async def get_for_user(self, project_id: UUID, user_id: UUID) -> Project | None:
		result = await self.session.execute(
			select(Project).where(Project.id == project_id, Project.user_id == user_id)
		)
		return result.scalar_one_or_none()

	async def delete(self, project: Project) -> None:
		await self.session.delete(project)
		await self.session.commit()
