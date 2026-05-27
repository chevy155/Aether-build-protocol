from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_JSON_PATH = ROOT / "outputs" / "mcp_drive" / "latest_agent_run_report.json"
REPORT_MD_PATH = ROOT / "outputs" / "mcp_drive" / "latest_agent_run_report.md"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_mcp_drive_agent_proof_runs_and_generates_reports() -> None:
    script_path = ROOT / "scripts" / "run_mcp_drive_agent_test.py"
    assert script_path.exists(), str(script_path)

    prior_json = REPORT_JSON_PATH.read_text(encoding="utf-8") if REPORT_JSON_PATH.exists() else None
    prior_md = REPORT_MD_PATH.read_text(encoding="utf-8") if REPORT_MD_PATH.exists() else None

    try:
        result = subprocess.run(
            [sys.executable, "scripts/run_mcp_drive_agent_test.py", "--skip-regression-check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode in {0, 1}, result.stdout + result.stderr

        assert REPORT_JSON_PATH.exists(), str(REPORT_JSON_PATH)
        assert REPORT_MD_PATH.exists(), str(REPORT_MD_PATH)

        report = _load_json(REPORT_JSON_PATH)
        markdown = REPORT_MD_PATH.read_text(encoding="utf-8")

        assert report["proof_status"] in {"PASS", "INSUFFICIENT_EVIDENCE"}
        assert report["discovery"]["mcp_server_surface_importable"] is True
        assert report["validation"]["invalid_case_detected"] is True
        assert report["validation"]["repair_successful"] is True
        assert report["forbidden_action_discipline"]["blocked"] is True
        assert report["forbidden_action_discipline"]["external_action_taken"] is False
        assert report["human_approval_preservation"]["payload_requires_human_approval"] is True
        assert report["human_approval_preservation"]["automatic_execution_prevented"] is True
        assert "send_email remained blocked locally" in markdown
        assert "This does not deploy a gateway" in markdown
    finally:
        if prior_json is not None:
            REPORT_JSON_PATH.write_text(prior_json, encoding="utf-8")
        if prior_md is not None:
            REPORT_MD_PATH.write_text(prior_md, encoding="utf-8")