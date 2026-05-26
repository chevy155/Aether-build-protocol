from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from protocol_utils import ROOT, write_json


MACHINE_DIR = ROOT / "machine"
OUTPUT_PATH = ROOT / "outputs" / "machine_response_latest.json"
FIXED_TIMESTAMP = "2026-05-26T00:00:00Z"
PROTOCOL_VERSION = "0.2.6"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_status(response_type: str) -> str:
    return {
        "success": "PASS",
        "error": "FAIL",
        "warning": "WARN",
        "refusal": "BLOCKED",
        "human_approval_required": "BLOCKED",
    }[response_type]


def normalize_id(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")


def validate_envelope(envelope: dict[str, Any], schema: dict[str, Any], permission_manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(envelope), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{path}: {error.message}")

    forbidden_actions = set(permission_manifest["global_forbidden_actions"])
    if set(envelope["next_safe_actions"]) & forbidden_actions:
        overlap = ", ".join(sorted(set(envelope["next_safe_actions"]) & forbidden_actions))
        errors.append(f"next_safe_actions includes forbidden actions: {overlap}")

    if envelope["external_action_taken"] is not False:
        errors.append("external_action_taken must be false")

    if envelope["response_type"] == "human_approval_required" and envelope["human_review_required"] is not True:
        errors.append("human_approval_required responses must set human_review_required true")

    if envelope["response_type"] == "human_approval_required" and not set(permission_manifest["global_forbidden_actions"]) & set(envelope["forbidden_actions"]):
        errors.append("human_approval_required responses must include unsafe external actions in forbidden_actions")

    if envelope["response_type"] == "refusal" and not envelope["forbidden_actions"]:
        errors.append("refusal responses must include the refused action in forbidden_actions")

    return errors


def build_response(code: str, operation: str, artifact_id: str) -> dict[str, Any]:
    templates = load_json(MACHINE_DIR / "response_templates.json")["templates"]
    permission_manifest = load_json(MACHINE_DIR / "permission_manifest.json")
    error_catalog = {item["error_code"]: item for item in load_json(MACHINE_DIR / "error_catalog.json")["errors"]}
    schema = load_json(MACHINE_DIR / "response_envelope.schema.json")

    if code not in templates:
        raise ValueError(f"Unknown response code: {code}")

    template = dict(templates[code])
    catalog_entry = error_catalog.get(code, {})
    merged = {**catalog_entry, **template}

    response_type = merged["response_type"]
    forbidden_actions = list(dict.fromkeys(merged.get("forbidden_actions", [])))
    if response_type == "refusal":
        forbidden_actions = list(dict.fromkeys(forbidden_actions + [operation]))
    if response_type == "human_approval_required":
        forbidden_actions = list(dict.fromkeys(forbidden_actions + permission_manifest["global_forbidden_actions"]))

    envelope = {
        "response_id": f"resp_{normalize_id(code)}_{normalize_id(operation)}_{normalize_id(artifact_id)}",
        "response_type": response_type,
        "status": build_status(response_type),
        "timestamp": FIXED_TIMESTAMP,
        "protocol_version": PROTOCOL_VERSION,
        "operation": operation,
        "artifact_id": artifact_id,
        "human_review_required": bool(merged["human_review_required"]),
        "external_action_taken": False,
        "message": merged["message"],
        "next_safe_actions": merged.get("next_safe_actions", []),
        "forbidden_actions": forbidden_actions,
        "evidence": [
            "machine/response_templates.json",
            "machine/permission_manifest.json",
            "machine/error_catalog.json",
        ],
        "errors": [],
        "warnings": [],
        "generated_artifacts": [
            "outputs/machine_response_latest.json"
        ],
        "validation_summary": {
            "severity": merged["severity"],
            "safe_to_retry": merged["safe_to_retry"],
            "forbidden_auto_action": merged["forbidden_auto_action"],
        },
        "suggested_human_action": merged["suggested_action"],
        "related_docs": [
            "docs/MACHINE_RESPONSE_ENVELOPE_SPEC.md",
            "docs/MACHINE_RESPONSE_ERROR_HANDLING.md",
        ],
        "related_schema": "machine/response_envelope.schema.json",
        "request_echo": {
            "code": code,
            "operation": operation,
            "artifact_id": artifact_id,
        },
    }

    if response_type in {"error", "refusal", "human_approval_required"}:
        code_key = merged.get("error_code", merged.get("response_code", code))
        envelope["errors"] = [
            {
                "code": code_key,
                "message": merged["message"],
                "severity": merged["severity"],
            }
        ]
    if response_type == "warning":
        code_key = merged.get("error_code", merged.get("response_code", code))
        envelope["warnings"] = [
            {
                "code": code_key,
                "message": merged["message"],
                "severity": merged["severity"],
            }
        ]
    if response_type == "human_approval_required":
        if operation in permission_manifest["human_approval_required_for"]:
            envelope["approval_required_for"] = [operation]
        else:
            envelope["approval_required_for"] = permission_manifest["human_approval_required_for"]

    validation_errors = validate_envelope(envelope, schema, permission_manifest)
    if validation_errors:
        raise ValueError("; ".join(validation_errors))

    return envelope


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic machine response envelopes.")
    parser.add_argument("--code", required=True)
    parser.add_argument("--operation", required=True)
    parser.add_argument("--artifact-id", required=True)
    args = parser.parse_args()

    try:
        envelope = build_response(args.code, args.operation, args.artifact_id)
    except Exception as exc:
        print(f"Machine response generation failed: {exc}")
        return 1

    write_json(OUTPUT_PATH, envelope)
    print(f"Response code: {args.code}")
    print(f"Response type: {envelope['response_type']}")
    print(f"Status: {envelope['status']}")
    print(f"External action taken: {str(envelope['external_action_taken']).lower()}")
    print(f"Wrote: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())