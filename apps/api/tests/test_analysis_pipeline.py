from uuid import uuid4

from app.infrastructure.agents.quality_agent import AgentResult
from app.infrastructure.agents.quality_agent import Evidence as AgentEvidence
from app.infrastructure.agents.quality_agent import Finding as AgentFinding
from app.models import AgentCategory
from app.services.analysis_pipeline.evidence_validator import validate
from app.services.analysis_pipeline.finding_correlator import correlate
from app.services.analysis_pipeline.result_normalizer import normalize


def make_result(component: str | None, with_evidence: bool) -> AgentResult:
    return AgentResult(
        findings=[
            AgentFinding(
                title="Issue",
                description="Evidence-backed issue",
                severity="MEDIUM",
                confidence=0.8,
                component=component,
            )
        ],
        evidence=[AgentEvidence(file="src/auth.py", line_start=4, tool="test")] if with_evidence else [],
        confidence=0.8,
    )


def test_evidence_validator_rejects_findings_without_evidence() -> None:
    items = normalize("security-agent", AgentCategory.SECURITY, make_result("auth", False), uuid4())
    valid, rejected = validate(items)
    assert valid == []
    assert len(rejected) == 1


def test_correlator_links_findings_from_different_agents() -> None:
    first = normalize("security-agent", AgentCategory.SECURITY, make_result("auth", True), uuid4())
    second = normalize("testing-agent", AgentCategory.TESTING, make_result("auth", True), first[0][0].analysis_run_id)
    correlated = correlate(first + second)
    assert correlated[0][0].correlation_id
    assert correlated[0][0].correlation_id == correlated[1][0].correlation_id
