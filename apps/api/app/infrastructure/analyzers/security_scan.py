import re
from pathlib import Path

SECRET_PATTERNS = {
	"api_key": re.compile(r"(?i)(api[_-]?key|secret[_-]?key)\s*[:=]\s*[\"'][^\"']+[\"']"),
	"password": re.compile(r"(?i)password\s*[:=]\s*[\"'][^\"']+[\"']"),
	"private_key": re.compile(r"-----BEGIN [A-Z ]+ PRIVATE KEY-----"),
}


def security_scan(root: Path, context: object) -> dict:
	secrets = []
	for relative in getattr(context, "file_tree", []):
		path = root / relative
		if path.suffix.lower() not in {".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".env"}:
			continue
		for line_number, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
			for rule, pattern in SECRET_PATTERNS.items():
				if pattern.search(line):
					secrets.append({"file": relative, "line": line_number, "rule": rule})
	return {"secrets": secrets}
