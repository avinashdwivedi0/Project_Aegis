from pathlib import Path

IGNORED_DIRECTORIES = {".git", ".venv", "node_modules", "dist", "build", "venv", "__pycache__", ".pytest_cache"}


def iter_source_files(root: Path):
	return (path for path in root.rglob("*") if path.is_file() and not IGNORED_DIRECTORIES.intersection(path.parts))
