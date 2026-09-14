from pathlib import Path

from app.infrastructure.analyzers.subprocess_utils import run_command


def lint_scan(root: Path, context: object) -> dict:
	if "Python" in getattr(context, "languages", {}):
		return run_command(["pylint", "--output-format=json", "."], root)
	if getattr(context, "languages", {}).get("JavaScript", 0) or getattr(context, "languages", {}).get("TypeScript", 0):
		return run_command(["npx", "eslint", ".", "--format", "json"], root)
	return {"skipped": True, "reason": "unsupported stack"}
