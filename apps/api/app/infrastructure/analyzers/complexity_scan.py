import ast
from pathlib import Path


def complexity_scan(root: Path, context: object) -> dict:
	results = []
	if "Python" not in getattr(context, "languages", {}):
		return {"skipped": True, "reason": "Python complexity scan only"}
	for relative in getattr(context, "file_tree", []):
		if not relative.endswith(".py"):
			continue
		tree = ast.parse((root / relative).read_text(errors="ignore"))
		for node in ast.walk(tree):
			if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
				complexity = sum(isinstance(item, (ast.If, ast.For, ast.While, ast.Try, ast.BoolOp)) for item in ast.walk(node)) + 1
				results.append({"file": relative, "function": node.name, "line": node.lineno, "complexity": complexity})
	return {"skipped": False, "functions": results}
