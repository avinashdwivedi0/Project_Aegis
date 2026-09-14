from uuid import UUID

from app.models import Finding, Report
from app.repositories.report_repository import ReportRepository


class ReportService:
	def __init__(self, repository: ReportRepository) -> None:
		self.repository = repository

	async def generate(self, project_id: UUID, run_id: UUID, findings: list[Finding]) -> Report:
		content = {
			"executive_summary": {"finding_count": len(findings), "critical_count": sum(item.severity.value == "CRITICAL" for item in findings)},
			"findings": [
				{"title": item.title, "severity": item.severity.value, "category": item.category.value, "description": item.description, "recommendation": item.recommendation.action if item.recommendation else None}
				for item in findings
			],
		}
		return await self.repository.save(Report(project_id=project_id, analysis_run_id=run_id, format="HTML", content=content))
