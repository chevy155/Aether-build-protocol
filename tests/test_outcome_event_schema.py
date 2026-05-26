from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from jsonschema import Draft202012Validator  # noqa: E402
from protocol_utils import build_outcome_event, load_json, load_schema, load_yaml  # noqa: E402


def test_outcome_event_schema_accepts_generated_seed_event() -> None:
    schema = load_schema("outcome_event.schema.json")
    packet = load_yaml(ROOT / "examples" / "sauna_node" / "build_packet.yaml")
    quote_response = load_json(ROOT / "examples" / "sauna_node" / "quote_response_example.json")
    payload = build_outcome_event(packet, quote_response)
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors == []


def test_outcome_event_schema_accepts_example_file() -> None:
    schema = load_schema("outcome_event.schema.json")
    payload = load_json(ROOT / "examples" / "sauna_node" / "outcome_event_example.json")
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors == []
