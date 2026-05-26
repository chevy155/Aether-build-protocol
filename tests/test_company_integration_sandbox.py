from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SANDBOX_ROOT = ROOT / "integrations" / "company_sandbox"


def test_company_integration_sandbox_generates_artifacts_and_preserves_guardrails() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/simulate_company_integration.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    required_files = [
        SANDBOX_ROOT / "company_profile.json",
        SANDBOX_ROOT / "README.md",
        SANDBOX_ROOT / "api_contract.md",
        SANDBOX_ROOT / "webhook_contract.md",
        SANDBOX_ROOT / "email_notification_contract.md",
        SANDBOX_ROOT / "approval_workflow.md",
        SANDBOX_ROOT / "inbound" / "company_project_payload.json",
        SANDBOX_ROOT / "inbound" / "company_bom_export.csv",
        SANDBOX_ROOT / "inbound" / "company_drawing_manifest.json",
        SANDBOX_ROOT / "mapped" / "build_packet.yaml",
        SANDBOX_ROOT / "mapped" / "quote_request.json",
        SANDBOX_ROOT / "mapped" / "human_approval_event.json",
        SANDBOX_ROOT / "outbound" / "notification_event.json",
        SANDBOX_ROOT / "outbound" / "email_preview.md",
        SANDBOX_ROOT / "outbound" / "webhook_payload.json",
        SANDBOX_ROOT / "ledger" / "artifact_provenance_manifest.json",
        SANDBOX_ROOT / "ledger" / "integration_event_log.jsonl",
        SANDBOX_ROOT / "ledger" / "company_integration_summary.json",
    ]
    for path in required_files:
        assert path.exists(), str(path)

    build_packet = yaml.safe_load((SANDBOX_ROOT / "mapped" / "build_packet.yaml").read_text(encoding="utf-8"))
    quote_request = json.loads((SANDBOX_ROOT / "mapped" / "quote_request.json").read_text(encoding="utf-8"))
    human_approval = json.loads((SANDBOX_ROOT / "mapped" / "human_approval_event.json").read_text(encoding="utf-8"))
    notification_event = json.loads((SANDBOX_ROOT / "outbound" / "notification_event.json").read_text(encoding="utf-8"))
    webhook_payload = json.loads((SANDBOX_ROOT / "outbound" / "webhook_payload.json").read_text(encoding="utf-8"))
    provenance_manifest = json.loads((SANDBOX_ROOT / "ledger" / "artifact_provenance_manifest.json").read_text(encoding="utf-8"))
    summary = json.loads((SANDBOX_ROOT / "ledger" / "company_integration_summary.json").read_text(encoding="utf-8"))
    email_preview = (SANDBOX_ROOT / "outbound" / "email_preview.md").read_text(encoding="utf-8").lower()
    event_lines = (SANDBOX_ROOT / "ledger" / "integration_event_log.jsonl").read_text(encoding="utf-8").strip().splitlines()
    event_records = [json.loads(line) for line in event_lines]

    assert build_packet["project_id"] == "nfs-hook-001"
    assert build_packet["dimensions"]["company_project_id"] == "NFS-SANDBOX-001"
    assert quote_request["human_approval_required"] is True
    assert "Supplier outreach" in quote_request["exclusions_to_state"]
    assert human_approval["decision"] == "approved_for_internal_review_only"
    assert "not approved for hiring" in human_approval["scope_limitations"]
    assert human_approval["human_approval_required_for_next_stage"] is True
    assert notification_event["email_sent"] is False
    assert webhook_payload["webhook_called"] is False
    assert webhook_payload["requires_human_review"] is True
    assert summary["status"] == "PASS"
    assert summary["external_action_taken"] is False
    assert summary["provenance_hashes_generated"] is True
    assert provenance_manifest["record_count"] == 12
    assert len(provenance_manifest["records"]) == 12
    assert all(len(record["sha256"]) == 64 for record in provenance_manifest["records"])
    assert event_records
    assert all(record["external_action_taken"] is False for record in event_records)
    assert "no real email sent" in email_preview
    assert "no supplier was contacted" in email_preview
    assert "human approval is required before any external release" in email_preview
    assert "no webhook called" in email_preview
    assert "not production integration" in email_preview
    assert "approved to build" not in email_preview
    assert "approved to fabricate" not in email_preview
    assert "approved to hire" not in email_preview
