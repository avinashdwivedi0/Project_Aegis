from pathlib import Path

from pydantic import BaseModel

from app.infrastructure.analyzers.project_scanner import scan_project


class ProjectContext(BaseModel):
	file_tree: list[str]
	languages: dict[str, int]
	frameworks: list[str]
	package_managers: list[str]
	config_files: list[str]
	test_files: list[str]
	test_frameworks: list[str]
	documentation: list[str]
	dependencies: dict[str, list[str]]
	apis: list[dict[str, str | int]]
	components: list[str]


def build_context(root: Path) -> ProjectContext:
	return ProjectContext.model_validate(scan_project(root))
