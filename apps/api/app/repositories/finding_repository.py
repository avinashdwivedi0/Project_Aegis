from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import AnalysisRun, Evidence, Finding, Project


class FindingRepository:
	def __init__(self, session: AsyncSession) -> None:
		self.session = session

	async def save_all(self, items: list[tuple[Finding, list[Evidence]]]) -> None:
		for finding, evidence_items in items:
			self.session.add(finding)
			for evidence in evidence_items:
				evidence.finding_id = finding.id
				self.session.add(evidence)
		await self.session.commit()

	async def get_for_user(self, finding_id: UUID, user_id: UUID) -> Finding | None:
		result = await self.session.execute(
			select(Finding)
			.join(Finding.analysis_run)
			.join(AnalysisRun.project)
			.where(Finding.id == finding_id, Project.user_id == user_id)
			.options(selectinload(Finding.evidence), selectinload(Finding.recommendation))
		)
		return result.scalar_one_or_none()

	async def list_for_user(self, user_id: UUID) -> list[Finding]:
		result = await self.session.execute(
			select(Finding)
			.join(Finding.analysis_run)
			.join(AnalysisRun.project)
			.where(Project.user_id == user_id)
			.options(selectinload(Finding.evidence), selectinload(Finding.recommendation))
		)
		return list(result.scalars().unique().all())

	async def list_for_run(self, run_id: UUID, user_id: UUID, severity: str | None = None, category: str | None = None, component: str | None = None) -> list[Finding]:
		query = (
			select(Finding)
			.join(Finding.analysis_run)
			.join(AnalysisRun.project)
			.where(AnalysisRun.id == run_id, Project.user_id == user_id)
			.options(selectinload(Finding.evidence), selectinload(Finding.recommendation))
		)
		if severity:
			query = query.where(Finding.severity == severity)
		if category:
			query = query.where(Finding.category == category)
		if component:
			query = query.where(Finding.component == component)
		result = await self.session.execute(query)
		return list(result.scalars().unique().all())
