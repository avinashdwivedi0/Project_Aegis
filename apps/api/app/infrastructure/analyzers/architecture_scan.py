import ast
from pathlib import Path


def architecture_scan(root: Path, context: object) -> dict:
	modules: dict[str, list[str]] = {}
	if "Python" not in getattr(context, "languages", {}):
		return {"skipped": True, "reason": "Python architecture scan only"}
	for relative in getattr(context, "file_tree", []):
		if not relative.endswith(".py"):
			continue
		imports = []
		for node in ast.walk(ast.parse((root / relative).read_text(errors="ignore"))):
			if isinstance(node, ast.Import):
				imports.extend(alias.name for alias in node.names)
			elif isinstance(node, ast.ImportFrom) and node.module:
				imports.append(node.module)
		modules[relative] = imports
	return {"skipped": False, "modules": modules}
