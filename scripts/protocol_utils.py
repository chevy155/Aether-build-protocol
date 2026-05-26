from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "protocols" / "build_intent" / "schemas"
EXAMPLE_DIR = ROOT / "examples" / "sauna_node"
OUTPUT_DIR = ROOT / "outputs"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_schema(name: str) -> dict[str, Any]:
    return load_json(SCHEMA_DIR / name)


def validate_payload(payload: dict[str, Any], schema_name: str) -> list[str]:
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(payload), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{path}: {error.message}")
    return errors


def build_quote_request(packet: dict[str, Any]) -> dict[str, Any]:
    categories = packet["quote_categories"]
    capabilities = [item["capability_id"] for item in packet["capability_requirements"]]

    risk_questions = []
    if packet.get("licensed_trade_required"):
      risk_questions.append("Which portions of scope require licensed trade execution or signoff?")
    if packet.get("code_review_required"):
      risk_questions.append("What code review or setback concerns must be resolved before final pricing?")
    if packet.get("permit_review_required"):
      risk_questions.append("What permit pathway, inspections, or local authority reviews are required?")
    risk_questions.extend(
        [
            "What site conditions could materially change price or lead time?",
            "Which assumptions would you need confirmed before firm pricing?",
        ]
    )

    return {
        "quote_request_id": f"rfq-{packet['project_id']}",
        "project_id": packet["project_id"],
        "scope_summary": packet["project_description"],
        "requested_quote_categories": categories,
        "required_capabilities": capabilities,
        "deliverables": [
            "Budgetary price range",
            "Lead time range",
            "Assumptions list",
            "Exclusions list",
            "Clarification questions",
            "Risk notes",
        ],
        "location_context": packet["location_context"],
        "desired_timeline": {
            "target_start_window": "2026-Q3",
            "pricing_stage": "budgetary_review",
        },
        "required_response_fields": [
            "price_min",
            "price_max",
            "lead_time_min_days",
            "lead_time_max_days",
            "assumptions",
            "exclusions",
            "substitutions",
            "confidence_score",
            "risk_notes",
            "clarification_questions",
        ],
        "assumptions_to_confirm": packet.get("assumptions", []) + packet.get("unknowns", []),
        "exclusions_to_state": [
            "Engineering approval",
            "Permit issuance",
            "Construction approval",
            "Autonomous procurement",
        ],
        "risk_questions": risk_questions,
        "human_approval_required": True,
    }


def compute_quote_readiness_score(quote_response: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "assumptions": bool(quote_response.get("assumptions")),
        "exclusions": bool(quote_response.get("exclusions")),
        "price_range": quote_response.get("price_min") is not None and quote_response.get("price_max") is not None,
        "lead_time": quote_response.get("lead_time_min_days") is not None and quote_response.get("lead_time_max_days") is not None,
        "confidence": quote_response.get("confidence_score") is not None,
        "substitutions": bool(quote_response.get("substitutions")),
        "risk_notes": bool(quote_response.get("risk_notes")),
        "clarification_questions": bool(quote_response.get("clarification_questions")),
    }
    met = sum(1 for ok in checks.values() if ok)
    score = round((met / len(checks)) * 100, 1)
    is_clean = met == len(checks)
    missing = [name for name, ok in checks.items() if not ok]
    return {
        "score": score,
        "is_clean_for_comparison": is_clean,
        "checks": checks,
        "missing_comparison_fields": missing,
    }


def evaluate_quote_response(quote_response: dict[str, Any], schema_errors: list[str]) -> dict[str, Any]:
    readiness = compute_quote_readiness_score(quote_response)
    confidence_score = quote_response.get("confidence_score")
    low_confidence = confidence_score is None or confidence_score < 0.6
    human_review_missing = quote_response.get("human_review_required") is not True
    blocking_flags = []
    if readiness["missing_comparison_fields"]:
        blocking_flags.extend(readiness["missing_comparison_fields"])
    if low_confidence:
        blocking_flags.append("low_confidence_score")
    if human_review_missing:
        blocking_flags.append("human_review_required_not_true")
    if schema_errors:
        blocking_flags.append("schema_validation_failed")

    return {
        "readiness": readiness,
        "low_confidence": low_confidence,
        "human_review_missing": human_review_missing,
        "confidence_score": confidence_score,
        "blocking_flags": blocking_flags,
        "pass": not blocking_flags and not schema_errors,
    }


def score_build_packet_quote_readiness(packet: dict[str, Any], schema_errors: list[str]) -> dict[str, Any]:
    categories = {
        "required_fields_present": 16 if not schema_errors else 0,
        "bom_completeness": 10 if packet.get("bom_items") else 0,
        "dimensions_and_tolerances": 10 if packet.get("dimensions") and packet.get("tolerances") else 0,
        "site_conditions": 8 if packet.get("site_conditions") else 0,
        "licensed_trade_flags": 7 if "licensed_trade_required" in packet else 0,
        "code_permit_review_flags": 7 if "code_review_required" in packet and "permit_review_required" in packet else 0,
        "safety_notes": 8 if packet.get("safety_notes") else 0,
        "unknowns_preserved": 8 if packet.get("unknowns") else 0,
        "assumptions_present": 6 if packet.get("assumptions") else 0,
        "capability_requirements": 8 if packet.get("capability_requirements") else 0,
        "quote_categories": 6 if packet.get("quote_categories") else 0,
        "human_approval_gate": 6 if packet.get("human_approval_required") is True else 0,
    }
    total = sum(categories.values())
    if schema_errors or total < 60:
        status = "NOT_READY_FOR_QUOTE_REVIEW"
    elif total < 85:
        status = "NEEDS_HUMAN_COMPLETION_BEFORE_QUOTE_REVIEW"
    else:
        status = "READY_FOR_HUMAN_QUOTE_REVIEW"
    gaps = [name for name, score in categories.items() if score == 0]
    return {
        "score": total,
        "status": status,
        "category_scores": categories,
        "schema_errors": schema_errors,
        "gaps": gaps,
        "approved_to_build": False,
    }


def render_build_packet_quote_readiness_report(packet: dict[str, Any], result: dict[str, Any]) -> str:
    lines = [
        "# Quote Readiness Score",
        "",
        f"**Project:** {packet.get('project_name', 'unknown')}  ",
        f"**Project ID:** {packet.get('project_id', 'unknown')}  ",
        f"**Score:** {result['score']} / 100  ",
        f"**Status:** {result['status']}  ",
        "**Note:** This score does not approve the project to build.",
        "",
        "## Category Scores",
        "",
    ]
    for name, score in result["category_scores"].items():
        lines.append(f"- {name}: {score}")
    lines.extend(["", "## Gaps", ""])
    if result["gaps"]:
        lines.extend(f"- {gap}" for gap in result["gaps"])
    else:
        lines.append("- None")
    lines.extend(["", "## Schema Errors", ""])
    if result["schema_errors"]:
        lines.extend(f"- {item}" for item in result["schema_errors"])
    else:
        lines.append("- No schema errors")
    return "\n".join(lines) + "\n"


def build_quote_response_validation_report(quote_response: dict[str, Any], schema_errors: list[str]) -> str:
    evaluation = evaluate_quote_response(quote_response, schema_errors)
    assessment = evaluation["readiness"]
    status = "PASS" if evaluation["pass"] else "FAIL"
    comparison_status = "CLEAN" if assessment["is_clean_for_comparison"] and not evaluation["blocking_flags"] else "NOT CLEAN ENOUGH TO COMPARE"

    lines = [
        "# Quote Response Validation Report",
        "",
        f"**Quote Response ID:** {quote_response.get('quote_response_id', 'unknown')}  ",
        f"**Quote Request ID:** {quote_response.get('quote_request_id', 'unknown')}  ",
        f"**Result:** {status}  ",
        f"**Schema Validation:** {'PASS' if not schema_errors else 'FAIL'}  ",
        f"**Quote-Readiness Score:** {assessment['score']} / 100  ",
        f"**Comparison Status:** {comparison_status}  ",
        f"**Human Review Required:** {quote_response.get('human_review_required')}  ",
        f"**Confidence Score:** {quote_response.get('confidence_score')}",
        "",
        "## Required Comparison Fields",
        "",
        f"- Assumptions stated: {assessment['checks']['assumptions']}",
        f"- Exclusions stated: {assessment['checks']['exclusions']}",
        f"- Price range stated: {assessment['checks']['price_range']}",
        f"- Lead time stated: {assessment['checks']['lead_time']}",
        f"- Confidence stated: {assessment['checks']['confidence']}",
        f"- Substitutions stated: {assessment['checks']['substitutions']}",
        f"- Risk notes stated: {assessment['checks']['risk_notes']}",
        f"- Clarification questions stated: {assessment['checks']['clarification_questions']}",
        f"- Low confidence score flagged: {evaluation['low_confidence']}",
        f"- Human review requirement not true: {evaluation['human_review_missing']}",
        "",
        "## Missing Comparison Fields",
        "",
    ]

    if assessment["missing_comparison_fields"]:
        lines.extend(f"- {item}" for item in assessment["missing_comparison_fields"])
    else:
        lines.append("- None")

    lines.extend(["", "## Blocking Flags", ""])
    if evaluation["blocking_flags"]:
        lines.extend(f"- {item}" for item in evaluation["blocking_flags"])
    else:
        lines.append("- None")

    lines.extend(["", "## Schema Errors", ""])
    if schema_errors:
        lines.extend(f"- {item}" for item in schema_errors)
    else:
        lines.append("- No schema errors")

    return "\n".join(lines) + "\n"


def build_negotiation_event(quote_request: dict[str, Any], quote_response: dict[str, Any]) -> dict[str, Any]:
    return {
        "negotiation_event_id": f"neg-{quote_response['quote_response_id']}",
        "quote_request_id": quote_request["quote_request_id"],
        "quote_response_id": quote_response["quote_response_id"],
        "event_type": "clarification_requested",
        "actor": "human_operator",
        "timestamp": "2026-05-26T00:00:00Z",
        "change_summary": "Human reviewer requested clarification on drainage assumptions, heater sizing, and substitution boundaries before quote comparison.",
        "before": {
            "comparison_status": "unreviewed",
            "confidence_score": quote_response["confidence_score"],
            "clarification_questions_count": len(quote_response.get("clarification_questions", [])),
        },
        "after": {
            "comparison_status": "clarification_pending",
            "required_follow_up": [
                "Confirm heater circuit sizing assumption.",
                "Confirm drainage scope boundary.",
                "Confirm whether cedar substitutions are allowed.",
            ],
        },
        "human_approval_required": True,
    }


def build_outcome_event(packet: dict[str, Any], quote_response: dict[str, Any]) -> dict[str, Any]:
    midpoint_price = round((quote_response["price_min"] + quote_response["price_max"]) / 2, 2)
    midpoint_lead_time = int(round((quote_response["lead_time_min_days"] + quote_response["lead_time_max_days"]) / 2))
    return {
        "outcome_event_id": f"out-{packet['project_id']}-seed",
        "project_id": packet["project_id"],
        "quote_response_id": quote_response["quote_response_id"],
        "event_type": "seed_example_not_real_world",
        "timestamp": "2026-05-26T00:00:00Z",
        "actor": "human_operator",
        "cost_actual": midpoint_price,
        "timeline_actual_days": midpoint_lead_time,
        "quality_score": 0,
        "inspection_status": "not_performed_seed_only",
        "delivery_status": "not_started_seed_only",
        "dispute_status": "none",
        "lessons_learned": [
            "Seed outcome only. Replace with real-world outcome data when a controlled pilot completes.",
            "Outcome ledger fields remain local and human-entered in v0.2.",
        ],
        "trust_signal": "seed_only_not_for_builder_scoring",
    }


def infer_project_id_from_quote_response(quote_response: dict[str, Any]) -> str:
    quote_request_id = str(quote_response.get("quote_request_id", ""))
    if quote_request_id.startswith("rfq-"):
        return quote_request_id[4:]
    return "unknown-project"


def _word_count(value: str) -> int:
    return len([part for part in str(value).split() if part.strip()])


def _average_word_count(items: list[str]) -> float:
    if not items:
        return 0.0
    return sum(_word_count(item) for item in items) / len(items)


def _fraction_score(numerator: int, denominator: int, weight: int) -> int:
    if denominator <= 0:
        return 0
    return int(round((numerator / denominator) * weight))


def score_quote_response_for_comparison(quote_response: dict[str, Any], schema_errors: list[str]) -> dict[str, Any]:
    required_fields = [
        "quote_response_id",
        "quote_request_id",
        "responder_name",
        "responder_type",
        "quoted_scope",
        "price_min",
        "price_max",
        "currency",
        "lead_time_min_days",
        "lead_time_max_days",
        "assumptions",
        "exclusions",
        "substitutions",
        "confidence_score",
        "risk_notes",
        "clarification_questions",
        "human_review_required",
    ]
    present_fields = []
    missing_fields = []
    for field in required_fields:
        value = quote_response.get(field)
        if value is None:
            missing_fields.append(field)
            continue
        if isinstance(value, str) and not value.strip():
            missing_fields.append(field)
            continue
        present_fields.append(field)

    assumptions = quote_response.get("assumptions", []) or []
    exclusions = quote_response.get("exclusions", []) or []
    risk_notes = quote_response.get("risk_notes", []) or []
    clarification_questions = quote_response.get("clarification_questions", []) or []
    substitutions = quote_response.get("substitutions", []) or []
    quoted_scope = str(quote_response.get("quoted_scope", "")).strip()
    confidence_score = quote_response.get("confidence_score")
    human_review_required = quote_response.get("human_review_required") is True
    price_min = quote_response.get("price_min")
    price_max = quote_response.get("price_max")
    lead_time_min = quote_response.get("lead_time_min_days")
    lead_time_max = quote_response.get("lead_time_max_days")

    category_scores = {
        "response_completeness": _fraction_score(len(present_fields), len(required_fields), 20),
        "scope_clarity": 10 if _word_count(quoted_scope) >= 12 else 5 if _word_count(quoted_scope) >= 6 else 0,
        "assumptions_clarity": 10 if len(assumptions) >= 2 and _average_word_count(assumptions) >= 5 else 5 if assumptions else 0,
        "exclusions_clarity": 10 if len(exclusions) >= 2 and _average_word_count(exclusions) >= 2 else 5 if exclusions else 0,
        "price_range_clarity": 10 if price_min is not None and price_max is not None and price_max >= price_min and quote_response.get("currency") else 0,
        "lead_time_clarity": 10 if lead_time_min is not None and lead_time_max is not None and lead_time_max >= lead_time_min else 0,
        "risk_disclosure": 10 if len(risk_notes) >= 2 else 5 if risk_notes else 0,
        "clarification_quality": 10 if len(clarification_questions) >= 2 else 5 if clarification_questions else 0,
        "human_review_readiness": 10 if human_review_required and confidence_score is not None and confidence_score >= 0.6 else 0,
    }
    completeness_score = sum(category_scores.values())

    strengths = []
    weaknesses = []
    clarification_needed = []
    if category_scores["scope_clarity"] == 10:
        strengths.append("clear quoted scope")
    else:
        weaknesses.append("scope needs more detail")
        clarification_needed.append("Expand quoted scope detail before comparison.")
    if category_scores["assumptions_clarity"] >= 10:
        strengths.append("clear assumptions disclosure")
    else:
        weaknesses.append("assumptions need clarification")
        clarification_needed.append("Clarify assumptions before comparison.")
    if category_scores["exclusions_clarity"] >= 10:
        strengths.append("clear exclusions disclosure")
    else:
        weaknesses.append("exclusions need clarification")
        clarification_needed.append("Clarify exclusions before comparison.")
    if category_scores["lead_time_clarity"] == 10:
        strengths.append("clear lead-time range")
    else:
        weaknesses.append("lead-time range unclear")
        clarification_needed.append("Clarify lead-time range before comparison.")
    if category_scores["risk_disclosure"] >= 10:
        strengths.append("explicit risk disclosure")
    else:
        weaknesses.append("risk disclosure is thin")
        clarification_needed.append("Add more risk disclosure before comparison.")
    if category_scores["clarification_quality"] >= 10:
        strengths.append("useful clarification questions")
    else:
        weaknesses.append("clarification questions are limited")
        clarification_needed.append("Add clarification questions before comparison.")
    if substitutions:
        strengths.append("substitution boundaries stated")
    else:
        weaknesses.append("substitution boundaries missing")
        clarification_needed.append("State substitution boundaries before comparison.")

    if confidence_score is None or confidence_score < 0.6:
        weaknesses.append("confidence score is low")
        clarification_needed.append("Review low confidence score before comparison.")
    if not human_review_required:
        weaknesses.append("human review requirement not preserved")
        clarification_needed.append("Set human review requirement to true before comparison.")
    if schema_errors:
        weaknesses.append("schema validation failed")
        clarification_needed.append("Fix schema validation issues before comparison.")

    if schema_errors or not human_review_required or completeness_score < 60:
        comparison_status = "NOT_COMPARISON_READY"
    elif clarification_needed or completeness_score < 85:
        comparison_status = "NEEDS_CLARIFICATION_BEFORE_COMPARISON"
    else:
        comparison_status = "COMPARISON_READY"

    return {
        "quote_response_id": quote_response.get("quote_response_id", "unknown"),
        "responder_name": quote_response.get("responder_name", "unknown"),
        "responder_type": quote_response.get("responder_type", "unknown"),
        "completeness_score": completeness_score,
        "category_scores": category_scores,
        "missing_fields": sorted(set(missing_fields)),
        "strengths": strengths,
        "weaknesses": sorted(set(weaknesses)),
        "clarification_needed": sorted(set(clarification_needed)),
        "human_review_required": human_review_required,
        "comparison_status": comparison_status,
        "schema_errors": schema_errors,
    }


def build_quote_comparison_summary(quote_responses: list[dict[str, Any]]) -> dict[str, Any]:
    scored_responses = []
    for quote_response in quote_responses:
        schema_errors = validate_payload(quote_response, "quote_response.schema.json")
        scored_responses.append(score_quote_response_for_comparison(quote_response, schema_errors))

    comparison_ready = [item for item in scored_responses if item["comparison_status"] == "COMPARISON_READY"]
    if comparison_ready:
        highest_ready = max(comparison_ready, key=lambda item: item["completeness_score"])
        for item in scored_responses:
            if item["quote_response_id"] == highest_ready["quote_response_id"]:
                item["comparison_status"] = "MOST_COMPLETE_FOR_HUMAN_REVIEW"
                break

    scored_responses.sort(key=lambda item: item["completeness_score"], reverse=True)
    return {
        "report_type": "quote_comparison_summary",
        "comparison_mode": "local_only_information_quality",
        "response_count": len(scored_responses),
        "responses": scored_responses,
        "guardrail_note": "This summary compares information quality only. It does not select contractors, approve hiring, or approve building.",
    }


def render_quote_comparison_summary(summary: dict[str, Any]) -> str:
    lines = [
        "# Quote Comparison Summary",
        "",
        "Local-only comparison of quote response quality and completeness.",
        "",
        "This report does not select vendors, approve hiring, approve building, or route quotes externally.",
        "",
        f"**Responses compared:** {summary['response_count']}  ",
        f"**Mode:** {summary['comparison_mode']}",
        "",
        "## Results",
        "",
    ]

    for item in summary["responses"]:
        lines.extend(
            [
                f"### {item['quote_response_id']}",
                "",
                f"- Responder name: {item['responder_name']}",
                f"- Responder type: {item['responder_type']}",
                f"- Completeness score: {item['completeness_score']} / 100",
                f"- Comparison status: {item['comparison_status']}",
                f"- Human review required: {item['human_review_required']}",
                "",
                "Strengths:",
            ]
        )
        if item["strengths"]:
            lines.extend(f"- {value}" for value in item["strengths"])
        else:
            lines.append("- None recorded")
        lines.extend(["", "Weaknesses:"])
        if item["weaknesses"]:
            lines.extend(f"- {value}" for value in item["weaknesses"])
        else:
            lines.append("- None recorded")
        lines.extend(["", "Missing fields:"])
        if item["missing_fields"]:
            lines.extend(f"- {value}" for value in item["missing_fields"])
        else:
            lines.append("- None")
        lines.extend(["", "Clarification needed:"])
        if item["clarification_needed"]:
            lines.extend(f"- {value}" for value in item["clarification_needed"])
        else:
            lines.append("- None")
        lines.append("")

    lines.extend([
        "## Guardrail",
        "",
        summary["guardrail_note"],
        "",
    ])
    return "\n".join(lines)


def build_example_quote_response(quote_request: dict[str, Any]) -> dict[str, Any]:
    return {
        "quote_response_id": f"resp-{quote_request['project_id']}-001",
        "quote_request_id": quote_request["quote_request_id"],
        "responder_name": "Cascade Sauna Build Co.",
        "responder_type": "regional_builder",
        "quoted_scope": "Sauna shell fabrication, site install coordination, cedar interior package, heater install coordination, waterproofing prep, and commissioning support.",
        "price_min": 42000,
        "price_max": 56000,
        "currency": "USD",
        "lead_time_min_days": 35,
        "lead_time_max_days": 60,
        "assumptions": [
            "Existing electrical service can support selected heater after licensed review.",
            "Site access supports small equipment and crew entry.",
            "Drainage tie-in remains within 20 feet of the sauna pad.",
        ],
        "exclusions": [
            "Stamped engineering",
            "Permit fees",
            "Utility upgrades beyond assumed capacity",
        ],
        "substitutions": [
            "Alternative cedar supplier allowed if lead time extends beyond 6 weeks.",
            "Equivalent waterproofing membrane allowed with approval.",
        ],
        "confidence_score": 0.72,
        "risk_notes": [
            "Final price may move if field drainage work expands.",
            "Heater model change could alter electrical scope.",
            "Stone lead time may vary seasonally.",
        ],
        "clarification_questions": [
            "Has the site slope been field measured?",
            "Is the outdoor shower drain tying into an existing line or new drywell?",
            "Will the owner supply the Harvia heater directly?",
        ],
        "human_review_required": True,
    }


def remove_fields(payload: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    updated = deepcopy(payload)
    for field in fields:
        updated.pop(field, None)
    return updated


def build_agent_manifest(packet: dict[str, Any]) -> dict[str, Any]:
    capability_ids = [item["capability_id"] for item in packet["capability_requirements"]]
    risk_flags = []
    if packet.get("licensed_trade_required"):
        risk_flags.append("licensed_trade_required")
    if packet.get("code_review_required"):
        risk_flags.append("code_review_required")
    if packet.get("permit_review_required"):
        risk_flags.append("permit_review_required")
    if packet.get("safety_notes"):
        risk_flags.append("safety_notes_present")

    review_steps = [
        "Review unknowns before external quoting.",
        "Confirm licensed electrician scope and heater power assumptions.",
        "Confirm permit and code review path with local reviewer.",
        "Approve outbound quote request before supplier routing.",
    ]

    return {
        "project_id": packet["project_id"],
        "project_name": packet["project_name"],
        "protocol_version": packet["protocol_version"],
        "project_summary": packet["project_description"],
        "quote_ready_status": "ready_for_human_quote_review" if not validate_payload(packet, "build_packet.schema.json") else "invalid",
        "required_capabilities": capability_ids,
        "risk_flags": risk_flags,
        "unknowns": packet.get("unknowns", []),
        "human_approval_required": packet.get("human_approval_required", True),
        "next_recommended_human_review_steps": review_steps,
    }
