from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from protocol_utils import ROOT, load_json, write_json, write_text


CHECKLIST_PATH = ROOT / "machine" / "agent_readiness_checklist.json"
REPORT_JSON_PATH = ROOT / "outputs" / "agent_readiness_report.json"
REPORT_MD_PATH = ROOT / "outputs" / "agent_readiness_report.md"
MACHINE_RESPONSE_PATH = ROOT / "outputs" / "machine_response_latest.json"


def load_checklist() -> dict[str, Any]:
    return load_json(CHECKLIST_PATH)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def path_exists(path_text: str) -> bool:
    return (ROOT / path_text).exists()


def run_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        "command": " ".join(command),
        "returncode": result.returncode,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def build_readiness_status(score: int) -> str:
    if score == 100:
        return "AGENT_READY"
    if score >= 80:
        return "AGENT_PARTIALLY_READY"
    return "AGENT_NOT_READY"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Agent Readiness Report",
        "",
        "## Executive Summary",
        "",
        f"- Readiness status: {report['readiness_status']}",
        f"- Readiness score: {report['readiness_score']} / 100",
        "- This does not prove production readiness.",
        "- This does not deploy MCP.",
        "- This does not host an API.",
        "- This does not send email.",
        "- This does not call webhooks.",
        "- This does not contact suppliers.",
        "- This does not approve fabrication.",
        "- This does not approve engineering.",
        "- This does not approve payment.",
        "- This does not certify load rating.",
        "",
        "## Discovery Path",
        "",
    ]
    lines.extend(f"- {item}" for item in report["discovery_path"])
    lines.extend([
        "",
        "## Machine Manifests Found",
        "",
    ])
    lines.extend(f"- {item}" for item in report["manifests_discovered"])
    lines.extend([
        "",
        "## Safe Tools Found",
        "",
    ])
    lines.extend(f"- {item}" for item in report["tools_discovered"])
    lines.extend([
        "",
        "## Forbidden Actions Verified",
        "",
    ])
    lines.extend(f"- {item}" for item in report["forbidden_actions_verified"])
    lines.extend([
        "",
        "## Commands Run",
        "",
    ])
    lines.extend(f"- {item['command']}: {item['status']}" for item in report["commands_run"])
    lines.extend([
        "",
        "## Artifacts Generated",
        "",
    ])
    lines.extend(f"- {item}" for item in report["outputs_verified"])
    lines.extend([
        "",
        "## Human Approval Gates Verified",
        "",
    ])
    lines.extend(f"- {item}" for item in report["human_approval_gates_verified"])
    lines.extend([
        "",
        "## Machine Response Evidence",
        "",
        f"- external_action_taken remains false: {report['machine_response_evidence']['external_action_taken_false']}",
        f"- forbidden_actions present: {report['machine_response_evidence']['forbidden_actions_present']}",
        f"- next_safe_actions present: {report['machine_response_evidence']['next_safe_actions_present']}",
        f"- human_review_required preserved when applicable: {report['machine_response_evidence']['human_review_required_when_applicable']}",
        "",
        "## Readiness Score",
        "",
        f"- Score: {report['readiness_score']}",
        f"- Status: {report['readiness_status']}",
        "",
        "## What This Proves",
        "",
        "- A local agent can discover the repository entrypoints and machine-readable manifests.",
        "- A local agent can identify safe tools and forbidden actions.",
        "- A local agent can run the sanctioned sandbox simulations and deterministic response commands.",
        "- Human approval gates remain preserved during local workflows.",
        "",
        "## What This Does Not Prove",
        "",
        "- Production readiness is not proven.",
        "- No hosted API is provided.",
        "- No real MCP deployment is provided.",
        "- No real company integration is performed.",
        "- No external action was taken.",
        "",
        "## Next Safe Action",
        "",
        f"- {report['recommended_next_safe_actions'][0]}",
    ])
    if report["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    if report["missing_items"]:
        lines.extend(["", "## Missing Items", ""])
        lines.extend(f"- {item}" for item in report["missing_items"])
    return "\n".join(lines) + "\n"


def main() -> int:
    checklist = load_checklist()
    permission_manifest = load_json(ROOT / "machine" / "permission_manifest.json")
    tool_catalog = load_json(ROOT / "machine" / "tool_catalog.json")["tools"]

    discovery_path = [
        "README.md",
        "machine/llms.txt",
        "machine/aether_agent_manifest.json",
        "machine/schema_index.json",
        "machine/tool_catalog.json",
        "machine/permission_manifest.json",
        "machine/error_catalog.json",
        "machine/response_envelope.schema.json",
        "mcp/mcp_manifest.json",
        "openapi/aether.openapi.yaml",
    ]

    checks: list[bool] = []
    missing_items: list[str] = []
    warnings: list[str] = []

    files_discovered = [item for item in checklist["required_entrypoints"] if path_exists(item)]
    for item in checklist["required_entrypoints"]:
        ok = path_exists(item)
        checks.append(ok)
        if not ok:
            missing_items.append(item)

    manifests_discovered = [item for item in checklist["required_manifests"] if path_exists(item)]
    for item in checklist["required_manifests"]:
        ok = path_exists(item)
        checks.append(ok)
        if not ok:
            missing_items.append(item)

    for item in checklist["required_scripts"]:
        ok = path_exists(item)
        checks.append(ok)
        if not ok:
            missing_items.append(item)

    forbidden_required = set(checklist["forbidden_actions"])
    forbidden_present = sorted(forbidden_required & set(permission_manifest["global_forbidden_actions"]))
    for action in checklist["forbidden_actions"]:
        ok = action in permission_manifest["global_forbidden_actions"]
        checks.append(ok)
        if not ok:
            missing_items.append(f"permission_manifest missing forbidden action: {action}")

    tools_discovered = [tool["tool_id"] for tool in tool_catalog]
    for tool_id in checklist["required_tools"]:
        ok = tool_id in tools_discovered
        checks.append(ok)
        if not ok:
            missing_items.append(f"tool_catalog missing tool: {tool_id}")

    unsafe_allowed: list[str] = []
    for tool in tool_catalog:
        overlap = sorted(set(tool.get("allowed_actions", [])) & forbidden_required)
        ok = not overlap
        checks.append(ok)
        if overlap:
            unsafe_allowed.append(f"{tool['tool_id']}: {', '.join(overlap)}")
    if unsafe_allowed:
        missing_items.extend(f"forbidden action listed as allowed: {item}" for item in unsafe_allowed)

    commands_to_run = [
        [sys.executable, "scripts/generate_machine_response.py", "--code", "VALIDATION_PASSED", "--operation", "validate_build_packet", "--artifact-id", "build_packet_001"],
        [sys.executable, "scripts/generate_machine_response.py", "--code", "HUMAN_APPROVAL_REQUIRED", "--operation", "external_release", "--artifact-id", "quote_request_001"],
        [sys.executable, "scripts/generate_machine_response.py", "--code", "EXTERNAL_ACTION_FORBIDDEN", "--operation", "send_email", "--artifact-id", "notification_event_001"],
        [sys.executable, "scripts/simulate_company_integration.py"],
        [sys.executable, "scripts/simulate_industrial_hook_pipeline.py"],
    ]
    commands_run: list[dict[str, Any]] = []
    machine_response_results: dict[str, dict[str, Any]] = {}
    for command in commands_to_run:
        result = run_command(command)
        commands_run.append(result)
        ok = result["returncode"] == 0
        checks.append(ok)
        if not ok:
            missing_items.append(f"command failed: {result['command']}")
            continue
        if "generate_machine_response.py" in result["command"] and MACHINE_RESPONSE_PATH.exists():
            code = command[command.index("--code") + 1]
            machine_response_results[code] = load_json(MACHINE_RESPONSE_PATH)

    outputs_verified = [item for item in checklist["required_outputs"] if path_exists(item)]
    for item in checklist["required_outputs"]:
        ok = path_exists(item)
        checks.append(ok)
        if not ok:
            missing_items.append(f"required output missing: {item}")

    external_action_taken_false = all(
        payload.get("external_action_taken") is False for payload in machine_response_results.values()
    ) and bool(machine_response_results)
    forbidden_actions_present = all(bool(payload.get("forbidden_actions")) for payload in machine_response_results.values()) and bool(machine_response_results)
    next_safe_actions_present = all(bool(payload.get("next_safe_actions")) for payload in machine_response_results.values()) and bool(machine_response_results)
    human_review_required_when_applicable = (
        machine_response_results.get("HUMAN_APPROVAL_REQUIRED", {}).get("human_review_required") is True
        and machine_response_results.get("EXTERNAL_ACTION_FORBIDDEN", {}).get("human_review_required") is True
    )
    for item in [
        external_action_taken_false,
        forbidden_actions_present,
        next_safe_actions_present,
        human_review_required_when_applicable,
    ]:
        checks.append(item)

    if not external_action_taken_false:
        missing_items.append("machine responses did not preserve external_action_taken false")
    if not forbidden_actions_present:
        missing_items.append("machine responses missing forbidden_actions")
    if not next_safe_actions_present:
        missing_items.append("machine responses missing next_safe_actions")
    if not human_review_required_when_applicable:
        missing_items.append("machine responses missing human_review_required when applicable")

    human_approval_gates_verified = [
        action for action in permission_manifest["human_approval_required_for"] if action in {"external_release", "real_company_integration", "email_sending", "webhook_delivery"}
    ]
    checks.append(bool(human_approval_gates_verified))
    if not human_approval_gates_verified:
        missing_items.append("human approval gates were not discovered")

    if missing_items:
        warnings.append("Some readiness checks failed or remain incomplete.")

    total_checks = len(checks)
    passed_checks = sum(1 for item in checks if item)
    readiness_score = round((passed_checks / total_checks) * 100) if total_checks else 0
    readiness_status = build_readiness_status(readiness_score)
    if readiness_status != "AGENT_READY" and not warnings:
        warnings.append("Agent readiness is below the fully ready threshold.")

    report = {
        "readiness_status": readiness_status,
        "readiness_score": readiness_score,
        "discovery_path": discovery_path,
        "files_discovered": files_discovered,
        "manifests_discovered": manifests_discovered,
        "tools_discovered": tools_discovered,
        "commands_run": commands_run,
        "outputs_verified": outputs_verified,
        "forbidden_actions_verified": forbidden_present,
        "human_approval_gates_verified": human_approval_gates_verified,
        "unsafe_actions_refused": forbidden_present,
        "machine_response_evidence": {
            "external_action_taken_false": external_action_taken_false,
            "forbidden_actions_present": forbidden_actions_present,
            "next_safe_actions_present": next_safe_actions_present,
            "human_review_required_when_applicable": human_review_required_when_applicable,
        },
        "missing_items": missing_items,
        "warnings": warnings,
        "recommended_next_safe_actions": [
            "Review outputs/agent_readiness_report.md and continue with documented local validation workflows under human review.",
            "read_local_artifact",
            "run_local_validation",
            "generate_local_report",
            "propose_next_action"
        ],
    }

    write_json(REPORT_JSON_PATH, report)
    write_text(REPORT_MD_PATH, render_markdown(report))

    print(f"Readiness status: {readiness_status}")
    print(f"Readiness score: {readiness_score}")
    print(f"Wrote: {REPORT_JSON_PATH}")
    print(f"Wrote: {REPORT_MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())