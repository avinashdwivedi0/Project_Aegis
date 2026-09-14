from pathlib import Path

from app.infrastructure.analyzers.subprocess_utils import run_command


def dependency_scan(root: Path, context: object) -> dict:
	if (root / "package.json").exists():
		return run_command(["npm", "outdated", "--json"], root)
	if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists():
		return run_command(["pip-audit", "-f", "json"], root)
	return {"skipped": True, "reason": "dependency manifest not found"}
