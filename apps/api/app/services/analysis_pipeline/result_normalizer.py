from uuid import UUID

from app.infrastructure.agents.quality_agent import AgentResult
from app.models import AgentCategory, Evidence, Finding, Severity


def normalize(
	agent_id: str,
	category: AgentCategory,
	result: AgentResult,
	analysis_run_id: UUID,
) -> list[tuple[Finding, list[Evidence]]]:
	items = []
	for result_finding in result.findings:
		finding = Finding(
				analysis_run_id=analysis_run_id,
				agent_id=agent_id,
				category=category,
				title=result_finding.title,
				description=result_finding.description,
				severity=Severity(result_finding.severity),
				confidence=result_finding.confidence,
				component=result_finding.component,
		)
		evidence = [
			Evidence(
				finding_id=finding.id,
				file=item.file,
				line_start=item.line_start,
				line_end=item.line_end,
				rule=item.rule,
				tool=item.tool,
				snippet=item.snippet,
			)
			for item in result.evidence
		]
		items.append((finding, evidence))
	return items
