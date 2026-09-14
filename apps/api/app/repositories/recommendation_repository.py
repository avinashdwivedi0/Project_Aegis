from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AnalysisRun, Finding, Project, Recommendation


class RecommendationRepository:
	def __init__(self, session: AsyncSession) -> None:
		self.session = session

	async def save(self, recommendation: Recommendation) -> Recommendation:
		self.session.add(recommendation)
		await self.session.commit()
		await self.session.refresh(recommendation)
		return recommendation

	async def list_for_project(self, project_id, user_id) -> list[Recommendation]:
		result = await self.session.execute(
			select(Recommendation)
			.join(Recommendation.finding)
			.join(Finding.analysis_run)
			.join(AnalysisRun.project)
			.where(Project.id == project_id, Project.user_id == user_id)
		)
		return list(result.scalars().all())
