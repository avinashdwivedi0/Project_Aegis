import json
import subprocess
from pathlib import Path


def run_command(command: list[str], cwd: Path, timeout: int = 60) -> dict:
	try:
		completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)
	except (FileNotFoundError, subprocess.TimeoutExpired) as error:
		return {"skipped": True, "error": str(error), "stdout": "", "stderr": ""}
	output: object = completed.stdout
	try:
		output = json.loads(completed.stdout)
	except json.JSONDecodeError:
		pass
	return {"skipped": False, "returncode": completed.returncode, "output": output, "stderr": completed.stderr}
