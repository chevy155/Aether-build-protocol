from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from protocol_utils import ROOT, write_json, write_text


NETWORK_DIR = ROOT / "network"
RESOURCE_DIR = NETWORK_DIR / "resources"
OUTPUT_JSON = ROOT / "outputs" / "asi_network_sense_report.json"
OUTPUT_MD = ROOT / "outputs" / "asi_network_sense_report.md"

REQUIRED_RESOURCE_FIELDS = [
    "resource_id",
    "resource_type",
    "description",
    "manifest_path",
    "source_of_truth_status",
    "trust_level",
    "synthetic_or_real",
    "allowed_read",
    "allowed_write",
    "forbidden_actions",
    "human_approval_required_for",
    "audit_required",
    "provenance_required",
]

REQUIRED_MANIFEST_FIELDS = [
    "resource_id",
    "purpose",
    "artifacts",
    "schemas_used",
    "scripts_used",
    "tests_covering_resource",
    "generated_outputs",
    "allowed_agent_actions",
    "forbidden_agent_actions",
    "required_human_approvals",
    "known_limitations",
    "evidence_paths",
]

SAFE_NEXT_ACTIONS = [
    "generate integration findings report",
    "collect reviewer feedback",
    "add bad-input simulation",
    "add human approval event schema tests",
    "add provenance verification tests",
]

REFUSED_UNSAFE_ACTIONS = [
    "send real email",
    "call webhook",
    "contact supplier",
    "approve fabrication",
    "approve engineering",
    "certify load rating",
    "scan network",
    "read outside repo",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_required_fields(payload: dict[str, Any], required: list[str], label: str) -> list[str]:
    missing = []
    for field in required:
        if field not in payload:
            missing.append(f"{label}: missing field {field}")
    return missing


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# ASI Network Sense Report",
        "",
        f"**Resource count:** {report['resource_count']}  ",
        f"**Recommended next build phase:** {report['recommended_next_build_phase']}  ",
        "**Boundary:** local manifests only, no real network scanning, no external access, no autonomous control.",
        "",
        "## Source-of-Truth Resources",
        "",
    ]
    lines.extend(f"- {item}" for item in report["source_of_truth_resources"])
    lines.extend(["", "## Simulation-Only Resources", ""])
    lines.extend(f"- {item}" for item in report["simulation_only_resources"])
    lines.extend(["", "## High-Trust Artifacts", ""])
    lines.extend(f"- {item}" for item in report["high_trust_artifacts"])
    lines.extend(["", "## Low-Trust Artifacts", ""])
    lines.extend(f"- {item}" for item in report["low_trust_artifacts"])
    lines.extend(["", "## Human Approval Gates", ""])
    lines.extend(f"- {item}" for item in report["human_approval_gates"])
    lines.extend(["", "## Forbidden Actions Summary", ""])
    lines.extend(f"- {item}" for item in report["forbidden_actions_summary"])
    lines.extend(["", "## Safe Next Actions", ""])
    lines.extend(f"- {item}" for item in report["safe_next_actions"])
    lines.extend(["", "## Refused Unsafe Actions", ""])
    lines.extend(f"- {item}" for item in report["refused_unsafe_actions"])
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- no fabrication approval",
            "- no engineering approval",
            "- no payment approval",
            "- no supplier contact",
            "- no quote routing",
            "- no load certification",
            "- no network scanning",
            "- human approval required",
        ]
    )
    return "\n".join(lines) + "\n"


def run() -> int:
    errors: list[str] = []

    registry = load_json(NETWORK_DIR / "resource_registry.json")
    trust_map = load_json(NETWORK_DIR / "trust_map.json")
    lineage_map = load_json(NETWORK_DIR / "data_lineage_map.json")
    permission_boundaries = load_json(NETWORK_DIR / "permission_boundaries.json")

    resources = registry.get("resources", [])
    if not resources:
        errors.append("resource_registry.json: resources missing or empty")

    manifests: list[dict[str, Any]] = []
    for resource in resources:
        errors.extend(check_required_fields(resource, REQUIRED_RESOURCE_FIELDS, resource.get("resource_id", "unknown_resource")))
        manifest_path = ROOT / resource.get("manifest_path", "")
        if not manifest_path.exists():
            errors.append(f"{resource.get('resource_id', 'unknown_resource')}: manifest missing at {resource.get('manifest_path', '')}")
            continue
        manifest = load_json(manifest_path)
        errors.extend(check_required_fields(manifest, REQUIRED_MANIFEST_FIELDS, manifest.get("resource_id", rel(manifest_path))))
        manifests.append(manifest)

    global_forbidden = permission_boundaries.get("global_forbidden_actions", [])
    human_gated = permission_boundaries.get("actions_requiring_human_approval", [])

    for manifest in manifests:
        allowed = manifest.get("allowed_agent_actions", [])
        overlapping = sorted(set(allowed) & set(global_forbidden))
        if overlapping:
            errors.append(
                f"{manifest['resource_id']}: forbidden global actions listed as allowed: {', '.join(overlapping)}"
            )

    if errors:
        for error in errors:
            print(error)
        return 1

    source_of_truth_resources = [
        resource["resource_id"]
        for resource in resources
        if resource["source_of_truth_status"] in {"primary_source_of_truth", "documentation_reference"}
    ]
    simulation_only_resources = [
        resource["resource_id"]
        for resource in resources
        if resource["synthetic_or_real"] in {"simulation_only", "synthetic_example"}
    ]

    artifact_entries = trust_map.get("artifacts", [])
    high_trust_artifacts = [item["artifact_path"] for item in artifact_entries if item.get("trust_level") == "HIGH"]
    low_trust_artifacts = [item["artifact_path"] for item in artifact_entries if item.get("trust_level") == "LOW"]

    manifest_human_approvals = sorted(
        {
            approval
            for manifest in manifests
            for approval in manifest.get("required_human_approvals", [])
        }
    )
    human_approval_gates = sorted(set(human_gated) | set(manifest_human_approvals))

    safe_next_actions = [action for action in SAFE_NEXT_ACTIONS if action not in global_forbidden]
    forbidden_actions_summary = global_forbidden

    source_truth_count = len(source_of_truth_resources)
    simulation_count = len(simulation_only_resources)
    recommended_next_build_phase = (
        "Expand manifest coverage and add provenance verification tests before any external enablement."
        if source_truth_count and simulation_count
        else "Stabilize the manifest layer before extending the sandbox."
    )

    report = {
        "report_id": "asi_network_sense_report_v0_2_5",
        "resource_count": len(resources),
        "source_of_truth_resources": source_of_truth_resources,
        "simulation_only_resources": simulation_only_resources,
        "high_trust_artifacts": high_trust_artifacts,
        "low_trust_artifacts": low_trust_artifacts,
        "human_approval_gates": human_approval_gates,
        "forbidden_actions_summary": forbidden_actions_summary,
        "safe_next_actions": safe_next_actions,
        "refused_unsafe_actions": REFUSED_UNSAFE_ACTIONS,
        "recommended_next_build_phase": recommended_next_build_phase,
        "lineage_records": [item["lineage_id"] for item in lineage_map.get("lineages", [])],
        "refusal_reason": "Unsafe actions remain outside the manifest-defined local sandbox.",
        "guardrails": {
            "local_manifests_only": True,
            "real_network_scanning": False,
            "external_api_calls": False,
            "email_sent": False,
            "webhook_called": False,
            "supplier_contacted": False,
            "quote_routed": False,
            "contractor_selected": False,
            "build_approved": False,
            "fabrication_approved": False,
            "engineering_approved": False,
            "payment_approved": False,
            "load_certified": False,
            "human_approval_required": True,
        },
    }

    write_json(OUTPUT_JSON, report)
    write_text(OUTPUT_MD, render_markdown(report))

    print("ASI Network Sense Sandbox")
    print("Resource registry: PASS")
    print("Capability manifests: PASS")
    print("Trust map: PASS")
    print("Data lineage map: PASS")
    print("Permission boundaries: PASS")
    print("ASI sense report: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())