from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NETWORK_DIR = ROOT / "network"
RESOURCE_DIR = NETWORK_DIR / "resources"
OUTPUT_JSON = ROOT / "outputs" / "asi_network_sense_report.json"
OUTPUT_MD = ROOT / "outputs" / "asi_network_sense_report.md"


def test_asi_network_sense_runs_and_preserves_guardrails() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/simulate_asi_network_sense.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    assert OUTPUT_JSON.exists(), str(OUTPUT_JSON)
    assert OUTPUT_MD.exists(), str(OUTPUT_MD)

    registry = json.loads((NETWORK_DIR / "resource_registry.json").read_text(encoding="utf-8"))
    permission_boundaries = json.loads((NETWORK_DIR / "permission_boundaries.json").read_text(encoding="utf-8"))
    report = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    report_md = OUTPUT_MD.read_text(encoding="utf-8").lower()

    expected_resources = {
        "aether_protocol_core",
        "sauna_reference_example",
        "industrial_hook_simulation",
        "company_integration_sandbox",
        "github_release_package",
        "docs_and_findings",
    }
    actual_resources = {resource["resource_id"] for resource in registry["resources"]}
    assert expected_resources == actual_resources

    global_forbidden = set(permission_boundaries["global_forbidden_actions"])
    for resource in registry["resources"]:
        manifest_path = ROOT / resource["manifest_path"]
        assert manifest_path.exists(), str(manifest_path)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["allowed_agent_actions"]
        assert manifest["forbidden_agent_actions"]
        assert not (set(manifest["allowed_agent_actions"]) & global_forbidden)

    assert report["resource_count"] == 6
    assert report["human_approval_gates"]
    assert "scan network" in report["refused_unsafe_actions"]
    assert "approve fabrication" in report["refused_unsafe_actions"]
    assert report["guardrails"]["fabrication_approved"] is False
    assert report["guardrails"]["engineering_approved"] is False
    assert report["guardrails"]["load_certified"] is False
    assert report["guardrails"]["real_network_scanning"] is False
    assert "no fabrication approval" in report_md
    assert "no engineering approval" in report_md
    assert "no load certification" in report_md
    assert "no network scanning" in report_md
    assert "fabrication approved" not in report_md
    assert "engineering approved" not in report_md
