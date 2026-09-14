from app.models import Evidence, Finding


def validate(
	items: list[tuple[Finding, list[Evidence]]],
) -> tuple[list[tuple[Finding, list[Evidence]]], list[Finding]]:
	valid = [(finding, evidence) for finding, evidence in items if evidence]
	rejected = [finding for finding, evidence in items if not evidence]
	return valid, rejected
