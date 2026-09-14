from app.infrastructure.ai.ai_provider import AIProvider
from app.models import Evidence, Finding, Recommendation
from app.schemas.recommendation_schemas import RecommendationOutput


class RecommendationService:
	def __init__(self, provider: AIProvider) -> None:
		self.provider = provider

	async def generate(self, finding: Finding, evidence: list[Evidence], context: dict) -> Recommendation:
		output = await self.provider.complete(
			"You write actionable software-quality recommendations from supplied evidence only.",
			f"Finding: {finding.model_dump()}\nEvidence: {[item.model_dump() for item in evidence]}\nContext: {context}",
			response_model=RecommendationOutput,
		)
		data = RecommendationOutput.model_validate_json(output)
		return Recommendation(
			finding_id=finding.id,
			reasoning=data.reasoning,
			impact=data.impact,
			action=data.action,
			reference=data.reference,
		)
