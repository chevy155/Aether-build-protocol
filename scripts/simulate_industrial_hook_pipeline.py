from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from generate_rfq_markdown import render_rfq
from protocol_utils import (
    ROOT,
    build_agent_manifest,
    build_negotiation_event,
    build_outcome_event,
    build_quote_comparison_summary,
    build_quote_request,
    build_quote_response_validation_report,
    remove_fields,
    render_build_packet_quote_readiness_report,
    render_quote_comparison_summary,
    score_build_packet_quote_readiness,
    score_quote_response_for_comparison,
    validate_payload,
    write_json,
    write_text,
)
from validate_build_packet import build_report


SIM_ROOT = ROOT / "simulations" / "industrial_hook"
BUILDER_DIR = SIM_ROOT / "builder_workspace"
AETHER_DIR = SIM_ROOT / "aether_workspace"
FABRICATOR_DIR = SIM_ROOT / "fabricator_workspace"
MONITOR_DIR = SIM_ROOT / "monitor_workspace"
OUTPUT_DIR = SIM_ROOT / "outputs"
FIXED_TIMESTAMP = "2026-05-26T00:00:00Z"
FORBIDDEN_PHRASES = [
    "best contractor",
    "winner",
    "approved to hire",
    "approved to build",
    "contractor selected",
    "supplier contacted",
    "payment processed",
    "automatic routing",
    "autonomous order",
    "permit approved",
    "engineering approved",
    "construction approved",
    "load-rated certified",
    "load rated certified",
]


@dataclass
class StageRecord:
    timestamp: str
    stage_name: str
    actor: str
    input_artifact: str
    output_artifact: str
    status: str


class TelemetryRecorder:
    def __init__(self) -> None:
        self._records: list[StageRecord] = []
        self._counter = 0

    def log(self, stage_name: str, actor: str, input_artifact: str, output_artifact: str, status: str) -> None:
        second = str(self._counter).rjust(2, "0")
        self._counter += 1
        self._records.append(
            StageRecord(
                timestamp=f"2026-05-26T00:00:{second}Z",
                stage_name=stage_name,
                actor=actor,
                input_artifact=input_artifact,
                output_artifact=output_artifact,
                status=status,
            )
        )

    def write(self, path: Path) -> None:
        lines = []
        for record in self._records:
            lines.append(
                json.dumps(
                    {
                        "timestamp": record.timestamp,
                        "stage_name": record.stage_name,
                        "actor": record.actor,
                        "input_artifact": record.input_artifact,
                        "output_artifact": record.output_artifact,
                        "status": record.status,
                    }
                )
            )
        write_text(path, "\n".join(lines) + ("\n" if lines else ""))

    @property
    def records(self) -> list[StageRecord]:
        return list(self._records)


def ensure_directories() -> None:
    for path in [
        BUILDER_DIR / "cad",
        BUILDER_DIR / "bom",
        BUILDER_DIR / "intake",
        AETHER_DIR,
        FABRICATOR_DIR,
        MONITOR_DIR,
        OUTPUT_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_builder_workspace(recorder: TelemetryRecorder) -> dict[str, Path]:
    cad_path = BUILDER_DIR / "cad" / "utility_hook_v1.mock_sldprt.json"
    drawing_path = BUILDER_DIR / "cad" / "utility_hook_print_rev0.mock_pdf.json"
    bom_path = BUILDER_DIR / "bom" / "bom_raw.csv"
    intake_path = BUILDER_DIR / "intake" / "builder_project_intake.yaml"

    cad_payload = {
        "file_name": "utility_hook_v1.mock_sldprt.json",
        "file_type": "mock_solidworks_part_metadata",
        "part_name": "Industrial Steel Utility Hook Simulation",
        "geometry_class": "industrial_style_utility_hook",
        "units": "inches",
        "bounding_box": {
            "height": 8.5,
            "width": 3.0,
            "thickness": 0.375,
        },
        "bend_radius_inches": 0.5,
        "mounting_holes": 4,
        "hole_diameter_inches": 0.375,
        "material": "A36 steel",
        "finish": "powder coat black matte optional",
        "notes": [
            "Mock CAD metadata only.",
            "No real CAD geometry is included.",
            "Engineering review required before real fabrication.",
        ],
    }
    drawing_payload = {
        "file_name": "utility_hook_print_rev0.mock_pdf.json",
        "file_type": "mock_pdf_print_metadata",
        "revision": "rev0",
        "drawing_title": "Industrial Steel Utility Hook Simulation",
        "dimensions": {
            "height_inches": 8.5,
            "width_inches": 3.0,
            "thickness_inches": 0.375,
            "hole_diameter_inches": 0.375,
            "hole_count": 4,
        },
        "tolerance_target_inches": "+/- 0.030",
        "notes": [
            "Simulated industrial-style hook for protocol testing only.",
            "Not certified.",
            "Not approved for lifting.",
            "Human approval required before real fabrication.",
        ],
    }
    intake_payload = {
        "project_name": "Industrial Steel Utility Hook Simulation",
        "project_id": "industrial-hook-sim-001",
        "project_type": "industrial_hook_protocol_simulation",
        "project_description": "Industrial-style steel utility hook simulation showing builder-to-fabricator protocol handoff.",
        "safety_statement": "This is a simulated industrial-style hook for protocol testing only. It is not certified, not engineered, not approved for lifting, and not approved for real fabrication without qualified human review.",
        "material": "A36 steel",
        "finish_preference": "powder coat black matte optional",
        "manufacturing_processes": [
            "CNC laser or plasma cutting",
            "deburring",
            "bending/forming if geometry requires it",
            "powder coating or zinc primer finish as optional finish",
        ],
        "dimensions": {
            "height_inches": 8.5,
            "width_inches": 3.0,
            "thickness_inches": 0.375,
            "mounting_holes": 4,
            "hole_diameter_inches": 0.375,
        },
        "tolerance_target_inches": 0.03,
        "quantity": 25,
        "notes": [
            "Mock print metadata only.",
            "Fastener spec intentionally left open for reviewer feedback.",
            "Use as a local-only simulation artifact.",
        ],
        "unknowns": [
            "Actual load requirement unknown",
            "Mounting substrate unknown",
            "Fastener specification requires review",
            "Coating environment unknown",
            "Engineering certification not provided",
            "Real CAD file not included",
            "Drawing is mock metadata only",
        ],
        "assumptions": [
            "A36 steel flat stock is acceptable for budgetary quoting.",
            "Part size fits standard small-batch fabrication equipment.",
            "Human review remains required before any real fabrication decision.",
        ],
        "engineering_review_required": True,
        "human_approval_required": True,
    }
    bom_rows = [
        ["item_id", "name", "category", "quantity", "unit", "material", "length_inches", "width_inches", "thickness_inches", "finish", "supplier_preference", "substitution_allowed", "notes"],
        ["IH-001", "Hook blank", "plate_cut_part", "25", "ea", "A36 steel", "8.5", "3.0", "0.375", "powder coat black matte optional", "Local metal service center", "true", "Main hook profile cut from plate"],
        ["IH-002", "Deburring and edge prep", "secondary_process", "25", "ea", "n/a", "0", "0", "0", "none", "In-house process", "false", "Remove sharp edges before handling"],
        ["IH-003", "Protective finish", "finish", "25", "ea", "powder coat or zinc primer", "0", "0", "0", "powder coat black matte optional", "Regional finisher", "true", "Final finish depends on environment review"],
    ]

    write_json(cad_path, cad_payload)
    write_json(drawing_path, drawing_payload)
    write_text(bom_path, "\n".join(",".join(row) for row in bom_rows) + "\n")
    write_yaml(intake_path, intake_payload)
    recorder.log(
        stage_name="builder_workspace_created",
        actor="builder_simulator",
        input_artifact="local fixture values",
        output_artifact="builder_workspace/cad, bom, intake",
        status="PASS",
    )
    return {
        "cad": cad_path,
        "drawing": drawing_path,
        "bom": bom_path,
        "intake": intake_path,
    }


def parse_bom_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_packet_from_builder(builder_paths: dict[str, Path]) -> dict[str, Any]:
    intake = load_yaml(builder_paths["intake"])
    cad = load_json(builder_paths["cad"])
    drawing = load_json(builder_paths["drawing"])
    bom_rows = parse_bom_rows(builder_paths["bom"])

    bom_items = []
    for row in bom_rows:
        item_id = row["item_id"]
        dimensions: dict[str, Any] = {}
        if float(row["length_inches"]):
            dimensions["length_inches"] = float(row["length_inches"])
        if float(row["width_inches"]):
            dimensions["width_inches"] = float(row["width_inches"])
        if float(row["thickness_inches"]):
            dimensions["thickness_inches"] = float(row["thickness_inches"])
        if not dimensions:
            dimensions["process_reference"] = row["category"]
        bom_items.append(
            {
                "item_id": item_id,
                "name": row["name"],
                "category": row["category"],
                "quantity": int(row["quantity"]),
                "unit": row["unit"],
                "material": row["material"],
                "dimensions": dimensions,
                "finish": row["finish"],
                "supplier_preference": row["supplier_preference"],
                "substitution_allowed": row["substitution_allowed"].lower() == "true",
                "notes": row["notes"],
            }
        )

    return {
        "protocol_version": "0.2.3",
        "project_id": intake["project_id"],
        "project_name": intake["project_name"],
        "project_type": intake["project_type"],
        "project_description": intake["project_description"],
        "design_files": [
            {
                "file_name": cad["file_name"],
                "file_type": "mock_cad_metadata",
                "path": str(builder_paths["cad"].relative_to(SIM_ROOT)).replace("\\", "/"),
                "notes": "Mock CAD metadata only. No real CAD geometry included.",
            },
            {
                "file_name": drawing["file_name"],
                "file_type": "mock_drawing_metadata",
                "path": str(builder_paths["drawing"].relative_to(SIM_ROOT)).replace("\\", "/"),
                "notes": "Mock drawing metadata only. Not certified for real fabrication or lifting.",
            },
        ],
        "geometry_summary": "Industrial-style steel utility hook plate profile with four mounting holes and optional formed geometry represented by mock metadata only.",
        "bom_items": bom_items,
        "material_specs": [
            intake["material"],
            "Optional powder coat or zinc-primer finish after human review.",
            "Fastener specification deferred pending substrate review.",
        ],
        "finish_requirements": [
            intake["finish_preference"],
            "Deburr all exposed edges.",
            "Final finish depends on coating environment review.",
        ],
        "dimensions": {
            "height_inches": intake["dimensions"]["height_inches"],
            "width_inches": intake["dimensions"]["width_inches"],
            "thickness_inches": intake["dimensions"]["thickness_inches"],
            "mounting_holes": intake["dimensions"]["mounting_holes"],
            "hole_diameter_inches": intake["dimensions"]["hole_diameter_inches"],
            "bend_radius_inches": cad["bend_radius_inches"],
        },
        "tolerances": [
            f"Target tolerance: +/- {intake['tolerance_target_inches']:.3f} inches",
            "Mock print only; no certified fabrication tolerance is implied.",
            "Engineering review required before any real-world load-bearing use.",
        ],
        "site_conditions": [
            "Mounting substrate unknown and requires human review.",
            "Coating environment unknown.",
            "No site survey has been performed.",
        ],
        "location_context": {
            "site_type": "simulation_only",
            "country": "USA",
            "network_required": False,
            "external_action_authorized": False,
        },
        "quote_categories": ["fabrication", "forming_review", "finishing"],
        "capability_requirements": [
            {
                "capability_id": "CNC_LASER_CUTTING",
                "capability_type": "fabrication",
                "required_for": "Primary hook profile cutting",
                "description": "Cut the hook blank from A36 plate stock.",
                "licensed_trade": False,
                "certification_required": False,
                "local_required": False,
                "risk_level": "high",
                "notes": "No fabrication authorized by this simulation.",
            },
            {
                "capability_id": "DEBURRING",
                "capability_type": "fabrication",
                "required_for": "Edge cleanup and handling safety",
                "description": "Remove burrs and sharp edges from cut part.",
                "licensed_trade": False,
                "certification_required": False,
                "local_required": False,
                "risk_level": "medium",
                "notes": "Human review required before real-world execution.",
            },
            {
                "capability_id": "PRESS_BRAKE_FORMING",
                "capability_type": "fabrication",
                "required_for": "Optional formed geometry",
                "description": "Form the hook if the final geometry requires a bend.",
                "licensed_trade": False,
                "certification_required": False,
                "local_required": False,
                "risk_level": "medium",
                "notes": "Geometry remains mock metadata only.",
            },
            {
                "capability_id": "POWDER_COATING",
                "capability_type": "finish",
                "required_for": "Optional corrosion-protection finish",
                "description": "Apply powder coat only after environment review.",
                "licensed_trade": False,
                "certification_required": False,
                "local_required": False,
                "risk_level": "medium",
                "notes": "Finish choice depends on environment review.",
            },
            {
                "capability_id": "SMALL_BATCH_FABRICATION",
                "capability_type": "fabrication",
                "required_for": "Quoted lot size",
                "description": "Support a small batch run of 25 parts.",
                "licensed_trade": False,
                "certification_required": False,
                "local_required": False,
                "risk_level": "medium",
                "notes": "Simulation only. No purchase order is implied.",
            },
        ],
        "install_scope": "Budgetary review of an industrial-style steel utility hook simulation only. No fabrication, lifting approval, installation approval, or supplier routing is authorized.",
        "licensed_trade_required": False,
        "code_review_required": False,
        "permit_review_required": False,
        "safety_notes": [
            intake["safety_statement"],
            "Engineering review required before any real-world load-bearing use.",
            "Human approval required before real fabrication.",
            "No external action authorized.",
        ],
        "unknowns": intake["unknowns"],
        "assumptions": intake["assumptions"],
        "human_approval_required": True,
    }


def build_fabricator_profile() -> dict[str, Any]:
    return {
        "fabricator_id": "fabricator-sim-001",
        "fabricator_name": "Deterministic Fabrication Simulator",
        "capabilities": [
            "CNC_LASER_CUTTING",
            "CNC_PLASMA_CUTTING",
            "DEBURRING",
            "PRESS_BRAKE_FORMING",
            "POWDER_COATING",
            "SMALL_BATCH_FABRICATION",
        ],
        "supported_materials": ["A36 steel", "mild steel"],
        "constraints": {
            "max_thickness_inches": 0.5,
            "tolerance_capability_inches": 0.03,
            "minimum_order_quantity": 5,
            "max_part_size_inches": {"height": 48.0, "width": 24.0},
            "coating_options": ["powder coat black matte optional", "zinc primer"],
            "requires_engineering_review_for_load_bearing_parts": True,
            "refuses_certification_without_engineer_stamp": True,
        },
    }


def generate_feasibility_review(packet: dict[str, Any], fabricator_profile: dict[str, Any]) -> dict[str, Any]:
    constraints = fabricator_profile["constraints"]
    required_capabilities = [item["capability_id"] for item in packet["capability_requirements"]]
    available_capabilities = set(fabricator_profile["capabilities"])
    missing_capabilities = [item for item in required_capabilities if item not in available_capabilities]
    thickness = float(packet["dimensions"]["thickness_inches"])
    tolerance_target = 0.03
    finish_options = [spec.lower() for spec in fabricator_profile["constraints"]["coating_options"]]
    finish_matches = [item for item in packet["finish_requirements"] if any(option in item.lower() for option in finish_options)]

    review_flags = [
        "engineering review required before real-world load-bearing use",
        "human approval required before real fabrication",
        "mounting substrate unknown",
        "fastener specification requires review",
        "no lifting approval or certification is implied",
    ]

    return {
        "review_id": f"feas-{packet['project_id']}",
        "project_id": packet["project_id"],
        "fabricator_id": fabricator_profile["fabricator_id"],
        "capability_match": {
            "required": required_capabilities,
            "available": sorted(available_capabilities),
            "missing": missing_capabilities,
            "pass": not missing_capabilities,
        },
        "material_compatibility": {
            "requested": "A36 steel",
            "supported": "A36 steel" in fabricator_profile["supported_materials"],
        },
        "thickness_compatibility": {
            "requested_inches": thickness,
            "max_inches": constraints["max_thickness_inches"],
            "pass": thickness <= constraints["max_thickness_inches"],
        },
        "tolerance_compatibility": {
            "requested_inches": tolerance_target,
            "capability_inches": constraints["tolerance_capability_inches"],
            "pass": tolerance_target <= constraints["tolerance_capability_inches"],
        },
        "finish_compatibility": {
            "requested": packet["finish_requirements"],
            "available": constraints["coating_options"],
            "pass": bool(finish_matches),
        },
        "missing_information": [
            "engineering certification not provided",
            "load rating not provided",
            "mounting substrate unknown",
            "fastener specification requires review",
        ],
        "review_flags": review_flags,
        "human_review_required": True,
        "budgetary_quote_allowed": True,
        "fabrication_approved": False,
        "feasibility_status": "REVIEWABLE_WITH_HUMAN_GATES",
    }


def build_received_packet_manifest(packet: dict[str, Any], quote_request: dict[str, Any], readiness: dict[str, Any]) -> dict[str, Any]:
    return {
        "manifest_id": f"recv-{packet['project_id']}",
        "project_id": packet["project_id"],
        "received_artifacts": [
            "aether_workspace/build_packet.yaml",
            "aether_workspace/quote_request.json",
            "aether_workspace/RFQ.md",
            "aether_workspace/agent_manifest.json",
            "aether_workspace/quote_readiness_score.json",
        ],
        "parsed_fields": {
            "project_name": packet["project_name"],
            "quote_request_id": quote_request["quote_request_id"],
            "quote_readiness_status": readiness["status"],
        },
        "human_review_required": True,
        "external_action_authorized": False,
    }


def build_quote_response(quote_request: dict[str, Any], feasibility_review: dict[str, Any]) -> dict[str, Any]:
    return {
        "quote_response_id": f"resp-{quote_request['project_id']}-fabricator-sim-001",
        "quote_request_id": quote_request["quote_request_id"],
        "responder_name": "Deterministic Fabrication Simulator",
        "responder_type": "fabricator_simulator",
        "quoted_scope": "Budgetary review for cutting, deburring, optional forming, and optional finish on an industrial-style steel utility hook simulation artifact.",
        "price_min": 850.0,
        "price_max": 1275.0,
        "currency": "USD",
        "lead_time_min_days": 7,
        "lead_time_max_days": 14,
        "assumptions": [
            "A36 steel plate is commercially available in the requested thickness.",
            "Quoted geometry is based on mock CAD metadata only.",
            "Human review remains required before any real fabrication decision.",
        ],
        "exclusions": [
            "Informational quote only.",
            "Engineering review required before real-world load-bearing use.",
            "No fabrication authorized.",
            "No supplier contacted.",
            "No external action taken.",
        ],
        "substitutions": [
            "Zinc primer may substitute for powder coat if environment review supports it.",
            "CNC plasma cutting may substitute for laser cutting if edge quality is acceptable after review.",
        ],
        "confidence_score": 0.81,
        "risk_notes": feasibility_review["review_flags"] + [
            "Budget may change if thickness or finish requirements change after human review.",
        ],
        "clarification_questions": [
            "What is the intended non-lifting use case for the hook?",
            "What substrate will receive the mounting holes?",
            "What fastener specification should be reviewed?",
            "Does the environment require powder coat or zinc primer?",
        ],
        "human_review_required": True,
    }


def build_industrial_hook_negotiation_event(quote_request: dict[str, Any], quote_response: dict[str, Any]) -> dict[str, Any]:
    return {
        "negotiation_event_id": f"neg-{quote_response['quote_response_id']}",
        "quote_request_id": quote_request["quote_request_id"],
        "quote_response_id": quote_response["quote_response_id"],
        "event_type": "clarification_requested",
        "actor": "human_operator",
        "timestamp": FIXED_TIMESTAMP,
        "change_summary": "Human reviewer requested clarification on substrate, fastener specification, finish environment, and non-lifting use-case boundaries before comparison.",
        "before": {
            "comparison_status": "unreviewed",
            "confidence_score": quote_response["confidence_score"],
            "clarification_questions_count": len(quote_response.get("clarification_questions", [])),
        },
        "after": {
            "comparison_status": "clarification_pending",
            "required_follow_up": [
                "Confirm the mounting substrate and expected attachment condition.",
                "Confirm the fastener specification and installation boundary.",
                "Confirm the intended environment for powder coat versus zinc primer review.",
                "Confirm the non-lifting use case before any real fabrication review.",
            ],
        },
        "human_approval_required": True,
    }


def build_simulation_comparison_outputs(quote_response: dict[str, Any]) -> tuple[dict[str, Any], str]:
    response_two = remove_fields(quote_response, ["substitutions"])
    response_two["quote_response_id"] = quote_response["quote_response_id"] + "-2"
    response_two["confidence_score"] = 0.69
    response_two["clarification_questions"] = [
        "Confirm substrate.",
        "Confirm finish.",
    ]

    response_three = remove_fields(quote_response, ["assumptions", "exclusions", "clarification_questions"])
    response_three["quote_response_id"] = quote_response["quote_response_id"] + "-3"
    response_three["confidence_score"] = 0.55
    response_three["substitutions"] = []
    response_three["risk_notes"] = ["Insufficient detail for comparison."]

    summary = build_quote_comparison_summary([quote_response, response_two, response_three])
    report = render_quote_comparison_summary(summary)
    return summary, report


def build_guardrail_audit(files_to_scan: list[Path], telemetry: TelemetryRecorder, quote_validation_report: str) -> dict[str, Any]:
    matches: dict[str, list[str]] = {}
    for path in files_to_scan:
        text = path.read_text(encoding="utf-8").lower()
        hit_list = [phrase for phrase in FORBIDDEN_PHRASES if phrase in text]
        if hit_list:
            matches[str(path.relative_to(SIM_ROOT)).replace("\\", "/")] = hit_list

    stage_names = [record.stage_name for record in telemetry.records]
    return {
        "audit_id": "guardrail-industrial-hook-001",
        "timestamp": FIXED_TIMESTAMP,
        "forbidden_phrase_matches": matches,
        "supplier_outreach_detected": False,
        "external_routing_detected": False,
        "contractor_selection_detected": False,
        "hiring_approval_detected": False,
        "build_approval_detected": False,
        "engineering_approval_detected": False,
        "load_certification_detected": False,
        "payment_detected": False,
        "autonomous_ordering_detected": False,
        "quote_response_validation_pass": "**Result:** PASS" in quote_validation_report,
        "monitored_stages": stage_names,
        "status": "PASS" if not matches else "FAIL",
    }


def build_simulation_trace(packet: dict[str, Any], quote_request: dict[str, Any], quote_response: dict[str, Any], outcome_event: dict[str, Any]) -> dict[str, Any]:
    return {
        "simulation_name": "industrial_hook_end_to_end_simulation",
        "lineage": [
            {
                "stage": "builder_package",
                "artifact": "builder_workspace/cad/utility_hook_v1.mock_sldprt.json",
            },
            {
                "stage": "build_packet",
                "artifact": "aether_workspace/build_packet.yaml",
                "project_id": packet["project_id"],
            },
            {
                "stage": "quote_request",
                "artifact": "aether_workspace/quote_request.json",
                "quote_request_id": quote_request["quote_request_id"],
            },
            {
                "stage": "rfq",
                "artifact": "aether_workspace/RFQ.md",
            },
            {
                "stage": "fabricator_response",
                "artifact": "fabricator_workspace/quote_response.json",
                "quote_response_id": quote_response["quote_response_id"],
            },
            {
                "stage": "validation",
                "artifact": "fabricator_workspace/quote_response_validation_report.md",
            },
            {
                "stage": "outcome",
                "artifact": "monitor_workspace/outcome_event.json",
                "outcome_event_id": outcome_event["outcome_event_id"],
            },
        ],
        "status": "PASS",
    }


def build_ledger_summary(packet: dict[str, Any], feasibility_review: dict[str, Any], quote_response: dict[str, Any], guardrail_audit: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_id": f"ledger-{packet['project_id']}",
        "project_id": packet["project_id"],
        "timestamp": FIXED_TIMESTAMP,
        "feasibility_status": feasibility_review["feasibility_status"],
        "quote_response_id": quote_response["quote_response_id"],
        "human_review_required": True,
        "engineering_review_required": True,
        "guardrail_status": guardrail_audit["status"],
        "external_action_taken": False,
        "summary": "Local-only simulation completed without authorizing fabrication, lifting approval, supplier contact, or external action.",
    }


def render_simulation_report(report: dict[str, Any]) -> str:
    lines = [
        "# Industrial Hook Simulation Report",
        "",
        f"**Simulation Name:** {report['simulation_name']}  ",
        f"**Timestamp:** {report['timestamp']}  ",
        f"**Final Status:** {report['final_status']}  ",
        f"**Human Review Required:** {report['human_review_required']}  ",
        f"**Engineering Review Required:** {report['engineering_review_required']}",
        "",
        "## Builder Input Summary",
        "",
        f"- Project: {report['builder_input_summary']['project_name']}",
        f"- Material: {report['builder_input_summary']['material']}",
        f"- Quantity: {report['builder_input_summary']['quantity']}",
        f"- Safety statement: {report['builder_input_summary']['safety_statement']}",
        "",
        "## Generated Protocol Artifacts",
        "",
    ]
    lines.extend(f"- {item}" for item in report["generated_protocol_artifacts"])
    lines.extend([
        "",
        "## Fabricator Review",
        "",
        f"- Capability match result: {report['fabricator_capability_match_result']}",
        f"- Feasibility result: {report['feasibility_result']}",
        f"- Quote response summary: {report['quote_response_summary']}",
        "",
        "## Missing Information",
        "",
    ])
    lines.extend(f"- {item}" for item in report["missing_information"])
    lines.extend([
        "",
        "## Risk Flags",
        "",
    ])
    lines.extend(f"- {item}" for item in report["risk_flags"])
    lines.extend([
        "",
        "## Guardrail Results",
        "",
        f"- Status: {report['guardrail_results']['status']}",
        f"- Local-only simulation: {report['guardrail_results']['local_only_simulation']}",
        f"- No external action authorized: {report['guardrail_results']['no_external_action_authorized']}",
        "",
        "## Telemetry Summary",
        "",
        f"- Stage count: {report['telemetry_summary']['stage_count']}",
        f"- Actors: {', '.join(report['telemetry_summary']['actors'])}",
        "",
        "## Outcome Event Summary",
        "",
        f"- Outcome event ID: {report['outcome_event_summary']['outcome_event_id']}",
        f"- Event type: {report['outcome_event_summary']['event_type']}",
        f"- Delivery status: {report['outcome_event_summary']['delivery_status']}",
    ])
    return "\n".join(lines) + "\n"


def run() -> tuple[int, dict[str, Any]]:
    recorder = TelemetryRecorder()
    ensure_directories()
    builder_paths = write_builder_workspace(recorder)

    packet = build_packet_from_builder(builder_paths)
    packet_errors = validate_payload(packet, "build_packet.schema.json")
    validation_report = build_report(packet, packet_errors)
    quote_request = build_quote_request(packet)
    rfq = render_rfq(quote_request)
    agent_manifest = build_agent_manifest(packet)
    quote_readiness = score_build_packet_quote_readiness(packet, packet_errors)
    quote_readiness_report = render_build_packet_quote_readiness_report(packet, quote_readiness)

    build_packet_path = AETHER_DIR / "build_packet.yaml"
    validation_report_path = AETHER_DIR / "validation_report.md"
    quote_request_path = AETHER_DIR / "quote_request.json"
    rfq_path = AETHER_DIR / "RFQ.md"
    agent_manifest_path = AETHER_DIR / "agent_manifest.json"
    quote_readiness_json_path = AETHER_DIR / "quote_readiness_score.json"
    quote_readiness_md_path = AETHER_DIR / "quote_readiness_score.md"

    write_yaml(build_packet_path, packet)
    write_text(validation_report_path, validation_report)
    write_json(quote_request_path, quote_request)
    write_text(rfq_path, rfq)
    write_json(agent_manifest_path, agent_manifest)
    write_json(quote_readiness_json_path, quote_readiness)
    write_text(quote_readiness_md_path, quote_readiness_report)
    recorder.log(
        stage_name="aether_artifacts_generated",
        actor="aether_protocol_engine",
        input_artifact="builder_workspace package",
        output_artifact="aether_workspace/build_packet.yaml and derived artifacts",
        status="PASS" if not packet_errors else "FAIL",
    )

    fabricator_profile = build_fabricator_profile()
    received_manifest = build_received_packet_manifest(packet, quote_request, quote_readiness)
    feasibility_review = generate_feasibility_review(packet, fabricator_profile)
    quote_response = build_quote_response(quote_request, feasibility_review)
    quote_response_errors = validate_payload(quote_response, "quote_response.schema.json")
    quote_validation_report = build_quote_response_validation_report(quote_response, quote_response_errors)

    fabricator_profile_path = FABRICATOR_DIR / "fabricator_profile.json"
    received_manifest_path = FABRICATOR_DIR / "received_packet_manifest.json"
    feasibility_review_path = FABRICATOR_DIR / "feasibility_review.json"
    quote_response_path = FABRICATOR_DIR / "quote_response.json"
    quote_validation_report_path = FABRICATOR_DIR / "quote_response_validation_report.md"

    write_json(fabricator_profile_path, fabricator_profile)
    write_json(received_manifest_path, received_manifest)
    write_json(feasibility_review_path, feasibility_review)
    write_json(quote_response_path, quote_response)
    write_text(quote_validation_report_path, quote_validation_report)
    recorder.log(
        stage_name="fabricator_simulation_completed",
        actor="fabricator_simulator",
        input_artifact="aether_workspace packet set",
        output_artifact="fabricator_workspace quote response set",
        status="PASS" if not quote_response_errors else "FAIL",
    )

    comparison_summary, comparison_report = build_simulation_comparison_outputs(quote_response)
    comparison_json_path = AETHER_DIR / "quote_comparison_summary.json"
    comparison_md_path = AETHER_DIR / "quote_comparison_summary.md"
    write_json(comparison_json_path, comparison_summary)
    write_text(comparison_md_path, comparison_report)

    negotiation_event = build_industrial_hook_negotiation_event(quote_request, quote_response)
    negotiation_errors = validate_payload(negotiation_event, "negotiation_event.schema.json")
    negotiation_path = AETHER_DIR / "negotiation_event.json"
    write_json(negotiation_path, negotiation_event)

    outcome_event = build_outcome_event(packet, quote_response)
    outcome_errors = validate_payload(outcome_event, "outcome_event.schema.json")
    outcome_path = MONITOR_DIR / "outcome_event.json"
    write_json(outcome_path, outcome_event)
    recorder.log(
        stage_name="comparison_and_outcome_generated",
        actor="aether_protocol_engine",
        input_artifact="fabricator_workspace/quote_response.json",
        output_artifact="quote comparison, negotiation, and outcome artifacts",
        status="PASS" if not (negotiation_errors or outcome_errors) else "FAIL",
    )

    files_to_scan = [
        validation_report_path,
        rfq_path,
        quote_validation_report_path,
        comparison_md_path,
        OUTPUT_DIR / "simulation_report.md",
    ]
    guardrail_audit = build_guardrail_audit(files_to_scan[:-1], recorder, quote_validation_report)
    trace = build_simulation_trace(packet, quote_request, quote_response, outcome_event)
    ledger_summary = build_ledger_summary(packet, feasibility_review, quote_response, guardrail_audit)

    telemetry_path = MONITOR_DIR / "telemetry_log.jsonl"
    guardrail_path = MONITOR_DIR / "guardrail_audit.json"
    trace_path = MONITOR_DIR / "simulation_trace.json"
    ledger_path = MONITOR_DIR / "ledger_summary.json"
    recorder.write(telemetry_path)
    write_json(guardrail_path, guardrail_audit)
    write_json(trace_path, trace)
    write_json(ledger_path, ledger_summary)
    recorder.log(
        stage_name="monitoring_artifacts_written",
        actor="monitoring_agent_stack",
        input_artifact="simulation state",
        output_artifact="monitor_workspace telemetry, audit, trace, ledger",
        status="PASS" if guardrail_audit["status"] == "PASS" else "FAIL",
    )
    recorder.write(telemetry_path)

    quote_validation_pass = "**Result:** PASS" in quote_validation_report
    comparison_responses = comparison_summary["responses"]
    strong_response = score_quote_response_for_comparison(quote_response, quote_response_errors)
    required_artifacts = [
        build_packet_path,
        validation_report_path,
        quote_request_path,
        rfq_path,
        agent_manifest_path,
        quote_readiness_json_path,
        quote_readiness_md_path,
        fabricator_profile_path,
        received_manifest_path,
        feasibility_review_path,
        quote_response_path,
        quote_validation_report_path,
        comparison_json_path,
        comparison_md_path,
        negotiation_path,
        telemetry_path,
        guardrail_path,
        trace_path,
        ledger_path,
        outcome_path,
    ]
    all_artifacts_exist = all(path.exists() for path in required_artifacts)
    final_status = "PASS" if all([
        all_artifacts_exist,
        feasibility_review["capability_match"]["pass"],
        feasibility_review["material_compatibility"]["supported"],
        feasibility_review["thickness_compatibility"]["pass"],
        feasibility_review["tolerance_compatibility"]["pass"],
        feasibility_review["finish_compatibility"]["pass"],
        guardrail_audit["status"] == "PASS",
        quote_validation_pass,
        not quote_response_errors,
        not negotiation_errors,
        not outcome_errors,
        strong_response["comparison_status"] in {"COMPARISON_READY", "MOST_COMPLETE_FOR_HUMAN_REVIEW", "NEEDS_CLARIFICATION_BEFORE_COMPARISON"},
        packet["human_approval_required"] is True,
    ]) else "FAIL"

    report_json = {
        "simulation_name": "Industrial Steel Utility Hook Simulation",
        "timestamp": FIXED_TIMESTAMP,
        "builder_input_summary": {
            "project_name": packet["project_name"],
            "material": packet["bom_items"][0]["material"],
            "quantity": packet["bom_items"][0]["quantity"],
            "safety_statement": packet["safety_notes"][0],
        },
        "generated_protocol_artifacts": [
            str(path.relative_to(SIM_ROOT)).replace("\\", "/") for path in required_artifacts if path.exists()
        ],
        "fabricator_capability_match_result": "PASS" if feasibility_review["capability_match"]["pass"] else "FAIL",
        "feasibility_result": feasibility_review["feasibility_status"],
        "quote_response_summary": {
            "quote_response_id": quote_response["quote_response_id"],
            "price_min": quote_response["price_min"],
            "price_max": quote_response["price_max"],
            "lead_time_min_days": quote_response["lead_time_min_days"],
            "lead_time_max_days": quote_response["lead_time_max_days"],
            "validation_result": "PASS" if quote_validation_pass else "FAIL",
            "comparison_status": comparison_responses[0]["comparison_status"],
            "informational_only": True,
        },
        "missing_information": feasibility_review["missing_information"],
        "risk_flags": feasibility_review["review_flags"],
        "guardrail_results": {
            "status": guardrail_audit["status"],
            "local_only_simulation": True,
            "no_external_action_authorized": True,
        },
        "telemetry_summary": {
            "stage_count": len(recorder.records),
            "actors": sorted({record.actor for record in recorder.records}),
        },
        "outcome_event_summary": {
            "outcome_event_id": outcome_event["outcome_event_id"],
            "event_type": outcome_event["event_type"],
            "delivery_status": outcome_event["delivery_status"],
        },
        "human_review_required": True,
        "engineering_review_required": True,
        "final_status": final_status,
    }
    report_md = render_simulation_report(report_json)
    report_json_path = OUTPUT_DIR / "simulation_report.json"
    report_md_path = OUTPUT_DIR / "simulation_report.md"
    write_json(report_json_path, report_json)
    write_text(report_md_path, report_md)

    print("Industrial Hook Simulation")
    print(f"Build packet validation: {'PASS' if not packet_errors else 'FAIL'}")
    print(f"Quote response validation: {'PASS' if quote_validation_pass else 'FAIL'}")
    print(f"Guardrail audit: {guardrail_audit['status']}")
    print(f"Final status: {final_status}")

    return (0 if final_status == "PASS" else 1), {
        "report_json_path": report_json_path,
        "report_md_path": report_md_path,
    }


def main() -> int:
    code, _ = run()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
