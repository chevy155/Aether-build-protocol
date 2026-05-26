from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from protocol_utils import build_agent_manifest, load_yaml  # noqa: E402


def test_agent_manifest_includes_required_capabilities_and_unknowns() -> None:
    packet = load_yaml(ROOT / "examples" / "sauna_node" / "build_packet.yaml")
    manifest = build_agent_manifest(packet)
    assert "electrician" in manifest["required_capabilities"]
    assert manifest["unknowns"]
    assert manifest["human_approval_required"] is True
