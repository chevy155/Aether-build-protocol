from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from jsonschema import Draft202012Validator  # noqa: E402
from protocol_utils import build_quote_response_validation_report, compute_quote_readiness_score, load_json, load_schema, remove_fields, validate_payload  # noqa: E402


def test_quote_response_schema_accepts_sauna_example() -> None:
    schema = load_schema("quote_response.schema.json")
    payload = load_json(ROOT / "examples" / "sauna_node" / "quote_response_example.json")
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors == []


def test_quote_response_schema_rejects_missing_required_field() -> None:
    schema = load_schema("quote_response.schema.json")
    payload = load_json(ROOT / "examples" / "sauna_node" / "quote_response_example.json")
    payload.pop("assumptions")
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors


def test_quote_readiness_scoring_detects_missing_comparison_fields() -> None:
    payload = load_json(ROOT / "examples" / "sauna_node" / "quote_response_example.json")
    reduced = remove_fields(payload, ["clarification_questions", "substitutions"])
    result = compute_quote_readiness_score(reduced)
    assert result["is_clean_for_comparison"] is False
    assert "clarification_questions" in result["missing_comparison_fields"]
    assert "substitutions" in result["missing_comparison_fields"]


def test_quote_response_validation_report_includes_pass_fail_and_catches_missing_assumptions() -> None:
    payload = load_json(ROOT / "examples" / "sauna_node" / "quote_response_example.json")
    reduced = remove_fields(payload, ["assumptions"])
    errors = validate_payload(reduced, "quote_response.schema.json")
    report = build_quote_response_validation_report(reduced, errors)
    assert "**Result:** FAIL" in report
    assert "- assumptions" in report


def test_validate_quote_response_script_generates_report() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_quote_response.py"), str(ROOT / "examples" / "sauna_node" / "quote_response_example.json")],
        check=True,
        cwd=ROOT,
    )
    report_path = ROOT / "outputs" / "quote_response_validation_report_latest.md"
    assert report_path.exists()
    report = report_path.read_text(encoding="utf-8")
    assert "**Result:** PASS" in report or "**Result:** FAIL" in report
