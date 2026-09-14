from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.analysis_run import AnalysisRun


class AnalysisRunRepository:
	def __init__(self, session: AsyncSession) -> None:
		self.session = session

	async def create(self, run: AnalysisRun) -> AnalysisRun:
		self.session.add(run)
		await self.session.commit()
		await self.session.refresh(run)
		if "agent_runs" not in run.__dict__ or run.__dict__.get("agent_runs") is None:
			run.__dict__["agent_runs"] = []
		return run

	async def get_for_user(self, run_id: UUID, user_id: UUID) -> AnalysisRun | None:
		result = await self.session.execute(
			select(AnalysisRun)
			.join(AnalysisRun.project)
			.where(AnalysisRun.id == run_id, AnalysisRun.project.has(user_id=user_id))
			.options(selectinload(AnalysisRun.agent_runs))
		)
		return result.scalar_one_or_none()

	async def save(self, run: AnalysisRun) -> AnalysisRun:
		self.session.add(run)
		await self.session.commit()
		await self.session.refresh(run)
		if "agent_runs" not in run.__dict__ or run.__dict__.get("agent_runs") is None:
			run.__dict__["agent_runs"] = []
		return run
