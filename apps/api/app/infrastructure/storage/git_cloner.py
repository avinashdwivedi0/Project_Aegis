import tempfile
from pathlib import Path

from git import Repo


def clone_repo(url: str, upload_tmp_dir: str) -> Path:
	destination = Path(tempfile.mkdtemp(prefix="aegis-", dir=upload_tmp_dir))
	Repo.clone_from(url, destination, depth=1)
	return destination
