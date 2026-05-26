from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from protocol_utils import build_quote_comparison_summary, load_json  # noqa: E402


FORBIDDEN_TERMS = [
    "winner",
    "best contractor",
    "approved to hire",
    "approved to build",
    "recommended contractor",
]


def test_generate_quote_comparison_summary_accepts_multiple_files() -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_quote_comparison_summary.py"),
            str(ROOT / "examples" / "sauna_node" / "quote_response_example.json"),
            str(ROOT / "examples" / "sauna_node" / "quote_response_example_2.json"),
            str(ROOT / "examples" / "sauna_node" / "quote_response_example_3.json"),
        ],
        check=True,
        cwd=ROOT,
    )
    assert (ROOT / "outputs" / "quote_comparison_summary_latest.json").exists()
    assert (ROOT / "outputs" / "quote_comparison_summary_latest.md").exists()


def test_quote_comparison_summary_scores_responses_and_preserves_human_review() -> None:
    payload = build_quote_comparison_summary(
        [
            load_json(ROOT / "examples" / "sauna_node" / "quote_response_example.json"),
            load_json(ROOT / "examples" / "sauna_node" / "quote_response_example_2.json"),
            load_json(ROOT / "examples" / "sauna_node" / "quote_response_example_3.json"),
        ]
    )
    assert payload["response_count"] == 3
    for response in payload["responses"]:
        assert 0 <= response["completeness_score"] <= 100
        assert isinstance(response["missing_fields"], list)
        assert isinstance(response["clarification_needed"], list)
        assert response["human_review_required"] is True


def test_quote_comparison_summary_avoids_forbidden_language() -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_quote_comparison_summary.py"),
            str(ROOT / "examples" / "sauna_node" / "quote_response_example.json"),
            str(ROOT / "examples" / "sauna_node" / "quote_response_example_2.json"),
            str(ROOT / "examples" / "sauna_node" / "quote_response_example_3.json"),
        ],
        check=True,
        cwd=ROOT,
    )
    markdown_report = (ROOT / "outputs" / "quote_comparison_summary_latest.md").read_text(encoding="utf-8").lower()
    json_report = (ROOT / "outputs" / "quote_comparison_summary_latest.json").read_text(encoding="utf-8").lower()
    for term in FORBIDDEN_TERMS:
        assert term not in markdown_report
        assert term not in json_report


def test_highest_scoring_ready_response_gets_most_complete_label() -> None:
    payload = load_json(ROOT / "outputs" / "quote_comparison_summary_latest.json")
    top = payload["responses"][0]
    assert top["comparison_status"] == "MOST_COMPLETE_FOR_HUMAN_REVIEW"
    assert top["completeness_score"] >= payload["responses"][1]["completeness_score"]
