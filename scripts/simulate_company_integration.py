from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from protocol_utils import ROOT, build_quote_request, validate_payload, write_json, write_text


INTEGRATION_ROOT = ROOT / "integrations" / "company_sandbox"
INBOUND_DIR = INTEGRATION_ROOT / "inbound"
MAPPED_DIR = INTEGRATION_ROOT / "mapped"
OUTBOUND_DIR = INTEGRATION_ROOT / "outbound"
LEDGER_DIR = INTEGRATION_ROOT / "ledger"
FIXED_TIMESTAMP = "2026-05-26T00:00:00Z"
FIXED_ACTOR = "northstar_integration_sandbox"
FORBIDDEN_PHRASES = [
    "approved to build",
    "approved to fabricate",
    "approved to hire",
    "selected contractor",
    "winner",
    "external routing",
    "payment processed",
    "load-rated certified",
    "certified lifting device",
    "fabrication authorized",
]


@dataclass
class EventRecord:
    timestamp: str
    event_type: str
    actor: str
    status: str
    artifact_path: str
    external_action_taken: bool


class EventLog:
    def __init__(self) -> None:
        self._events: list[EventRecord] = []
        self._counter = 0

    def add(self, event_type: str, artifact_path: str, status: str = "PASS") -> None:
        second = str(self._counter).rjust(2, "0")
        self._counter += 1
        self._events.append(
            EventRecord(
                timestamp=f"2026-05-26T00:00:{second}Z",
                event_type=event_type,
                actor=FIXED_ACTOR,
                status=status,
                artifact_path=artifact_path,
                external_action_taken=False,
            )
        )

    def write(self, path: Path) -> None:
        lines = []
        for event in self._events:
            lines.append(
                json.dumps(
                    {
                        "timestamp": event.timestamp,
                        "event_type": event.event_type,
                        "actor": event.actor,
                        "status": event.status,
                        "artifact_path": event.artifact_path,
                        "external_action_taken": event.external_action_taken,
                    }
                )
            )
        write_text(path, "\n".join(lines) + ("\n" if lines else ""))

    @property
    def events(self) -> list[EventRecord]:
        return list(self._events)


def ensure_directories() -> None:
    for path in [INBOUND_DIR, MAPPED_DIR, OUTBOUND_DIR, LEDGER_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False)


def parse_bom_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_for_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def build_company_profile() -> dict[str, Any]:
    return {
        "company_name": "Northstar Fabrication Systems",
        "company_type": "fabrication_shop",
        "integration_mode": "sandbox_only",
        "capabilities": [
            "CNC_LASER_CUTTING",
            "CNC_PLASMA_CUTTING",
            "PRESS_BRAKE_FORMING",
            "DEBURRING",
            "WELDING",
            "POWDER_COATING",
            "SMALL_BATCH_FABRICATION",
        ],
        "allowed_channels": [
            "local_file_exchange",
            "email_preview",
            "webhook_preview",
        ],
        "forbidden_channels": [
            "real_email_send",
            "real_webhook_call",
            "supplier_routing",
            "payment_processing",
            "build_approval",
            "fabrication_approval",
            "engineering_approval",
            "load_certification",
        ],
    }


def build_company_project_payload() -> dict[str, Any]:
    return {
        "company_project_id": "NFS-SANDBOX-001",
        "requester": "Northstar Fabrication Systems Sandbox Queue",
        "project_name": "Industrial Steel Utility Hook Sandbox",
        "project_description": "Sandbox-only Northstar submission showing how a fabrication company could map a hook project payload into Aether-native artifacts without any external action.",
        "part_family": "industrial_steel_utility_hook",
        "drawing_manifest_reference": "integrations/company_sandbox/inbound/company_drawing_manifest.json",
        "bom_reference": "integrations/company_sandbox/inbound/company_bom_export.csv",
        "desired_quote_type": "budgetary_internal_review",
        "required_capabilities": [
            "CNC_LASER_CUTTING",
            "PRESS_BRAKE_FORMING",
            "DEBURRING",
            "POWDER_COATING",
            "SMALL_BATCH_FABRICATION",
        ],
        "target_material": "A36 steel",
        "target_finish": "powder coat black matte optional",
        "dimensions_summary": {
            "height_inches": 8.5,
            "width_inches": 3.0,
            "thickness_inches": 0.375,
            "hole_count": 4,
            "hole_diameter_inches": 0.375,
        },
        "tolerance_summary": "+/- 0.030 inches",
        "unknowns": [
            "real CAD file not provided",
            "drawing is manifest-only",
            "load requirement unknown",
            "mounting substrate unknown",
            "fastener specification requires review",
            "engineering certification not provided",
            "load rating not validated",
        ],
        "assumptions": [
            "Sandbox payload is for internal review only.",
            "A36 steel flat stock is acceptable for budgetary review.",
            "Human approval remains required before any external release.",
        ],
        "human_approval_required": True,
    }


def build_drawing_manifest() -> dict[str, Any]:
    return {
        "manifest_id": "nfs-drawing-manifest-001",
        "company_project_id": "NFS-SANDBOX-001",
        "manifest_type": "drawing_manifest_only",
        "files": [
            {
                "file_name": "utility_hook_print_manifest_only.pdf",
                "file_type": "drawing_manifest_entry",
                "revision": "sandbox-rev0",
                "provided": False,
                "notes": "Manifest-only entry. No real drawing package is included in the sandbox.",
            },
            {
                "file_name": "utility_hook_model_manifest_only.sldprt",
                "file_type": "cad_manifest_entry",
                "revision": "sandbox-rev0",
                "provided": False,
                "notes": "Real CAD file not provided. Sandbox uses manifest metadata only.",
            },
        ],
        "notes": [
            "Sandbox-only manifest.",
            "No real SolidWorks parser is used.",
            "No fabrication approval is implied.",
        ],
    }


def write_bom_csv(path: Path) -> None:
    rows = [
        ["item_id", "name", "category", "quantity", "unit", "material", "length_inches", "width_inches", "thickness_inches", "finish", "notes"],
        ["NFS-001", "Hook blank", "plate_cut_part", "25", "ea", "A36 steel", "8.5", "3.0", "0.375", "powder coat black matte optional", "Primary hook blank for sandbox review"],
        ["NFS-002", "Deburring", "secondary_process", "25", "ea", "n/a", "0", "0", "0", "none", "Deburr and edge-safe handling requirement"],
        ["NFS-003", "Protective finish", "finish", "25", "ea", "powder coat or zinc primer", "0", "0", "0", "powder coat black matte optional", "Final finish depends on environment review"],
    ]
    write_text(path, "\n".join(",".join(row) for row in rows) + "\n")


def map_bom_to_items(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for row in rows:
        dimensions: dict[str, Any] = {}
        if float(row["length_inches"]):
            dimensions["length_inches"] = float(row["length_inches"])
        if float(row["width_inches"]):
            dimensions["width_inches"] = float(row["width_inches"])
        if float(row["thickness_inches"]):
            dimensions["thickness_inches"] = float(row["thickness_inches"])
        if not dimensions:
            dimensions["process_reference"] = row["category"]
        items.append(
            {
                "item_id": row["item_id"],
                "name": row["name"],
                "category": row["category"],
                "quantity": int(row["quantity"]),
                "unit": row["unit"],
                "material": row["material"],
                "dimensions": dimensions,
                "finish": row["finish"],
                "supplier_preference": "Sandbox internal review only",
                "substitution_allowed": row["item_id"] != "NFS-002",
                "notes": row["notes"],
            }
        )
    return items


def build_packet_from_company_payload(
    payload: dict[str, Any],
    drawing_manifest: dict[str, Any],
    bom_rows: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "protocol_version": "0.2.4",
        "project_id": "nfs-hook-001",
        "project_name": payload["project_name"],
        "project_type": "company_integration_sandbox_submission",
        "project_description": payload["project_description"],
        "design_files": [
            {
                "file_name": "company_drawing_manifest.json",
                "file_type": "company_drawing_manifest",
                "path": payload["drawing_manifest_reference"],
                "notes": "Manifest-only company drawing reference. Real CAD file not provided.",
            }
        ],
        "geometry_summary": "Company-sandbox industrial steel utility hook represented by manifest-only drawing references and BOM export metadata.",
        "bom_items": map_bom_to_items(bom_rows),
        "material_specs": [
            payload["target_material"],
            "Engineering review required before any load-bearing interpretation.",
            f"Company project ID preserved: {payload['company_project_id']}",
        ],
        "finish_requirements": [
            payload["target_finish"],
            "Final finish selection requires environment review.",
            "No external action authorized.",
        ],
        "dimensions": {
            "company_project_id": payload["company_project_id"],
            "height_inches": payload["dimensions_summary"]["height_inches"],
            "width_inches": payload["dimensions_summary"]["width_inches"],
            "thickness_inches": payload["dimensions_summary"]["thickness_inches"],
            "hole_count": payload["dimensions_summary"]["hole_count"],
            "hole_diameter_inches": payload["dimensions_summary"]["hole_diameter_inches"],
        },
        "tolerances": [
            f"Target tolerance: {payload['tolerance_summary']}",
            "Drawing is manifest-only; no real print package has been validated.",
            "Load certification not provided.",
        ],
        "site_conditions": [
            "Sandbox submission only.",
            "No supplier outreach.",
            "No quote routing.",
            "No external action authorized.",
        ],
        "location_context": {
            "site_type": "company_integration_sandbox",
            "company_name": "Northstar Fabrication Systems",
            "integration_mode": "sandbox_only",
            "external_action_authorized": False,
        },
        "quote_categories": ["fabrication", "finishing", "internal_review"],
        "capability_requirements": [
            {
                "capability_id": capability,
                "capability_type": "fabrication",
                "required_for": "Northstar sandbox company submission",
                "description": f"Company-sandbox capability requirement for {capability}.",
                "licensed_trade": False,
                "certification_required": False,
                "local_required": False,
                "risk_level": "high" if capability in {"CNC_LASER_CUTTING", "PRESS_BRAKE_FORMING"} else "medium",
                "notes": "Sandbox only. No fabrication approval or external action is implied.",
            }
            for capability in payload["required_capabilities"]
        ],
        "install_scope": "Company sandbox mapping for internal quote review only. Not approved for fabrication, supplier outreach, payment, engineering approval, or load certification.",
        "licensed_trade_required": False,
        "code_review_required": False,
        "permit_review_required": False,
        "safety_notes": [
            "Fake company only. Sandbox-only integration flow.",
            "Human approval required before any external release.",
            "Engineering review required before real-world use.",
            "Load certification not provided.",
            "No external action authorized.",
        ],
        "unknowns": payload["unknowns"],
        "assumptions": payload["assumptions"] + drawing_manifest["notes"],
        "human_approval_required": True,
    }


def build_human_approval_event(project_id: str, artifact_id: str) -> dict[str, Any]:
    return {
        "approval_event_id": "approval_nfs_001",
        "project_id": project_id,
        "artifact_id": artifact_id,
        "approval_type": "quote_request_review",
        "actor_name": "Simulated Human Reviewer",
        "actor_role": "Operations Manager",
        "timestamp": FIXED_TIMESTAMP,
        "decision": "approved_for_internal_review_only",
        "scope_limitations": [
            "not approved for fabrication",
            "not approved for supplier outreach",
            "not approved for payment",
            "not approved for hiring",
            "not engineering approved",
            "not load certified",
        ],
        "notes": "Approved for internal sandbox review only. No external action authorized.",
        "human_approval_required_for_next_stage": True,
    }


def build_notification_event(project_id: str, artifact_id: str) -> dict[str, Any]:
    return {
        "notification_event_id": "notification_nfs_001",
        "event_type": "aether.email.preview.created",
        "project_id": project_id,
        "artifact_id": artifact_id,
        "status": "preview_only",
        "timestamp": FIXED_TIMESTAMP,
        "email_sent": False,
        "notes": [
            "sandbox only",
            "no real email sent",
            "no supplier was contacted",
            "no quote was routed",
            "no build was approved",
            "no fabrication was approved",
            "no engineering approval was granted",
            "no webhook called",
            "not production integration",
            "human approval is required before any external release",
        ],
    }


def render_email_preview(project_id: str) -> str:
    lines = [
        "# Email Notification Preview",
        "",
        "Subject: [Aether Sandbox] Human approval required before external quote review",
        "",
        f"Project ID: {project_id}",
        "",
        "This is a sandbox only preview.",
        "",
        "- no real email sent",
        "- no supplier was contacted",
        "- no quote was routed",
        "- no build was approved",
        "- no fabrication was approved",
        "- no engineering approval was granted",
        "- no webhook called",
        "- not production integration",
        "- human approval is required before any external release",
        "",
        "No external action was taken.",
    ]
    return "\n".join(lines) + "\n"


def build_webhook_preview(project_id: str, artifact_id: str, artifact_paths: list[str]) -> dict[str, Any]:
    return {
        "event_id": "webhook_nfs_001",
        "event_type": "aether.human_approval.required",
        "project_id": project_id,
        "artifact_id": artifact_id,
        "status": "preview_only",
        "timestamp": FIXED_TIMESTAMP,
        "requires_human_review": True,
        "webhook_called": False,
        "forbidden_actions_confirmed": [
            "no supplier contacted",
            "no quote routed",
            "no contractor selected",
            "no hiring approval",
            "no build approval",
            "no fabrication approval",
            "no engineering approval",
            "no payment approval",
            "no load certification",
        ],
        "artifact_paths": artifact_paths,
    }


def build_summary(project_id: str, profile: dict[str, Any], packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "company_name": profile["company_name"],
        "project_id": project_id,
        "integration_mode": profile["integration_mode"],
        "status": "PASS",
        "sandbox_claim": "fake company local-only sandbox mapping into Aether-native artifacts",
        "non_claims": [
            "no real company connected",
            "no real API server",
            "no real email provider",
            "no real webhook delivery",
            "no supplier contact",
            "no quote routing",
            "no build approval",
            "no fabrication approval",
            "no engineering approval",
            "no payment approval",
            "no load certification",
            "not production integration",
        ],
        "human_approval_required": packet["human_approval_required"],
        "engineering_review_required": True,
        "provenance_hashes_generated": True,
        "external_action_taken": False,
    }


def write_provenance_manifest(records: list[dict[str, Any]], path: Path) -> None:
    payload = {
        "manifest_id": "provenance_nfs_001",
        "timestamp": FIXED_TIMESTAMP,
        "record_count": len(records),
        "records": records,
    }
    write_json(path, payload)


def build_provenance_record(
    artifact_id: str,
    artifact_type: str,
    path: Path,
    source_artifacts: list[str],
    schema_or_contract: str,
) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "path": relative_path(path),
        "sha256": sha256_for_path(path),
        "generated_by": "scripts/simulate_company_integration.py",
        "source_artifacts": source_artifacts,
        "timestamp": FIXED_TIMESTAMP,
        "schema_or_contract": schema_or_contract,
        "human_review_required": True,
    }


def check_forbidden_wording(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text:
                hits.append(f"{relative_path(path)}: {phrase}")
    return hits


def run() -> int:
    ensure_directories()
    log = EventLog()

    company_profile = build_company_profile()
    company_profile_path = INTEGRATION_ROOT / "company_profile.json"
    write_json(company_profile_path, company_profile)
    log.add("company_profile_loaded", relative_path(company_profile_path))

    payload = build_company_project_payload()
    payload_path = INBOUND_DIR / "company_project_payload.json"
    write_json(payload_path, payload)
    log.add("inbound_payload_loaded", relative_path(payload_path))

    bom_path = INBOUND_DIR / "company_bom_export.csv"
    write_bom_csv(bom_path)
    log.add("bom_loaded", relative_path(bom_path))

    drawing_manifest = build_drawing_manifest()
    drawing_manifest_path = INBOUND_DIR / "company_drawing_manifest.json"
    write_json(drawing_manifest_path, drawing_manifest)
    log.add("drawing_manifest_loaded", relative_path(drawing_manifest_path))

    bom_rows = parse_bom_rows(bom_path)
    build_packet = build_packet_from_company_payload(payload, drawing_manifest, bom_rows)
    build_packet_errors = validate_payload(build_packet, "build_packet.schema.json")
    if build_packet_errors:
        for error in build_packet_errors:
            print(error)
        return 1
    build_packet_path = MAPPED_DIR / "build_packet.yaml"
    write_yaml(build_packet_path, build_packet)
    log.add("build_packet_mapped", relative_path(build_packet_path))

    quote_request = build_quote_request(build_packet)
    quote_request["exclusions_to_state"].extend(
        [
            "Fabrication approval",
            "Supplier outreach",
            "Payment processing",
            "Quote routing",
        ]
    )
    quote_request["risk_questions"].append("What must remain internal-only before any external quote review?")
    quote_request_path = MAPPED_DIR / "quote_request.json"
    write_json(quote_request_path, quote_request)
    log.add("quote_request_mapped", relative_path(quote_request_path))

    human_approval_event = build_human_approval_event(build_packet["project_id"], quote_request["quote_request_id"])
    human_approval_event_path = MAPPED_DIR / "human_approval_event.json"
    write_json(human_approval_event_path, human_approval_event)
    log.add("human_approval_event_created", relative_path(human_approval_event_path))

    notification_event = build_notification_event(build_packet["project_id"], human_approval_event["approval_event_id"])
    notification_event_path = OUTBOUND_DIR / "notification_event.json"
    write_json(notification_event_path, notification_event)

    email_preview_path = OUTBOUND_DIR / "email_preview.md"
    write_text(email_preview_path, render_email_preview(build_packet["project_id"]))
    log.add("email_preview_created", relative_path(email_preview_path))

    webhook_payload = build_webhook_preview(
        build_packet["project_id"],
        human_approval_event["approval_event_id"],
        [
            relative_path(build_packet_path),
            relative_path(quote_request_path),
            relative_path(human_approval_event_path),
            relative_path(email_preview_path),
        ],
    )
    webhook_payload_path = OUTBOUND_DIR / "webhook_payload.json"
    write_json(webhook_payload_path, webhook_payload)
    log.add("webhook_preview_created", relative_path(webhook_payload_path))

    integration_log_path = LEDGER_DIR / "integration_event_log.jsonl"
    summary_path = LEDGER_DIR / "company_integration_summary.json"
    summary = build_summary(build_packet["project_id"], company_profile, build_packet)
    write_json(summary_path, summary)
    log.add("integration_summary_created", relative_path(summary_path))
    log.add("sandbox_completed", relative_path(summary_path))
    log.write(integration_log_path)

    provenance_records = [
        build_provenance_record("company_profile_nfs_001", "company_profile", company_profile_path, [], "integrations/company_sandbox/company_profile.json"),
        build_provenance_record("company_project_payload_nfs_001", "company_project_payload", payload_path, [relative_path(company_profile_path)], "integrations/company_sandbox/api_contract.md"),
        build_provenance_record("company_bom_export_nfs_001", "company_bom_export", bom_path, [relative_path(payload_path)], "integrations/company_sandbox/api_contract.md"),
        build_provenance_record("company_drawing_manifest_nfs_001", "company_drawing_manifest", drawing_manifest_path, [relative_path(payload_path)], "integrations/company_sandbox/webhook_contract.md"),
        build_provenance_record("build_packet_nfs_001", "build_packet", build_packet_path, [relative_path(payload_path), relative_path(bom_path), relative_path(drawing_manifest_path)], "protocols/build_intent/schemas/build_packet.schema.json"),
        build_provenance_record("quote_request_nfs_001", "quote_request", quote_request_path, [relative_path(build_packet_path)], "protocols/build_intent/schemas/quote_request.schema.json"),
        build_provenance_record("approval_nfs_001", "human_approval_event", human_approval_event_path, [relative_path(quote_request_path)], "docs/HUMAN_APPROVAL_EVENT_SPEC.md"),
        build_provenance_record("notification_nfs_001", "notification_event", notification_event_path, [relative_path(human_approval_event_path)], "docs/EMAIL_NOTIFICATION_SPEC.md"),
        build_provenance_record("webhook_nfs_001", "webhook_payload", webhook_payload_path, [relative_path(human_approval_event_path), relative_path(build_packet_path)], "docs/WEBHOOK_EVENT_SPEC.md"),
        build_provenance_record("email_preview_nfs_001", "email_preview", email_preview_path, [relative_path(human_approval_event_path)], "docs/EMAIL_NOTIFICATION_SPEC.md"),
        build_provenance_record("integration_event_log_nfs_001", "integration_event_log", integration_log_path, [relative_path(company_profile_path), relative_path(payload_path), relative_path(build_packet_path), relative_path(quote_request_path), relative_path(human_approval_event_path)], "docs/COMPANY_INTEGRATION_ARCHITECTURE.md"),
        build_provenance_record("company_integration_summary_nfs_001", "company_integration_summary", summary_path, [relative_path(integration_log_path), relative_path(build_packet_path), relative_path(human_approval_event_path)], "docs/COMPANY_CONNECTION_REQUIREMENTS.md"),
    ]
    provenance_path = LEDGER_DIR / "artifact_provenance_manifest.json"
    write_provenance_manifest(provenance_records, provenance_path)
    log.add("provenance_manifest_created", relative_path(provenance_path))
    log.write(integration_log_path)

    preview_hits = check_forbidden_wording([email_preview_path, webhook_payload_path, human_approval_event_path, summary_path])
    if preview_hits:
        for hit in preview_hits:
            print(hit)
        return 1

    print("Company Integration Sandbox")
    print("Profile: PASS")
    print("Payload mapping: PASS")
    print("Human approval event: PASS")
    print("Email preview only: PASS")
    print("Webhook preview only: PASS")
    print("Provenance manifest: PASS")
    print("Final status: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
