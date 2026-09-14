import hashlib

from app.models import Evidence, Finding


def correlate(items: list[tuple[Finding, list[Evidence]]]) -> list[tuple[Finding, list[Evidence]]]:
	groups: dict[str, list[tuple[Finding, list[Evidence]]]] = {}
	for item in items:
		finding, evidence = item
		key = finding.component or next((entry.file for entry in evidence), "")
		if key:
			groups.setdefault(key, []).append(item)
	for key, group in groups.items():
		if len({finding.agent_id for finding, _ in group}) > 1:
			correlation_id = hashlib.sha1(key.encode(), usedforsecurity=False).hexdigest()[:16]
			for finding, _ in group:
				finding.correlation_id = correlation_id
	return items
