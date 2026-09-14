from uuid import uuid4

import pytest

from app.models import AgentCategory, Evidence, Finding, Severity
from app.services.analysis_pipeline.quality_calculator import compute_scores
from app.services.recommendation_service import RecommendationService


class FakeProvider:
    async def complete(self, system: str, prompt: str, response_model=None, temperature: float = 0.2) -> str:
        return '{"reasoning":"The evidence identifies the issue.","impact":"It increases risk.","action":"Fix the issue.","reference":null}'


def test_quality_scores_penalize_findings() -> None:
    finding = Finding(
        analysis_run_id=uuid4(),
        agent_id="security-agent",
        category=AgentCategory.SECURITY,
        title="Issue",
        description="Issue",
        severity=Severity.HIGH,
        confidence=0.8,
    )
    scores, overall = compute_scores([finding])
    assert scores["SECURITY"] == 88.0
    assert overall < 100


@pytest.mark.asyncio
async def test_recommendation_is_structured() -> None:
    finding = Finding(
        analysis_run_id=uuid4(),
        agent_id="security-agent",
        category=AgentCategory.SECURITY,
        title="Issue",
        description="Issue",
        severity=Severity.HIGH,
        confidence=0.8,
    )
    recommendation = await RecommendationService(FakeProvider()).generate(
        finding,
        [Evidence(finding_id=finding.id, file="app.py")],
        {},
    )
    assert recommendation.finding_id == finding.id
    assert recommendation.action == "Fix the issue."
