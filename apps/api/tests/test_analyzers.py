from pathlib import Path

from app.infrastructure.analyzers.architecture_scan import architecture_scan
from app.infrastructure.analyzers.complexity_scan import complexity_scan
from app.infrastructure.analyzers.doc_scan import doc_scan
from app.infrastructure.analyzers.project_context import build_context
from app.infrastructure.analyzers.security_scan import security_scan
from app.infrastructure.analyzers.subprocess_utils import run_command


def test_analyzers_return_structured_results(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text(
        "API_KEY = 'not-a-real-key'\n"
        "def work(value):\n"
        "    if value:\n"
        "        return 1\n"
        "    return 0\n"
    )
    (tmp_path / "README.md").write_text("# App\n\n## Setup\nInstall it.\n\n## Usage\nRun it.\n")
    context = build_context(tmp_path)

    assert security_scan(tmp_path, context)["secrets"][0]["rule"] == "api_key"
    assert complexity_scan(tmp_path, context)["functions"][0]["complexity"] == 2
    assert doc_scan(tmp_path, context)["setup_section"] is True
    assert architecture_scan(tmp_path, context)["skipped"] is False


def test_missing_subprocess_is_skipped(tmp_path: Path) -> None:
    result = run_command(["definitely-missing-aegis-tool"], tmp_path)
    assert result["skipped"] is True
