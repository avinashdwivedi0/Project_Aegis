from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project, Report


class ReportRepository:
	def __init__(self, session: AsyncSession) -> None:
		self.session = session

	async def save(self, report: Report) -> Report:
		self.session.add(report)
		await self.session.commit()
		await self.session.refresh(report)
		return report

	async def get_for_user(self, report_id: UUID, user_id: UUID) -> Report | None:
		result = await self.session.execute(select(Report).join(Report.project).where(Report.id == report_id, Project.user_id == user_id))
		return result.scalar_one_or_none()
