from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON_PATH = ROOT / "outputs" / "agent_readiness_report.json"
REPORT_MD_PATH = ROOT / "outputs" / "agent_readiness_report.md"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_agent_readiness_check_runs_and_generates_reports() -> None:
    script_path = ROOT / "scripts" / "run_agent_readiness_check.py"
    assert script_path.exists(), str(script_path)

    result = subprocess.run(
        [sys.executable, "scripts/run_agent_readiness_check.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    assert REPORT_JSON_PATH.exists(), str(REPORT_JSON_PATH)
    assert REPORT_MD_PATH.exists(), str(REPORT_MD_PATH)

    report = _load_json(REPORT_JSON_PATH)
    markdown = REPORT_MD_PATH.read_text(encoding="utf-8")

    assert report["readiness_status"] in {"AGENT_READY", "AGENT_PARTIALLY_READY"}
    assert 0 <= report["readiness_score"] <= 100
    assert "send_email" in report["forbidden_actions_verified"]
    assert report["human_approval_gates_verified"]
    assert report["machine_response_evidence"]["external_action_taken_false"] is True
    assert "does not approve fabrication" in markdown.lower()
    assert "does not approve engineering" in markdown.lower()
    assert "does not approve payment" in markdown.lower()
    assert "does not certify load rating" in markdown.lower()
    assert "human approval gates verified" in markdown.lower()