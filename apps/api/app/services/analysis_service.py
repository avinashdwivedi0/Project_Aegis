from datetime import UTC, datetime
from uuid import UUID

from app.infrastructure.agents import AGENT_REGISTRY
from app.infrastructure.agents.quality_agent import AgentResult
from app.infrastructure.ai.orchestrator import AIOrchestrator
from app.infrastructure.ai.provider_factory import get_ai_provider
from app.models import AgentCategory, AgentRun, AgentRunStatus, AnalysisRun, AnalysisStatus
from app.models.project import Project
from app.repositories.analysis_run_repository import AnalysisRunRepository
from app.repositories.finding_repository import FindingRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.analysis_pipeline.evidence_validator import validate
from app.services.analysis_pipeline.finding_correlator import correlate
from app.services.analysis_pipeline.quality_calculator import compute_scores
from app.services.analysis_pipeline.result_normalizer import normalize
from app.services.recommendation_service import RecommendationService


class AnalysisService:
	def __init__(
		self,
		repository: AnalysisRunRepository,
		finding_repository: FindingRepository | None = None,
		recommendation_repository: RecommendationRepository | None = None,
	) -> None:
		self.repository = repository
		self.finding_repository = finding_repository
		self.recommendation_repository = recommendation_repository

	async def create_run(self, project: Project) -> AnalysisRun:
		return await self.repository.create(AnalysisRun(project_id=project.id))

	async def execute(self, run: AnalysisRun, project: Project) -> None:
		run.status = AnalysisStatus.RUNNING
		await self.repository.save(run)
		results = await AIOrchestrator().execute(project.inventory or {})
		items = []
		for agent_id, result in results.items():
			if not isinstance(result, Exception):
				items.extend(normalize(agent_id, AgentCategory[AGENT_REGISTRY[agent_id].category], result, run.id))
		items, _ = validate(items)
		items = correlate(items)
		if self.finding_repository is not None:
			await self.finding_repository.save_all(items)
		if self.recommendation_repository is not None:
			recommendations = RecommendationService(get_ai_provider())
			for finding, evidence in items:
				try:
					await self.recommendation_repository.save(
						await recommendations.generate(finding, evidence, project.inventory or {})
					)
				except Exception:  # noqa: BLE001
					run.status = AnalysisStatus.PARTIAL_FAILURE
		scores, overall = compute_scores([finding for finding, _ in items])
		run.dimension_scores = scores
		run.overall_score = overall
		run.agent_runs = [
			AgentRun(
				analysis_run_id=run.id,
				agent_id=agent_id,
				category=AgentCategory[AGENT_REGISTRY[agent_id].category],
				status=AgentRunStatus.FAILED if isinstance(result, Exception) else AgentRunStatus.SUCCEEDED,
				confidence=result.confidence if not isinstance(result, Exception) else None,
				completed_at=datetime.now(UTC),
				error_message=str(result) if isinstance(result, Exception) else None,
			)
			for agent_id, result in results.items()
		]
		if not any(isinstance(result, Exception) for result in results.values()) and run.status != AnalysisStatus.PARTIAL_FAILURE:
			run.status = AnalysisStatus.COMPLETED
		run.completed_at = datetime.now(UTC)
		await self.repository.save(run)

	async def execute_baseline(self, run: AnalysisRun, project: Project) -> None:
		run.status = AnalysisStatus.RUNNING
		await self.repository.save(run)
		result = await get_ai_provider().complete(
			"Review this project as a single software-quality analyst using only supplied context.",
			str(project.inventory or {}),
			response_model=AgentResult,
		)
		parsed = AgentResult.model_validate_json(result)
		items, _ = validate(normalize("single-agent-baseline", AgentCategory.CODE_QUALITY, parsed, run.id))
		items = correlate(items)
		if self.finding_repository is not None:
			await self.finding_repository.save_all(items)
		if self.recommendation_repository is not None:
			recommendations = RecommendationService(get_ai_provider())
			for finding, evidence in items:
				await self.recommendation_repository.save(await recommendations.generate(finding, evidence, project.inventory or {}))
		scores, overall = compute_scores([finding for finding, _ in items])
		run.dimension_scores = scores
		run.overall_score = overall
		run.status = AnalysisStatus.COMPLETED
		run.completed_at = datetime.now(UTC)
		await self.repository.save(run)

	async def get_run(self, run_id: UUID, user_id: UUID) -> AnalysisRun | None:
		return await self.repository.get_for_user(run_id, user_id)
