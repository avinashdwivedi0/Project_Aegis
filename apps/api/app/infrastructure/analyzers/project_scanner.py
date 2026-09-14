import json
import re
from pathlib import Path

IGNORED_DIRECTORIES = {".git", ".venv", "node_modules", "dist", "build", "venv", "__pycache__", ".pytest_cache"}
EXTENSIONS = {".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript"}


def scan_project(root: Path) -> dict:
	files = [path for path in root.rglob("*") if path.is_file() and not IGNORED_DIRECTORIES.intersection(path.parts)]
	languages: dict[str, int] = {}
	config_files: list[str] = []
	test_files: list[str] = []
	documentation: list[str] = []
	dependencies: dict[str, list[str]] = {}
	apis: list[dict[str, str | int]] = []

	for path in files:
		relative = path.relative_to(root).as_posix()
		language = EXTENSIONS.get(path.suffix.lower())
		if language:
			languages[language] = languages.get(language, 0) + 1
		if path.name in {"package.json", "pyproject.toml", "requirements.txt", "pytest.ini", "jest.config.js", "vitest.config.ts"}:
			config_files.append(relative)
		if "test" in path.name.lower() or "spec" in path.name.lower():
			test_files.append(relative)
		if path.name.lower() in {"readme.md", "contributing.md", "architecture.md", "api.md"}:
			documentation.append(relative)
		if path.name == "package.json":
			data = _read_json(path)
			dependencies[relative] = sorted({*data.get("dependencies", {}), *data.get("devDependencies", {})})
		elif path.name == "requirements.txt":
			dependencies[relative] = [line.split("==")[0].strip() for line in path.read_text().splitlines() if line and not line.startswith("#")]
		if path.suffix.lower() in {".py", ".js", ".jsx", ".ts", ".tsx"}:
			apis.extend(_detect_routes(path, root))

	frameworks = _detect_frameworks(root)
	package_managers = [name for name, marker in (("npm", "package-lock.json"), ("pnpm", "pnpm-lock.yaml"), ("yarn", "yarn.lock"), ("poetry", "poetry.lock")) if (root / marker).exists()]
	return {
		"file_tree": sorted(path.relative_to(root).as_posix() for path in files),
		"languages": languages,
		"frameworks": frameworks,
		"package_managers": package_managers,
		"config_files": sorted(config_files),
		"test_files": sorted(test_files),
		"test_frameworks": _test_frameworks(root),
		"documentation": sorted(documentation),
		"dependencies": dependencies,
		"apis": apis,
		"components": _components(root),
	}


def _read_json(path: Path) -> dict:
	try:
		return json.loads(path.read_text())
	except (OSError, json.JSONDecodeError):
		return {}


def _detect_frameworks(root: Path) -> list[str]:
	package = _read_json(root / "package.json")
	names = set(package.get("dependencies", {})) | set(package.get("devDependencies", {}))
	frameworks = [name for name in ("react", "express", "next", "vite") if name in names]
	requirements = "\n".join(path.read_text(errors="ignore") for path in (root / "requirements.txt", root / "pyproject.toml") if path.exists()).lower()
	frameworks.extend(name for name in ("django", "flask", "fastapi") if name in requirements)
	return sorted(set(frameworks))


def _test_frameworks(root: Path) -> list[str]:
	markers = {"pytest.ini": "pytest", "jest.config.js": "jest", "vitest.config.ts": "vitest"}
	return sorted(value for key, value in markers.items() if (root / key).exists())


def _components(root: Path) -> list[str]:
	for directory in ("src", "app"):
		path = root / directory
		if path.is_dir():
			return sorted(child.name for child in path.iterdir() if child.is_dir())
	return []


def _detect_routes(path: Path, root: Path) -> list[dict[str, str | int]]:
	routes = []
	pattern = re.compile(r"@?(?:app|router)\.(get|post|put|delete)\s*\(\s*[\"']([^\"']+)")
	for line_number, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
		match = pattern.search(line)
		if match:
			routes.append({"file": path.relative_to(root).as_posix(), "line": line_number, "method": match.group(1).upper(), "path": match.group(2)})
	return routes
