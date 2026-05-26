from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_rfq_markdown import render_rfq  # noqa: E402
from protocol_utils import build_quote_request, load_yaml  # noqa: E402


def test_quote_request_generation_creates_required_fields() -> None:
    packet = load_yaml(ROOT / "examples" / "sauna_node" / "build_packet.yaml")
    quote_request = build_quote_request(packet)
    assert quote_request["project_id"] == "sauna-node-001"
    assert quote_request["human_approval_required"] is True
    assert "requested_quote_categories" in quote_request
    assert "required_capabilities" in quote_request
    assert "risk_questions" in quote_request


def test_rfq_generation_includes_human_approval_warning() -> None:
    packet = load_yaml(ROOT / "examples" / "sauna_node" / "build_packet.yaml")
    quote_request = build_quote_request(packet)
    rfq = render_rfq(quote_request)
    assert "for review and quoting only" in rfq
    assert "Human approval required: True" in rfq
