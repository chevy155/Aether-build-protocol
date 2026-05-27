from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

from generate_machine_response import build_response
from protocol_utils import (
    ROOT,
    build_quote_comparison_summary,
    build_quote_request,
    render_quote_comparison_summary,
    validate_payload,
    write_json,
    write_text,
)


SANDBOX_ROOT = ROOT / "transactions" / "print_job_sandbox"
DESIGNER_DIR = SANDBOX_ROOT / "designer_workspace"
AETHER_DIR = SANDBOX_ROOT / "aether_transaction"
SHOP_DIR = SANDBOX_ROOT / "shop_network"
SHOPS_DIR = SHOP_DIR / "shops"
QUOTES_DIR = SANDBOX_ROOT / "quotes"
NEGOTIATION_DIR = SANDBOX_ROOT / "negotiation"
FULFILLMENT_DIR = SANDBOX_ROOT / "fulfillment"
LEDGER_DIR = SANDBOX_ROOT / "ledger"
FIXED_DATE = "2026-05-27"
FIXED_ACTOR = "aether_print_transaction_sandbox"
FIXED_TIMESTAMPS = {
    "request": f"{FIXED_DATE}T00:00:00Z",
    "build_packet": f"{FIXED_DATE}T00:00:01Z",
    "quote_request": f"{FIXED_DATE}T00:00:02Z",
    "shop_match": f"{FIXED_DATE}T00:00:03Z",
    "quotes": f"{FIXED_DATE}T00:00:04Z",
    "negotiation_1": f"{FIXED_DATE}T00:00:05Z",
    "negotiation_2": f"{FIXED_DATE}T00:00:06Z",
    "fulfillment": f"{FIXED_DATE}T00:00:07Z",
    "delivery": f"{FIXED_DATE}T00:00:08Z",
    "outcome": f"{FIXED_DATE}T00:00:09Z",
    "closeout": f"{FIXED_DATE}T00:00:10Z",
}
FORBIDDEN_LABELS = {
    "winner",
    "selected shop",
    "approved vendor",
    "proceed to order",
    "approved to print",
}
TRANSACTION_STATES = [
    "REQUEST_CREATED",
    "BUILD_PACKET_CREATED",
    "QUOTE_REQUEST_CREATED",
    "SHOP_MATCH_SIMULATED",
    "QUOTE_RESPONSES_SIMULATED",
    "QUOTE_COMPARISON_CREATED",
    "HUMAN_APPROVAL_REQUIRED",
    "NEGOTIATION_SIMULATED",
    "WORK_ORDER_SIMULATED",
    "DELIVERY_SIMULATED",
    "OUTCOME_RECORDED",
    "CLOSED_LOCAL_ONLY",
]


def ensure_directories() -> None:
    for path in [
        DESIGNER_DIR,
        AETHER_DIR,
        SHOP_DIR,
        SHOPS_DIR,
        QUOTES_DIR,
        NEGOTIATION_DIR,
        FULFILLMENT_DIR,
        LEDGER_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def sha256_for_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_bom_csv(path: Path) -> None:
    rows = [
        ["item_id", "name", "category", "quantity", "unit", "material", "notes"],
        ["HOOK-001", "Wall-mounted cable hook body", "printed_part", "6", "ea", "PETG", "Simulation-only printed hook body"],
        ["HOOK-002", "Wall-mount hardware placeholder", "fastener_placeholder", "6", "ea", "unknown", "Fastener spec intentionally unresolved"],
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def build_design_request() -> dict[str, Any]:
    return {
        "requester_id": "designer_sandbox_001",
        "project_id": "m2m-print-hook-001",
        "project_name": "Wall-Mounted 3D Printed Cable Hook",
        "project_description": "A designer needs a small functional wall-mounted hook 3D printed for local protocol transaction simulation only.",
        "intended_use": "Cable management hook for light-duty interior organization review.",
        "quantity": 6,
        "target_material": "PETG",
        "acceptable_material_substitutions": [
            "Nylon PA12",
            "Carbon fiber nylon simulation only",
        ],
        "color_preference": "Matte black",
        "finish_preference": "Minimal support marks, light bead blast if SLS simulated",
        "dimensions_summary": {
            "height_mm": 72,
            "width_mm": 28,
            "depth_mm": 46,
            "wall_thickness_mm": 6,
        },
        "tolerance_requirement": "+/-0.4 mm",
        "strength_requirement": "Functional light-duty hook only; not load-rated and not safety-critical.",
        "mounting_method": "Two-screw wall mount with human review required for substrate and fastener selection.",
        "cad_manifest_reference": "transactions/print_job_sandbox/designer_workspace/mock_cad_manifest.json",
        "bom_reference": "transactions/print_job_sandbox/designer_workspace/bom.csv",
        "unknowns": [
            "real CAD file not provided",
            "load requirement not validated",
            "mounting substrate unknown",
            "fastener spec unknown",
            "print orientation not approved",
            "layer height preference unknown",
            "real shop not contacted",
        ],
        "assumptions": [
            "This remains a local-only machine-to-machine sandbox transaction.",
            "The hook is treated as a non-safety-critical plastic part pending human review.",
            "No real print order, payment, or delivery is authorized.",
        ],
        "human_approval_required": True,
    }


def build_mock_cad_manifest() -> dict[str, Any]:
    return {
        "manifest_id": "mock-cad-hook-001",
        "project_id": "m2m-print-hook-001",
        "cad_files": [
            {
                "file_name": "wall_mounted_cable_hook.step",
                "file_type": "manifest_only_step_reference",
                "provided": False,
                "notes": "Real CAD file not provided. Geometry is represented by manifest metadata only.",
            }
        ],
        "geometry_notes": [
            "Simulation-only cable hook geometry.",
            "No watertight mesh or real print file is included.",
            "No installation approval is implied.",
        ],
    }


def build_part_requirements() -> dict[str, Any]:
    return {
        "process_options": ["FDM", "SLS"],
        "material_options": ["PETG", "Nylon PA12", "Carbon fiber nylon simulation only"],
        "safety_statement": "This is not load-rated, not safety-critical, and not approved for real installation without human review.",
        "human_approval_required": True,
        "external_contact_authorized": False,
    }


def parse_bom_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_required_capabilities(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "project_id": request["project_id"],
        "required_processes": ["FDM", "SLS"],
        "required_materials": [request["target_material"], *request["acceptable_material_substitutions"]],
        "tolerance_requirement": request["tolerance_requirement"],
        "needs_engineering_review_for_load_bearing": True,
        "requires_human_review": True,
        "forbidden_actions": [
            "contact_supplier",
            "route_quote",
            "approve_fabrication",
            "approve_payment",
            "certify_load_rating",
        ],
    }


def map_build_packet(request: dict[str, Any], bom_rows: list[dict[str, str]]) -> dict[str, Any]:
    bom_items = []
    for row in bom_rows:
        bom_items.append(
            {
                "item_id": row["item_id"],
                "name": row["name"],
                "category": row["category"],
                "quantity": int(row["quantity"]),
                "unit": row["unit"],
                "material": row["material"],
                "dimensions": request["dimensions_summary"] if row["item_id"] == "HOOK-001" else {"pending_review": row["notes"]},
                "finish": request["finish_preference"],
                "supplier_preference": "No real shop selected; sandbox review only",
                "substitution_allowed": row["item_id"] == "HOOK-001",
                "notes": row["notes"],
            }
        )

    return {
        "protocol_version": "0.2.8",
        "project_id": request["project_id"],
        "project_name": request["project_name"],
        "project_type": "m2m_print_transaction_sandbox",
        "project_description": request["project_description"],
        "design_files": [
            {
                "file_name": "wall_mounted_cable_hook.step",
                "file_type": "manifest_only_step_reference",
                "path": request["cad_manifest_reference"],
                "notes": "Manifest-only geometry reference. No real CAD file provided.",
            }
        ],
        "geometry_summary": "Wall-mounted cable hook for local 3D print transaction simulation, represented by manifest metadata only.",
        "bom_items": bom_items,
        "material_specs": [
            request["target_material"],
            "Nylon PA12 permitted as reviewed substitution.",
            "Carbon fiber nylon is simulation-only and requires engineering review before any real interpretation.",
        ],
        "finish_requirements": [
            request["finish_preference"],
            "No cosmetic or structural approval is implied.",
        ],
        "dimensions": request["dimensions_summary"],
        "tolerances": [
            f"Target tolerance: {request['tolerance_requirement']}",
            "Print orientation remains unapproved.",
        ],
        "site_conditions": [
            "Local-only print transaction sandbox.",
            "No real shop contacted.",
            "No real installation authorized.",
        ],
        "location_context": {
            "transaction_mode": "local_only_sandbox",
            "part_category": "3d_printed_hook",
            "intended_environment": "interior_light_duty_review_only",
            "external_action_authorized": False,
        },
        "quote_categories": ["3d_printing", "prototype_review", "material_option_review"],
        "capability_requirements": [
            {
                "capability_id": "fdm_printing",
                "capability_type": "additive_manufacturing",
                "required_for": "Baseline PETG production path",
                "description": "FDM simulation path for PETG prototype production review.",
                "licensed_trade": False,
                "certification_required": False,
                "local_required": True,
                "risk_level": "medium",
                "notes": "No real print may proceed without human review.",
            },
            {
                "capability_id": "sls_printing",
                "capability_type": "additive_manufacturing",
                "required_for": "Nylon PA12 option review",
                "description": "SLS simulation path for stronger nylon substitution review.",
                "licensed_trade": False,
                "certification_required": False,
                "local_required": True,
                "risk_level": "medium",
                "notes": "Substitution review is informational only.",
            },
            {
                "capability_id": "engineering_review",
                "capability_type": "review",
                "required_for": "Any load-bearing interpretation or carbon fiber nylon consideration",
                "description": "Engineering review remains required for any real-world stiffness or load interpretation.",
                "licensed_trade": False,
                "certification_required": False,
                "local_required": True,
                "risk_level": "high",
                "notes": "No engineering approval is granted inside the sandbox.",
            },
        ],
        "install_scope": "No real installation authorized. Internal review only.",
        "licensed_trade_required": False,
        "code_review_required": False,
        "permit_review_required": False,
        "safety_notes": [
            "Not load-rated.",
            "Not safety-critical.",
            "No real installation without human review.",
        ],
        "unknowns": request["unknowns"],
        "assumptions": request["assumptions"],
        "human_approval_required": True,
    }


def build_human_approval_event(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "human_approval_event_id": "approval-m2m-print-hook-001",
        "project_id": request["project_id"],
        "timestamp": FIXED_TIMESTAMPS["quote_request"],
        "actor": "internal_review_board",
        "decision": "approved_for_internal_review_only",
        "approved_actions": ["internal_review", "local_artifact_generation", "simulated_quote_analysis"],
        "not_approved_actions": [
            "external quote routing",
            "real shop contact",
            "fabrication",
            "payment",
            "delivery",
            "installation",
            "engineering",
            "load certification",
        ],
        "scope_limitations": [
            "No external RFQ distribution.",
            "No physical print order.",
            "No supplier or shop contact.",
        ],
        "human_approval_required_for_next_stage": True,
        "sandbox_only": True,
    }


def build_transaction_state() -> dict[str, Any]:
    return {
        "states": TRANSACTION_STATES,
        "current_state": "CLOSED_LOCAL_ONLY",
        "human_approval_required": True,
        "external_action_taken": False,
    }


def build_shop_profiles() -> list[dict[str, Any]]:
    return [
        {
            "shop_id": "shop_profile_001",
            "shop_name": "Pacific Layer Works",
            "shop_type": "fake_additive_shop",
            "capabilities": ["FDM", "rapid_prototyping"],
            "materials_supported": ["PETG", "PLA", "ASA"],
            "max_part_size": {"x_mm": 220, "y_mm": 220, "z_mm": 250},
            "tolerance_capability": "+/-0.4 mm",
            "finish_options": ["standard FDM", "vapor smoothing simulation"],
            "lead_time_range_days": [2, 5],
            "minimum_order_quantity": 1,
            "requires_engineering_review_for_load_bearing_parts": False,
            "can_certify_load_rating": False,
            "sandbox_only": True,
            "external_contacted": False,
            "strength": "fast local prototyping",
            "limitations": ["no SLS", "no engineering certification"],
        },
        {
            "shop_id": "shop_profile_002",
            "shop_name": "Northstar Additive Lab",
            "shop_type": "fake_additive_shop",
            "capabilities": ["SLS", "batch_production"],
            "materials_supported": ["Nylon PA12"],
            "max_part_size": {"x_mm": 340, "y_mm": 340, "z_mm": 600},
            "tolerance_capability": "+/-0.35 mm",
            "finish_options": ["bead blast", "dyed black simulation"],
            "lead_time_range_days": [6, 10],
            "minimum_order_quantity": 3,
            "requires_engineering_review_for_load_bearing_parts": False,
            "can_certify_load_rating": False,
            "sandbox_only": True,
            "external_contacted": False,
            "strength": "stronger nylon options",
            "limitations": ["longer lead time"],
        },
        {
            "shop_id": "shop_profile_003",
            "shop_name": "Apex Composite Print",
            "shop_type": "fake_additive_shop",
            "capabilities": ["FDM", "composite_print_simulation"],
            "materials_supported": ["Carbon fiber nylon simulation only"],
            "max_part_size": {"x_mm": 300, "y_mm": 300, "z_mm": 300},
            "tolerance_capability": "+/-0.45 mm",
            "finish_options": ["standard composite simulation finish"],
            "lead_time_range_days": [5, 8],
            "minimum_order_quantity": 1,
            "requires_engineering_review_for_load_bearing_parts": True,
            "can_certify_load_rating": False,
            "sandbox_only": True,
            "external_contacted": False,
            "strength": "high stiffness material options",
            "limitations": ["requires engineering review", "no load certification in sandbox"],
        },
    ]


def build_shop_match_results(required_capabilities: dict[str, Any], shops: list[dict[str, Any]]) -> dict[str, Any]:
    matches = []
    for shop in shops:
        material_match = any(material in shop["materials_supported"] for material in required_capabilities["required_materials"])
        process_match = any(process in shop["capabilities"] for process in required_capabilities["required_processes"])
        tolerance_match = shop["tolerance_capability"] in {"+/-0.4 mm", "+/-0.35 mm", "+/-0.45 mm"}
        lead_time_max = shop["lead_time_range_days"][1]
        lead_time_fit = lead_time_max <= 8
        score = 30
        if material_match:
            score += 30
        if process_match:
            score += 20
        if tolerance_match:
            score += 10
        if lead_time_fit:
            score += 10
        risk_flags = []
        missing_info = [
            "load requirement not validated",
            "mounting substrate unknown",
            "fastener spec unknown",
        ]
        if shop["requires_engineering_review_for_load_bearing_parts"]:
            risk_flags.append("engineering_review_required_for_any_structural_interpretation")
        if not material_match:
            risk_flags.append("target_material_not_natively_supported")
        if not lead_time_fit:
            risk_flags.append("lead_time_longer_than_initial_target")
        if shop["shop_id"] == "shop_profile_001":
            label = "MOST_COMPLETE_FOR_HUMAN_REVIEW"
        elif material_match:
            label = "NEEDS_CLARIFICATION"
        else:
            label = "NOT_READY_FOR_REAL_RFQ"
        matches.append(
            {
                "shop_id": shop["shop_id"],
                "shop_name": shop["shop_name"],
                "capability_match_score": score,
                "material_match": material_match,
                "tolerance_match": tolerance_match,
                "lead_time_fit": lead_time_fit,
                "risk_flags": risk_flags,
                "missing_info": missing_info,
                "human_review_required": True,
                "external_contacted": False,
                "label": label,
            }
        )
    return {
        "project_id": "m2m-print-hook-001",
        "comparison_mode": "local_only_fake_shop_matching",
        "matches": matches,
        "selection_status": "no shop selected",
        "guardrail_note": "Fake shop matching only. No winner, vendor selection, or order approval is produced.",
    }


def build_quote_responses(quote_request: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "quote_response_id": "quote_response_001",
            "quote_request_id": quote_request["quote_request_id"],
            "responder_name": "Pacific Layer Works",
            "responder_type": "fake_shop_profile",
            "quoted_scope": "Informational only PETG FDM prototype run for six non-load-rated cable hooks with standard cleanup and packaging simulation.",
            "price_min": 42.0,
            "price_max": 68.0,
            "currency": "USD",
            "lead_time_min_days": 2,
            "lead_time_max_days": 5,
            "assumptions": [
                "PETG is acceptable.",
                "No real CAD repair is required.",
                "Mounting hardware remains outside print scope.",
                "Informational only; no real quote issued.",
            ],
            "exclusions": [
                "No shop contacted.",
                "No print authorized.",
                "No payment authorized.",
                "No engineering review or load certification.",
            ],
            "substitutions": ["PLA possible for visual fit-check only; not recommended for final use."],
            "confidence_score": 0.86,
            "risk_notes": [
                "Mounting substrate remains unknown.",
                "Hook orientation needs human approval.",
            ],
            "clarification_questions": [
                "Should PETG remain the baseline material?",
                "What wall anchor system is intended?",
            ],
            "human_review_required": True,
            "external_action_taken": False,
            "sandbox_only": True,
        },
        {
            "quote_response_id": "quote_response_002",
            "quote_request_id": quote_request["quote_request_id"],
            "responder_name": "Northstar Additive Lab",
            "responder_type": "fake_shop_profile",
            "quoted_scope": "Informational only Nylon PA12 SLS production simulation for six cable hooks with stronger material option and batch-friendly setup assumptions.",
            "price_min": 88.0,
            "price_max": 126.0,
            "currency": "USD",
            "lead_time_min_days": 6,
            "lead_time_max_days": 10,
            "assumptions": [
                "Nylon PA12 substitution is acceptable.",
                "Longer lead time is acceptable for stronger material review.",
                "Informational only; no real quote issued.",
            ],
            "exclusions": [
                "No shop contacted.",
                "No print authorized.",
                "No payment authorized.",
                "No shipping commitment.",
            ],
            "substitutions": ["Black dye finish may be simulated for appearance only."],
            "confidence_score": 0.81,
            "risk_notes": [
                "Lead time increases for SLS batching.",
                "Fastener and substrate assumptions remain unresolved.",
            ],
            "clarification_questions": [
                "Is Nylon PA12 preferred over PETG for the functional review?",
                "Is surface finish or strength the higher priority?",
            ],
            "human_review_required": True,
            "external_action_taken": False,
            "sandbox_only": True,
        },
        {
            "quote_response_id": "quote_response_003",
            "quote_request_id": quote_request["quote_request_id"],
            "responder_name": "Apex Composite Print",
            "responder_type": "fake_shop_profile",
            "quoted_scope": "Informational only carbon fiber nylon simulation for stiffness review with explicit engineering escalation before any real interpretation.",
            "price_min": 104.0,
            "price_max": 154.0,
            "currency": "USD",
            "lead_time_min_days": 5,
            "lead_time_max_days": 8,
            "assumptions": [
                "Carbon fiber nylon remains simulation-only.",
                "Engineering review is required before any real structural interpretation.",
                "Informational only; no real quote issued.",
            ],
            "exclusions": [
                "No shop contacted.",
                "No print authorized.",
                "No payment authorized.",
                "No load certification provided.",
            ],
            "substitutions": ["Nylon PA12 recommended if engineering review is not available."],
            "confidence_score": 0.74,
            "risk_notes": [
                "Engineering review required.",
                "No load certification available in sandbox.",
            ],
            "clarification_questions": [
                "Is the stiffness review worth the additional engineering gate?",
                "Does the designer want to avoid composite-material assumptions?",
            ],
            "human_review_required": True,
            "external_action_taken": False,
            "sandbox_only": True,
        },
    ]


def build_negotiation_events(quote_request: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    event_1 = {
        "negotiation_event_id": "negotiation_event_001",
        "actor": "designer",
        "event_type": "clarification_requested",
        "timestamp": FIXED_TIMESTAMPS["negotiation_1"],
        "change_summary": "Designer asks whether PETG can be substituted with Nylon PA12 for better durability.",
        "before": {"target_material": "PETG", "lead_time_range_days": [2, 5]},
        "after": {"candidate_material": "Nylon PA12", "quote_review_status": "clarification_pending"},
        "human_approval_required": True,
        "external_action_taken": False,
        "sandbox_only": True,
    }
    event_2 = {
        "negotiation_event_id": "negotiation_event_002",
        "actor": "simulated_shop_response",
        "event_type": "clarification_response",
        "timestamp": FIXED_TIMESTAMPS["negotiation_2"],
        "change_summary": "Simulated shop response says Nylon PA12 is possible but requires higher cost and longer lead time.",
        "before": {"material_option": "PETG", "price_range": [42.0, 68.0], "lead_time_range_days": [2, 5]},
        "after": {"material_option": "Nylon PA12", "price_range": [88.0, 126.0], "lead_time_range_days": [6, 10]},
        "human_approval_required": True,
        "external_action_taken": False,
        "sandbox_only": True,
    }
    summary = {
        "project_id": "m2m-print-hook-001",
        "quote_request_id": quote_request["quote_request_id"],
        "events": [event_1["negotiation_event_id"], event_2["negotiation_event_id"]],
        "summary": "Negotiation remained simulated only. Nylon PA12 is feasible for review but increases cost and lead time.",
        "human_review_required": True,
        "external_action_taken": False,
        "sandbox_only": True,
    }
    return [event_1, event_2], summary


def build_fulfillment_artifacts() -> dict[str, dict[str, Any]]:
    work_order = {
        "work_order_id": "simulated_work_order_001",
        "project_id": "m2m-print-hook-001",
        "status": "simulation_only_not_authorized",
        "notes": [
            "Simulation only.",
            "No real work authorized.",
            "Human approval remains required for any external execution.",
        ],
        "sandbox_only": True,
        "external_action_taken": False,
    }
    print_status = {
        "print_status_id": "simulated_print_status_001",
        "project_id": "m2m-print-hook-001",
        "status": "simulated_complete",
        "progress_percent": 100,
        "notes": ["Synthetic print completion event.", "No real printer was used."],
        "sandbox_only": True,
        "external_action_taken": False,
    }
    delivery_event = {
        "delivery_event_id": "simulated_delivery_event_001",
        "project_id": "m2m-print-hook-001",
        "status": "simulated_delivery_only",
        "notes": ["No real delivery occurred.", "No shipment was booked or fulfilled."],
        "sandbox_only": True,
        "external_action_taken": False,
    }
    outcome_event = {
        "outcome_event_id": "outcome_event_001",
        "project_id": "m2m-print-hook-001",
        "quote_response_id": "quote_response_001",
        "event_type": "simulated_transaction_outcome",
        "timestamp": FIXED_TIMESTAMPS["outcome"],
        "actor": FIXED_ACTOR,
        "cost_actual": 55.0,
        "timeline_actual_days": 4,
        "quality_score": 0.88,
        "inspection_status": "simulated_pass_not_real_inspection",
        "delivery_status": "simulated_received_not_real_delivery",
        "dispute_status": "none",
        "lessons_learned": [
            "Material substitutions need explicit human review.",
            "Shop profile matching is useful only for internal sandbox analysis.",
        ],
        "trust_signal": "sandbox_only_informational_outcome",
        "sandbox_only": True,
        "external_action_taken": False,
    }
    return {
        "work_order": work_order,
        "print_status": print_status,
        "delivery_event": delivery_event,
        "outcome_event": outcome_event,
    }


def build_transaction_manifest(paths: list[Path]) -> dict[str, Any]:
    return {
        "manifest_id": "print-transaction-manifest-001",
        "project_id": "m2m-print-hook-001",
        "artifact_count": len(paths),
        "artifacts": [relative_path(path) for path in paths],
        "sandbox_only": True,
    }


def write_transaction_event_log() -> None:
    records = [
        {
            "timestamp": FIXED_TIMESTAMPS["request"],
            "event_type": "REQUEST_CREATED",
            "actor": FIXED_ACTOR,
            "status": "PASS",
            "external_action_taken": False,
        },
        {
            "timestamp": FIXED_TIMESTAMPS["build_packet"],
            "event_type": "BUILD_PACKET_CREATED",
            "actor": FIXED_ACTOR,
            "status": "PASS",
            "external_action_taken": False,
        },
        {
            "timestamp": FIXED_TIMESTAMPS["shop_match"],
            "event_type": "SHOP_MATCH_SIMULATED",
            "actor": FIXED_ACTOR,
            "status": "PASS",
            "external_action_taken": False,
        },
        {
            "timestamp": FIXED_TIMESTAMPS["quotes"],
            "event_type": "QUOTE_RESPONSES_SIMULATED",
            "actor": FIXED_ACTOR,
            "status": "PASS",
            "external_action_taken": False,
        },
        {
            "timestamp": FIXED_TIMESTAMPS["closeout"],
            "event_type": "CLOSED_LOCAL_ONLY",
            "actor": FIXED_ACTOR,
            "status": "PASS",
            "external_action_taken": False,
        },
    ]
    lines = [json.dumps(record) for record in records]
    write_text(LEDGER_DIR / "transaction_event_log.jsonl", "\n".join(lines) + "\n")


def write_provenance_manifest(paths: list[Path]) -> dict[str, Any]:
    manifest = {
        "manifest_id": "print-transaction-provenance-001",
        "record_count": len(paths),
        "records": [
            {
                "path": relative_path(path),
                "sha256": sha256_for_path(path),
            }
            for path in paths
        ],
    }
    write_json(LEDGER_DIR / "provenance_manifest.json", manifest)
    return manifest


def write_guardrail_audit(match_results: dict[str, Any], human_approval_event: dict[str, Any]) -> dict[str, Any]:
    labels = {entry["label"].lower() for entry in match_results["matches"]}
    audit = {
        "status": "PASS",
        "no_email_sent": True,
        "no_webhook_called": True,
        "no_real_shop_contacted": True,
        "no_quote_routed": True,
        "no_shop_selected": match_results["selection_status"] == "no shop selected",
        "no_print_approved": True,
        "no_fabrication_approved": True,
        "no_payment_approved": True,
        "no_delivery_approved": True,
        "no_engineering_approval": True,
        "no_load_certification": True,
        "human_approval_required": human_approval_event["human_approval_required_for_next_stage"],
        "local_only_sandbox": True,
        "forbidden_labels_present": sorted(label for label in labels if label in FORBIDDEN_LABELS),
    }
    write_json(LEDGER_DIR / "guardrail_audit.json", audit)
    return audit


def render_closeout_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Transaction Closeout Report",
        "",
        f"**Project:** {summary['project_id']}  ",
        f"**Status:** {summary['status']}  ",
        f"**Current State:** {summary['current_state']}  ",
        "**Mode:** local_only_sandbox",
        "",
        "## Summary",
        "",
        "- Designer request captured and mapped into a valid Build Packet.",
        "- Fake shop profiles matched for human review only.",
        "- Quote responses, negotiation, fulfillment, and outcome remained simulation-only.",
        "- Human approval remained required and no external action occurred.",
        "",
        "## Guardrails",
        "",
        "- No email sent",
        "- No webhook called",
        "- No real shop contacted",
        "- No winner selected",
        "- No print or fabrication approved",
        "- No payment, delivery, engineering approval, or load certification",
        "",
        "## Machine Responses",
        "",
    ]
    lines.extend(f"- {item['response_type']} / {item['status']} / {item['request_echo']['code']}" for item in summary["machine_responses"])
    return "\n".join(lines) + "\n"


def write_transaction_readme() -> None:
    text = """# Machine-to-Machine Print Transaction Sandbox

This sandbox simulates a designer-to-shop machine-to-machine print transaction for a wall-mounted 3D printed cable hook.

- local-only
- fake shops only
- no external action
- no shop contacted
- no payment
- no print approval
- no fabrication approval
- no delivery approval
- no engineering approval
- human approval required

Run from repo root:

```powershell
python scripts/simulate_print_transaction.py
```
"""
    write_text(SANDBOX_ROOT / "README.md", text)


def main() -> int:
    ensure_directories()
    write_transaction_readme()

    design_request = build_design_request()
    mock_cad_manifest = build_mock_cad_manifest()
    part_requirements = build_part_requirements()

    design_request_path = DESIGNER_DIR / "design_request.json"
    mock_cad_manifest_path = DESIGNER_DIR / "mock_cad_manifest.json"
    part_requirements_path = DESIGNER_DIR / "part_requirements.yaml"
    bom_path = DESIGNER_DIR / "bom.csv"

    write_json(design_request_path, design_request)
    write_json(mock_cad_manifest_path, mock_cad_manifest)
    write_yaml(part_requirements_path, part_requirements)
    write_bom_csv(bom_path)

    bom_rows = parse_bom_rows(bom_path)
    build_packet = map_build_packet(design_request, bom_rows)
    build_packet_errors = validate_payload(build_packet, "build_packet.schema.json")
    if build_packet_errors:
        print("Build Packet validation failed")
        for item in build_packet_errors:
            print(item)
        return 1

    quote_request = build_quote_request(build_packet)
    quote_request["exclusions_to_state"].extend(
        [
            "Real shop contact",
            "Real print authorization",
            "Payment authorization",
            "Delivery authorization",
        ]
    )
    required_capabilities = build_required_capabilities(design_request)
    human_approval_event = build_human_approval_event(design_request)
    transaction_state = build_transaction_state()

    build_packet_path = AETHER_DIR / "build_packet.yaml"
    quote_request_path = AETHER_DIR / "quote_request.json"
    required_capabilities_path = AETHER_DIR / "required_capabilities.json"
    human_approval_event_path = AETHER_DIR / "human_approval_event.json"
    transaction_state_path = AETHER_DIR / "transaction_state.json"

    write_yaml(build_packet_path, build_packet)
    write_json(quote_request_path, quote_request)
    write_json(required_capabilities_path, required_capabilities)
    write_json(human_approval_event_path, human_approval_event)
    write_json(transaction_state_path, transaction_state)

    shops = build_shop_profiles()
    for shop in shops:
        write_json(SHOPS_DIR / f"{shop['shop_id']}.json", shop)
    match_results = build_shop_match_results(required_capabilities, shops)
    write_json(SHOP_DIR / "shop_match_results.json", match_results)

    quote_responses = build_quote_responses(quote_request)
    for quote_response in quote_responses:
        schema_errors = validate_payload(quote_response, "quote_response.schema.json")
        if schema_errors:
            print(f"Quote response validation failed for {quote_response['quote_response_id']}")
            for item in schema_errors:
                print(item)
            return 1
        write_json(QUOTES_DIR / f"{quote_response['quote_response_id']}.json", quote_response)

    comparison_summary = build_quote_comparison_summary(quote_responses)
    write_json(QUOTES_DIR / "quote_comparison_summary.json", comparison_summary)
    write_text(QUOTES_DIR / "quote_comparison_summary.md", render_quote_comparison_summary(comparison_summary))

    negotiation_events, negotiation_summary = build_negotiation_events(quote_request)
    for event in negotiation_events:
        write_json(NEGOTIATION_DIR / f"{event['negotiation_event_id']}.json", event)
    write_json(NEGOTIATION_DIR / "negotiation_summary.json", negotiation_summary)

    fulfillment = build_fulfillment_artifacts()
    write_json(FULFILLMENT_DIR / "simulated_work_order.json", fulfillment["work_order"])
    write_json(FULFILLMENT_DIR / "simulated_print_status.json", fulfillment["print_status"])
    write_json(FULFILLMENT_DIR / "simulated_delivery_event.json", fulfillment["delivery_event"])
    write_json(FULFILLMENT_DIR / "outcome_event.json", fulfillment["outcome_event"])

    write_transaction_event_log()

    machine_responses = [
        build_response("VALIDATION_PASSED", "validate_build_packet", design_request["project_id"]),
        build_response("HUMAN_APPROVAL_REQUIRED", "external_release", quote_request["quote_request_id"]),
        build_response("EXTERNAL_ACTION_FORBIDDEN", "contact_supplier", design_request["project_id"]),
        build_response("ENGINEERING_REVIEW_REQUIRED", "engineering_review", design_request["project_id"]),
        build_response("LOAD_CERTIFICATION_NOT_PROVIDED", "load_certification", design_request["project_id"]),
    ]
    machine_response_path = LEDGER_DIR / "machine_response_envelopes.json"
    write_json(machine_response_path, {"responses": machine_responses})

    artifact_paths = [
        design_request_path,
        mock_cad_manifest_path,
        part_requirements_path,
        bom_path,
        build_packet_path,
        quote_request_path,
        required_capabilities_path,
        human_approval_event_path,
        transaction_state_path,
        *(SHOPS_DIR / f"{shop['shop_id']}.json" for shop in shops),
        SHOP_DIR / "shop_match_results.json",
        *(QUOTES_DIR / f"{quote_response['quote_response_id']}.json" for quote_response in quote_responses),
        QUOTES_DIR / "quote_comparison_summary.json",
        NEGOTIATION_DIR / "negotiation_event_001.json",
        NEGOTIATION_DIR / "negotiation_event_002.json",
        NEGOTIATION_DIR / "negotiation_summary.json",
        FULFILLMENT_DIR / "simulated_work_order.json",
        FULFILLMENT_DIR / "simulated_print_status.json",
        FULFILLMENT_DIR / "simulated_delivery_event.json",
        FULFILLMENT_DIR / "outcome_event.json",
        LEDGER_DIR / "transaction_event_log.jsonl",
        machine_response_path,
    ]

    transaction_manifest = build_transaction_manifest(artifact_paths)
    transaction_manifest_path = AETHER_DIR / "transaction_manifest.json"
    write_json(transaction_manifest_path, transaction_manifest)
    artifact_paths.append(transaction_manifest_path)

    provenance_manifest = write_provenance_manifest(artifact_paths)
    guardrail_audit = write_guardrail_audit(match_results, human_approval_event)

    closeout_report = {
        "project_id": design_request["project_id"],
        "status": "PASS",
        "current_state": transaction_state["current_state"],
        "artifact_count": len(artifact_paths),
        "machine_responses": machine_responses,
        "guardrail_audit": guardrail_audit,
        "provenance_record_count": provenance_manifest["record_count"],
        "external_action_taken": False,
        "human_approval_required": True,
    }
    write_json(LEDGER_DIR / "transaction_closeout_report.json", closeout_report)
    write_text(LEDGER_DIR / "transaction_closeout_report.md", render_closeout_report(closeout_report))

    print("Print transaction sandbox status: PASS")
    print(f"Wrote: {SANDBOX_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())