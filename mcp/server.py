from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MACHINE_DIR = ROOT / "machine"
RESPONSE_SCRIPT = ROOT / "scripts" / "generate_machine_response.py"

FORBIDDEN_ACTIONS = {
    "send_email",
    "call_webhook",
    "contact_supplier",
    "approve_fabrication",
    "approve_engineering",
    "certify_load_rating",
    "scan_network",
    "read_outside_repo",
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _refuse(action: str) -> dict[str, Any]:
    return {
        "status": "BLOCKED",
        "action": action,
        "message": f"Action '{action}' is forbidden in the local-only MCP skeleton.",
        "external_action_taken": False,
        "human_review_required": True,
    }


def _run_script(script_path: str, *args: str) -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, script_path, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "script": script_path,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "external_action_taken": False,
        "human_review_required": True,
    }


def read_aether_agent_manifest() -> dict[str, Any]:
    return _load_json(MACHINE_DIR / "aether_agent_manifest.json")


def read_permission_manifest() -> dict[str, Any]:
    return _load_json(MACHINE_DIR / "permission_manifest.json")


def read_schema_index() -> dict[str, Any]:
    return _load_json(MACHINE_DIR / "schema_index.json")


def read_tool_catalog() -> dict[str, Any]:
    return _load_json(MACHINE_DIR / "tool_catalog.json")


def read_error_catalog() -> dict[str, Any]:
    return _load_json(MACHINE_DIR / "error_catalog.json")


def read_response_envelope_schema() -> dict[str, Any]:
    return _load_json(MACHINE_DIR / "response_envelope.schema.json")


def read_response_templates() -> dict[str, Any]:
    return _load_json(MACHINE_DIR / "response_templates.json")


def run_build_packet_validation(build_packet_path: str = "examples/sauna_node/build_packet.yaml") -> dict[str, Any]:
    return _run_script("scripts/validate_build_packet.py", build_packet_path)


def run_industrial_hook_simulation() -> dict[str, Any]:
    return _run_script("scripts/simulate_industrial_hook_pipeline.py")


def run_company_integration_simulation() -> dict[str, Any]:
    return _run_script("scripts/simulate_company_integration.py")


def generate_machine_response(code: str, operation: str, artifact_id: str) -> dict[str, Any]:
    return _run_script(str(RESPONSE_SCRIPT.relative_to(ROOT)).replace("\\", "/"), "--code", code, "--operation", operation, "--artifact-id", artifact_id)


def generate_human_approval_required_response(operation: str, artifact_id: str) -> dict[str, Any]:
    return generate_machine_response("HUMAN_APPROVAL_REQUIRED", operation, artifact_id)


def generate_external_action_forbidden_response(operation: str, artifact_id: str) -> dict[str, Any]:
    return generate_machine_response("EXTERNAL_ACTION_FORBIDDEN", operation, artifact_id)


def refuse_forbidden_action(action: str) -> dict[str, Any]:
    if action in FORBIDDEN_ACTIONS:
        result = generate_machine_response("MCP_TOOL_REFUSAL", action, f"mcp_{action}")
        if result["status"] == "PASS":
            return result
        return _refuse(action)
    return {
        "status": "UNKNOWN",
        "action": action,
        "message": "Action is not declared as a safe MCP tool.",
        "external_action_taken": False,
        "human_review_required": True,
    }


if __name__ == "__main__":
    print(json.dumps(_load_json(ROOT / "mcp" / "mcp_manifest.json"), indent=2))