from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIM_ROOT = ROOT / "simulations" / "industrial_hook"


def test_industrial_hook_simulation_generates_artifacts_and_preserves_guardrails() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/simulate_industrial_hook_pipeline.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    required_files = [
        SIM_ROOT / "builder_workspace" / "cad" / "utility_hook_v1.mock_sldprt.json",
        SIM_ROOT / "builder_workspace" / "cad" / "utility_hook_print_rev0.mock_pdf.json",
        SIM_ROOT / "builder_workspace" / "bom" / "bom_raw.csv",
        SIM_ROOT / "builder_workspace" / "intake" / "builder_project_intake.yaml",
        SIM_ROOT / "aether_workspace" / "build_packet.yaml",
        SIM_ROOT / "aether_workspace" / "validation_report.md",
        SIM_ROOT / "aether_workspace" / "quote_request.json",
        SIM_ROOT / "aether_workspace" / "RFQ.md",
        SIM_ROOT / "aether_workspace" / "agent_manifest.json",
        SIM_ROOT / "aether_workspace" / "quote_readiness_score.json",
        SIM_ROOT / "aether_workspace" / "quote_readiness_score.md",
        SIM_ROOT / "aether_workspace" / "quote_comparison_summary.json",
        SIM_ROOT / "aether_workspace" / "quote_comparison_summary.md",
        SIM_ROOT / "aether_workspace" / "negotiation_event.json",
        SIM_ROOT / "fabricator_workspace" / "fabricator_profile.json",
        SIM_ROOT / "fabricator_workspace" / "received_packet_manifest.json",
        SIM_ROOT / "fabricator_workspace" / "feasibility_review.json",
        SIM_ROOT / "fabricator_workspace" / "quote_response.json",
        SIM_ROOT / "fabricator_workspace" / "quote_response_validation_report.md",
        SIM_ROOT / "monitor_workspace" / "telemetry_log.jsonl",
        SIM_ROOT / "monitor_workspace" / "guardrail_audit.json",
        SIM_ROOT / "monitor_workspace" / "simulation_trace.json",
        SIM_ROOT / "monitor_workspace" / "ledger_summary.json",
        SIM_ROOT / "monitor_workspace" / "outcome_event.json",
        SIM_ROOT / "outputs" / "simulation_report.md",
        SIM_ROOT / "outputs" / "simulation_report.json",
    ]
    for path in required_files:
        assert path.exists(), str(path)

    report = json.loads((SIM_ROOT / "outputs" / "simulation_report.json").read_text(encoding="utf-8"))
    guardrail_audit = json.loads((SIM_ROOT / "monitor_workspace" / "guardrail_audit.json").read_text(encoding="utf-8"))
    report_md = (SIM_ROOT / "outputs" / "simulation_report.md").read_text(encoding="utf-8").lower()
    quote_validation_md = (SIM_ROOT / "fabricator_workspace" / "quote_response_validation_report.md").read_text(encoding="utf-8")
    telemetry_lines = (SIM_ROOT / "monitor_workspace" / "telemetry_log.jsonl").read_text(encoding="utf-8").strip().splitlines()

    assert report["final_status"] == "PASS"
    assert guardrail_audit["status"] == "PASS"
    assert report["human_review_required"] is True
    assert report["engineering_review_required"] is True
    assert "approved to build" not in report_md
    assert "approved to hire" not in report_md
    assert "load-rated certified" not in report_md
    assert "human review required" in report_md
    assert "engineering review required" in report_md
    assert "**Result:** PASS" in quote_validation_md
    assert len(telemetry_lines) >= 5
