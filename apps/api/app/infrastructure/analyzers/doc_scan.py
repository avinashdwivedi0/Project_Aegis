from pathlib import Path


def doc_scan(root: Path, context: object) -> dict:
	files = {path.lower() for path in getattr(context, "file_tree", [])}
	readme = next((path for path in files if path.endswith("readme.md")), None)
	content = (root / readme).read_text(errors="ignore").lower() if readme else ""
	return {
		"readme_exists": readme is not None,
		"setup_section": "setup" in content or "installation" in content,
		"usage_section": "usage" in content,
		"api_section": "api" in content,
		"architecture_documented": any("architecture" in path for path in files),
	}
