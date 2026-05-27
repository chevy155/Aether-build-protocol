from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SANDBOX_ROOT = ROOT / "transactions" / "print_job_sandbox"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_print_transaction_sandbox_generates_artifacts_and_preserves_guardrails() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/simulate_print_transaction.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    required_files = [
        SANDBOX_ROOT / "README.md",
        SANDBOX_ROOT / "designer_workspace" / "design_request.json",
        SANDBOX_ROOT / "designer_workspace" / "mock_cad_manifest.json",
        SANDBOX_ROOT / "designer_workspace" / "part_requirements.yaml",
        SANDBOX_ROOT / "designer_workspace" / "bom.csv",
        SANDBOX_ROOT / "aether_transaction" / "build_packet.yaml",
        SANDBOX_ROOT / "aether_transaction" / "quote_request.json",
        SANDBOX_ROOT / "aether_transaction" / "required_capabilities.json",
        SANDBOX_ROOT / "aether_transaction" / "human_approval_event.json",
        SANDBOX_ROOT / "aether_transaction" / "transaction_manifest.json",
        SANDBOX_ROOT / "aether_transaction" / "transaction_state.json",
        SANDBOX_ROOT / "shop_network" / "shops" / "shop_profile_001.json",
        SANDBOX_ROOT / "shop_network" / "shops" / "shop_profile_002.json",
        SANDBOX_ROOT / "shop_network" / "shops" / "shop_profile_003.json",
        SANDBOX_ROOT / "shop_network" / "shop_match_results.json",
        SANDBOX_ROOT / "quotes" / "quote_response_001.json",
        SANDBOX_ROOT / "quotes" / "quote_response_002.json",
        SANDBOX_ROOT / "quotes" / "quote_response_003.json",
        SANDBOX_ROOT / "quotes" / "quote_comparison_summary.json",
        SANDBOX_ROOT / "negotiation" / "negotiation_event_001.json",
        SANDBOX_ROOT / "negotiation" / "negotiation_event_002.json",
        SANDBOX_ROOT / "negotiation" / "negotiation_summary.json",
        SANDBOX_ROOT / "fulfillment" / "simulated_work_order.json",
        SANDBOX_ROOT / "fulfillment" / "simulated_print_status.json",
        SANDBOX_ROOT / "fulfillment" / "simulated_delivery_event.json",
        SANDBOX_ROOT / "fulfillment" / "outcome_event.json",
        SANDBOX_ROOT / "ledger" / "transaction_event_log.jsonl",
        SANDBOX_ROOT / "ledger" / "provenance_manifest.json",
        SANDBOX_ROOT / "ledger" / "guardrail_audit.json",
        SANDBOX_ROOT / "ledger" / "transaction_closeout_report.json",
        SANDBOX_ROOT / "ledger" / "transaction_closeout_report.md",
        SANDBOX_ROOT / "ledger" / "machine_response_envelopes.json",
    ]
    for path in required_files:
        assert path.exists(), str(path)

    design_request = _load_json(SANDBOX_ROOT / "designer_workspace" / "design_request.json")
    build_packet = yaml.safe_load((SANDBOX_ROOT / "aether_transaction" / "build_packet.yaml").read_text(encoding="utf-8"))
    quote_request = _load_json(SANDBOX_ROOT / "aether_transaction" / "quote_request.json")
    required_capabilities = _load_json(SANDBOX_ROOT / "aether_transaction" / "required_capabilities.json")
    human_approval = _load_json(SANDBOX_ROOT / "aether_transaction" / "human_approval_event.json")
    transaction_state = _load_json(SANDBOX_ROOT / "aether_transaction" / "transaction_state.json")
    shop_match_results = _load_json(SANDBOX_ROOT / "shop_network" / "shop_match_results.json")
    quote_responses = [
        _load_json(SANDBOX_ROOT / "quotes" / f"quote_response_00{index}.json")
        for index in range(1, 4)
    ]
    comparison_summary = _load_json(SANDBOX_ROOT / "quotes" / "quote_comparison_summary.json")
    negotiation_1 = _load_json(SANDBOX_ROOT / "negotiation" / "negotiation_event_001.json")
    negotiation_2 = _load_json(SANDBOX_ROOT / "negotiation" / "negotiation_event_002.json")
    work_order = _load_json(SANDBOX_ROOT / "fulfillment" / "simulated_work_order.json")
    print_status = _load_json(SANDBOX_ROOT / "fulfillment" / "simulated_print_status.json")
    delivery_event = _load_json(SANDBOX_ROOT / "fulfillment" / "simulated_delivery_event.json")
    outcome_event = _load_json(SANDBOX_ROOT / "fulfillment" / "outcome_event.json")
    provenance_manifest = _load_json(SANDBOX_ROOT / "ledger" / "provenance_manifest.json")
    guardrail_audit = _load_json(SANDBOX_ROOT / "ledger" / "guardrail_audit.json")
    closeout_report = _load_json(SANDBOX_ROOT / "ledger" / "transaction_closeout_report.json")
    machine_responses = _load_json(SANDBOX_ROOT / "ledger" / "machine_response_envelopes.json")

    assert design_request["project_name"] == "Wall-Mounted 3D Printed Cable Hook"
    assert build_packet["project_id"] == design_request["project_id"]
    assert quote_request["human_approval_required"] is True
    assert required_capabilities["requires_human_review"] is True
    assert human_approval["decision"] == "approved_for_internal_review_only"
    assert "external quote routing" in human_approval["not_approved_actions"]
    assert transaction_state["current_state"] == "CLOSED_LOCAL_ONLY"
    assert transaction_state["states"][-1] == "CLOSED_LOCAL_ONLY"
    assert len(shop_match_results["matches"]) == 3
    assert shop_match_results["selection_status"] == "no shop selected"
    assert all(match["external_contacted"] is False for match in shop_match_results["matches"])
    assert all(match["label"] in {"MOST_COMPLETE_FOR_HUMAN_REVIEW", "NEEDS_CLARIFICATION", "NOT_READY_FOR_REAL_RFQ"} for match in shop_match_results["matches"])
    assert all("winner" not in match["label"].lower() for match in shop_match_results["matches"])
    assert len(quote_responses) == 3
    assert all(response["external_action_taken"] is False for response in quote_responses)
    assert all(response["sandbox_only"] is True for response in quote_responses)
    assert all(response["human_review_required"] is True for response in quote_responses)
    assert all("No shop contacted." in response["exclusions"] for response in quote_responses)
    assert comparison_summary["response_count"] == 3
    assert negotiation_1["external_action_taken"] is False
    assert negotiation_2["external_action_taken"] is False
    assert work_order["external_action_taken"] is False
    assert print_status["external_action_taken"] is False
    assert delivery_event["external_action_taken"] is False
    assert outcome_event["external_action_taken"] is False
    assert outcome_event["sandbox_only"] is True
    assert provenance_manifest["record_count"] == len(provenance_manifest["records"])
    assert all(len(record["sha256"]) == 64 for record in provenance_manifest["records"])
    assert guardrail_audit["status"] == "PASS"
    assert guardrail_audit["no_email_sent"] is True
    assert guardrail_audit["no_webhook_called"] is True
    assert guardrail_audit["no_real_shop_contacted"] is True
    assert guardrail_audit["no_quote_routed"] is True
    assert guardrail_audit["no_shop_selected"] is True
    assert guardrail_audit["no_print_approved"] is True
    assert guardrail_audit["no_fabrication_approved"] is True
    assert guardrail_audit["no_payment_approved"] is True
    assert guardrail_audit["no_delivery_approved"] is True
    assert guardrail_audit["no_engineering_approval"] is True
    assert guardrail_audit["no_load_certification"] is True
    assert guardrail_audit["human_approval_required"] is True
    assert guardrail_audit["local_only_sandbox"] is True
    assert not guardrail_audit["forbidden_labels_present"]
    assert closeout_report["status"] == "PASS"
    assert closeout_report["external_action_taken"] is False
    response_codes = {item["request_echo"]["code"] for item in machine_responses["responses"]}
    assert {"VALIDATION_PASSED", "HUMAN_APPROVAL_REQUIRED", "EXTERNAL_ACTION_FORBIDDEN", "ENGINEERING_REVIEW_REQUIRED", "LOAD_CERTIFICATION_NOT_PROVIDED"}.issubset(response_codes)