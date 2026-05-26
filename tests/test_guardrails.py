from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from protocol_utils import load_schema  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402


def test_guardrails_appear_in_readme_and_docs() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    guardrails = (ROOT / "docs" / "GUARDRAILS.md").read_text(encoding="utf-8")
    assert "Human approval is required" in readme
    assert "No autonomous action." in guardrails
    assert "Licensed trade flags" in guardrails


def test_outcome_event_schema_requires_trust_and_outcome_fields() -> None:
    schema = load_schema("outcome_event.schema.json")
    payload = {
        "outcome_event_id": "out-1",
        "project_id": "sauna-node-001",
        "quote_response_id": "resp-1",
        "event_type": "completed",
        "timestamp": "2026-05-26T00:00:00Z",
        "actor": "human_operator"
    }
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    messages = json.dumps([error.message for error in errors])
    assert "cost_actual" in messages
    assert "trust_signal" in messages
