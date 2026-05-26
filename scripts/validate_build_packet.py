from __future__ import annotations

import sys
from pathlib import Path

from protocol_utils import EXAMPLE_DIR, OUTPUT_DIR, load_yaml, validate_payload, write_text


def build_report(packet: dict, errors: list[str]) -> str:
    status = "PASS" if not errors else "FAIL"
    unknowns = packet.get("unknowns", [])
    safety_notes = packet.get("safety_notes", [])
    capabilities = [item["capability_id"] for item in packet.get("capability_requirements", [])]

    missing = [message for message in errors if "is a required property" in message]

    lines = [
        "# Validation Report",
        "",
        f"**Project:** {packet.get('project_name', 'unknown')}  ",
        f"**Project ID:** {packet.get('project_id', 'unknown')}  ",
        f"**Result:** {status}",
        "",
        "## Summary",
        "",
        f"- Schema validation: {status}",
        f"- Missing field issues: {len(missing)}",
        f"- Unknowns captured: {len(unknowns)}",
        f"- Safety notes captured: {len(safety_notes)}",
        f"- Licensed trade required: {packet.get('licensed_trade_required', False)}",
        f"- Code review required: {packet.get('code_review_required', False)}",
        f"- Permit review required: {packet.get('permit_review_required', False)}",
        f"- Human approval required: {packet.get('human_approval_required', False)}",
        "",
        "## Required Capabilities",
        "",
    ]
    if capabilities:
        lines.extend(f"- {capability}" for capability in capabilities)
    else:
        lines.append("- None listed")

    lines.extend(["", "## Unknowns", ""])
    if unknowns:
        lines.extend(f"- {item}" for item in unknowns)
    else:
        lines.append("- None recorded")

    lines.extend(["", "## Safety Notes", ""])
    if safety_notes:
        lines.extend(f"- {item}" for item in safety_notes)
    else:
        lines.append("- None recorded")

    lines.extend(["", "## Validation Errors", ""])
    if errors:
        lines.extend(f"- {item}" for item in errors)
    else:
        lines.append("- No schema errors")

    return "\n".join(lines) + "\n"


def main() -> int:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else EXAMPLE_DIR / "build_packet.yaml"
    packet = load_yaml(input_path)
    errors = validate_payload(packet, "build_packet.schema.json")
    report = build_report(packet, errors)

    output_path = OUTPUT_DIR / "validation_report_latest.md"
    example_path = EXAMPLE_DIR / "validation_report.md"
    write_text(output_path, report)
    write_text(example_path, report)

    print(f"Validation result: {'PASS' if not errors else 'FAIL'}")
    print(f"Wrote: {output_path}")
    print(f"Wrote: {example_path}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
