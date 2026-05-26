from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from jsonschema import Draft202012Validator  # noqa: E402
from protocol_utils import build_negotiation_event, load_json, load_schema  # noqa: E402


def test_negotiation_event_schema_accepts_generated_event() -> None:
    schema = load_schema("negotiation_event.schema.json")
    quote_request = load_json(ROOT / "examples" / "sauna_node" / "quote_request.json")
    quote_response = load_json(ROOT / "examples" / "sauna_node" / "quote_response_example.json")
    payload = build_negotiation_event(quote_request, quote_response)
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors == []


def test_negotiation_event_schema_accepts_example_file() -> None:
    schema = load_schema("negotiation_event.schema.json")
    payload = load_json(ROOT / "examples" / "sauna_node" / "negotiation_event_example.json")
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors == []
