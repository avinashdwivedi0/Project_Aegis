import io
import tempfile
import zipfile
from pathlib import Path


def extract_zip(content: bytes, upload_tmp_dir: str) -> Path:
	destination = Path(tempfile.mkdtemp(prefix="aegis-", dir=upload_tmp_dir))
	with zipfile.ZipFile(io.BytesIO(content)) as archive:
		for member in archive.infolist():
			target = (destination / member.filename).resolve()
			if destination.resolve() not in target.parents:
				raise ValueError("archive contains an invalid path")
		archive.extractall(destination)
	return destination
