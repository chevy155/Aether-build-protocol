from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from protocol_utils import load_schema, load_yaml  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402


def test_build_packet_schema_accepts_sauna_packet() -> None:
    schema = load_schema("build_packet.schema.json")
    packet = load_yaml(ROOT / "examples" / "sauna_node" / "build_packet.yaml")
    errors = list(Draft202012Validator(schema).iter_errors(packet))
    assert errors == []


def test_build_packet_schema_rejects_missing_required_field() -> None:
    schema = load_schema("build_packet.schema.json")
    packet = load_yaml(ROOT / "examples" / "sauna_node" / "build_packet.yaml")
    packet.pop("project_name")
    errors = list(Draft202012Validator(schema).iter_errors(packet))
    assert errors
