import json
from pathlib import Path


def test_scan(root: Path, context: object) -> dict:
	files = getattr(context, "file_tree", [])
	source_count = sum(path.endswith((".py", ".js", ".jsx", ".ts", ".tsx")) and "test" not in path.lower() and "spec" not in path.lower() for path in files)
	test_files = getattr(context, "test_files", [])
	coverage = None
	for candidate in (root / "coverage.json", root / "coverage" / "coverage-summary.json"):
		if candidate.exists():
			coverage = json.loads(candidate.read_text())
			break
	return {"frameworks": getattr(context, "test_frameworks", []), "source_files": source_count, "test_files": len(test_files), "coverage": coverage}
