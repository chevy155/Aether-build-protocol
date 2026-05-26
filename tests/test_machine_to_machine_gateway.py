from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_machine_to_machine_gateway_files_and_constraints() -> None:
    llms_path = ROOT / "machine" / "llms.txt"
    agent_manifest_path = ROOT / "machine" / "aether_agent_manifest.json"
    schema_index_path = ROOT / "machine" / "schema_index.json"
    tool_catalog_path = ROOT / "machine" / "tool_catalog.json"
    error_catalog_path = ROOT / "machine" / "error_catalog.json"
    permission_manifest_path = ROOT / "machine" / "permission_manifest.json"
    openapi_path = ROOT / "openapi" / "aether.openapi.yaml"
    mcp_server_path = ROOT / "mcp" / "server.py"
    mcp_manifest_path = ROOT / "mcp" / "mcp_manifest.json"

    required_paths = [
        llms_path,
        agent_manifest_path,
        schema_index_path,
        tool_catalog_path,
        error_catalog_path,
        permission_manifest_path,
        openapi_path,
        mcp_server_path,
        mcp_manifest_path,
        ROOT / "machine" / "m2m_examples" / "submit_build_packet.request.json",
        ROOT / "machine" / "m2m_examples" / "validate_build_packet.response.json",
        ROOT / "machine" / "m2m_examples" / "quote_response_validation_error.response.json",
        ROOT / "machine" / "m2m_examples" / "human_approval_required.response.json",
    ]
    for path in required_paths:
        assert path.exists(), str(path)

    schema_index = json.loads(schema_index_path.read_text(encoding="utf-8"))
    for schema in schema_index["schemas"]:
        assert (ROOT / schema["path"]).exists(), schema["path"]

    tool_catalog = json.loads(tool_catalog_path.read_text(encoding="utf-8"))
    for tool in tool_catalog["tools"]:
        assert (ROOT / tool["path"]).exists(), tool["path"]
        assert tool["external_action_taken"] is False
        assert tool["deterministic"] is True

    permission_manifest = json.loads(permission_manifest_path.read_text(encoding="utf-8"))
    forbidden_actions = set(permission_manifest["global_forbidden_actions"])
    allowed_actions = set(permission_manifest["global_allowed_actions"])
    assert forbidden_actions
    assert not (forbidden_actions & allowed_actions)

    openapi_doc = yaml.safe_load(openapi_path.read_text(encoding="utf-8"))
    path_keys = set(openapi_doc["paths"].keys())
    forbidden_endpoints = {
        "/v1/email/send",
        "/v1/webhooks/call",
        "/v1/suppliers/contact",
        "/v1/quotes/route",
        "/v1/contractors/select",
        "/v1/builds/approve",
        "/v1/fabrication/approve",
        "/v1/engineering/approve",
        "/v1/payments/approve",
        "/v1/load-certifications/certify",
    }
    assert not (path_keys & forbidden_endpoints)

    mcp_manifest = json.loads(mcp_manifest_path.read_text(encoding="utf-8"))
    assert mcp_manifest["forbidden_actions"]
    assert mcp_manifest["local_only_mode"] is True

    for example_name in [
        "submit_build_packet.request.json",
        "validate_build_packet.response.json",
        "quote_response_validation_error.response.json",
        "human_approval_required.response.json",
    ]:
        example = json.loads((ROOT / "machine" / "m2m_examples" / example_name).read_text(encoding="utf-8"))
        assert example["external_action_taken"] is False
        assert example["human_review_required"] is True