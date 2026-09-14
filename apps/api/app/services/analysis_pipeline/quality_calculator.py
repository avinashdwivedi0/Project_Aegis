from app.models import Finding, Severity

DIMENSIONS = ("SECURITY", "CODE_QUALITY", "TESTING", "ARCHITECTURE", "DEPENDENCY", "DOCUMENTATION")
PENALTIES = {Severity.CRITICAL: 25, Severity.HIGH: 15, Severity.MEDIUM: 8, Severity.LOW: 3, Severity.INFO: 1}


def compute_scores(findings: list[Finding]) -> tuple[dict[str, float], float]:
	scores = {dimension: 100.0 for dimension in DIMENSIONS}
	for finding in findings:
		scores[finding.category.value] = max(
			0.0,
			scores[finding.category.value] - PENALTIES[finding.severity] * finding.confidence,
		)
	# This simple penalty model is explainable; the exact scoring model will be defined/evaluated during research.
	overall = round(sum(scores.values()) / len(scores), 2)
	return {key: round(value, 2) for key, value in scores.items()}, overall
