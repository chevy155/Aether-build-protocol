from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
MACHINE_DIR = ROOT / "machine"
OUTPUT_PATH = ROOT / "outputs" / "machine_response_latest.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_machine_response_envelopes_and_generator() -> None:
    schema_path = MACHINE_DIR / "response_envelope.schema.json"
    templates_path = MACHINE_DIR / "response_templates.json"
    assert schema_path.exists(), str(schema_path)
    assert templates_path.exists(), str(templates_path)

    schema = _load_json(schema_path)
    validator = Draft202012Validator(schema)

    example_paths = [
        MACHINE_DIR / "response_examples" / "success.validation_passed.json",
        MACHINE_DIR / "response_examples" / "error.schema_invalid.json",
        MACHINE_DIR / "response_examples" / "error.human_approval_required.json",
        MACHINE_DIR / "response_examples" / "error.external_action_forbidden.json",
        MACHINE_DIR / "response_examples" / "warning.engineering_review_required.json",
        MACHINE_DIR / "response_examples" / "refusal.fabrication_approval_forbidden.json",
    ]
    for path in example_paths:
        assert path.exists(), str(path)
        payload = _load_json(path)
        errors = sorted(validator.iter_errors(payload), key=lambda item: list(item.path))
        assert not errors, f"Schema errors in {path}: {[error.message for error in errors]}"
        assert payload["external_action_taken"] is False

    for command in [
        [sys.executable, "scripts/generate_machine_response.py", "--code", "VALIDATION_PASSED", "--operation", "validate_build_packet", "--artifact-id", "build_packet_001"],
        [sys.executable, "scripts/generate_machine_response.py", "--code", "HUMAN_APPROVAL_REQUIRED", "--operation", "external_release", "--artifact-id", "quote_request_001"],
        [sys.executable, "scripts/generate_machine_response.py", "--code", "EXTERNAL_ACTION_FORBIDDEN", "--operation", "send_email", "--artifact-id", "notification_event_001"],
    ]:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stdout + result.stderr

    assert OUTPUT_PATH.exists(), str(OUTPUT_PATH)

    success_payload = subprocess.run(
        [sys.executable, "scripts/generate_machine_response.py", "--code", "VALIDATION_PASSED", "--operation", "validate_build_packet", "--artifact-id", "build_packet_001"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert success_payload.returncode == 0, success_payload.stdout + success_payload.stderr
    response = _load_json(OUTPUT_PATH)
    assert response["response_type"] == "success"
    assert response["status"] == "PASS"

    human_payload = subprocess.run(
        [sys.executable, "scripts/generate_machine_response.py", "--code", "HUMAN_APPROVAL_REQUIRED", "--operation", "external_release", "--artifact-id", "quote_request_001"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert human_payload.returncode == 0, human_payload.stdout + human_payload.stderr
    response = _load_json(OUTPUT_PATH)
    assert response["response_type"] == "human_approval_required"
    assert response["human_review_required"] is True

    forbidden_payload = subprocess.run(
        [sys.executable, "scripts/generate_machine_response.py", "--code", "EXTERNAL_ACTION_FORBIDDEN", "--operation", "send_email", "--artifact-id", "notification_event_001"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert forbidden_payload.returncode == 0, forbidden_payload.stdout + forbidden_payload.stderr
    response = _load_json(OUTPUT_PATH)
    assert response["response_type"] in {"error", "refusal"}
    assert response["external_action_taken"] is False

    permission_manifest = _load_json(MACHINE_DIR / "permission_manifest.json")
    forbidden_actions = set(permission_manifest["global_forbidden_actions"])
    assert not (set(response["next_safe_actions"]) & forbidden_actions)

    fabrication_response = _load_json(MACHINE_DIR / "response_examples" / "refusal.fabrication_approval_forbidden.json")
    assert "approve_fabrication" in fabrication_response["forbidden_actions"]

    templates = _load_json(templates_path)["templates"]
    assert "approve_payment" in templates["PAYMENT_APPROVAL_FORBIDDEN"]["forbidden_actions"]
    assert "contact_supplier" in templates["SUPPLIER_CONTACT_FORBIDDEN"]["forbidden_actions"]

    openapi_text = (ROOT / "openapi" / "aether.openapi.yaml").read_text(encoding="utf-8")
    assert "ResponseEnvelope" in openapi_text

    mcp_manifest = _load_json(ROOT / "mcp" / "mcp_manifest.json")
    assert "machine/response_envelope.schema.json" in mcp_manifest["resources"]
    assert "generate_machine_response" in mcp_manifest["tools"]