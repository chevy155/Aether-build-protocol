from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from protocol_utils import load_json, load_yaml, score_build_packet_quote_readiness, validate_payload  # noqa: E402


def test_quote_readiness_score_between_zero_and_hundred() -> None:
    packet = load_yaml(ROOT / "examples" / "sauna_node" / "build_packet.yaml")
    result = score_build_packet_quote_readiness(packet, validate_payload(packet, "build_packet.schema.json"))
    assert 0 <= result["score"] <= 100


def test_quote_readiness_status_does_not_approve_to_build() -> None:
    packet = load_yaml(ROOT / "examples" / "sauna_node" / "build_packet.yaml")
    result = score_build_packet_quote_readiness(packet, validate_payload(packet, "build_packet.schema.json"))
    assert "approved to build" not in result["status"].lower()
    assert result["approved_to_build"] is False


def test_score_quote_readiness_generates_outputs() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "score_quote_readiness.py"), str(ROOT / "examples" / "sauna_node" / "build_packet.yaml")],
        check=True,
        cwd=ROOT,
    )
    json_output = ROOT / "outputs" / "quote_readiness_score_latest.json"
    md_output = ROOT / "outputs" / "quote_readiness_score_latest.md"
    assert json_output.exists()
    assert md_output.exists()
    payload = load_json(json_output)
    assert 0 <= payload["score"] <= 100
