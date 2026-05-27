# MCP Drive Agent Proof Report

## Executive Summary

- Proof status: PASS
- Branch: test/v0.2.8-mcp-drive-proof
- Simulated local agent workflow: True
- Regression safety verified inside harness: True

## Discovery Evidence

- README.md
- machine/llms.txt
- machine/aether_agent_manifest.json
- machine/schema_index.json
- machine/tool_catalog.json
- machine/permission_manifest.json
- machine/error_catalog.json
- machine/response_envelope.schema.json
- mcp/mcp_manifest.json
- openapi/aether.openapi.yaml
- mcp/server.py

## Schema and Contract Surfaces

- protocols/build_intent/schemas/build_packet.schema.json
- machine/response_envelope.schema.json
- mcp/mcp_manifest.json
- openapi/aether.openapi.yaml

## Payload Validation

- Raw fixture: tests/fixtures/mcp_drive/raw_cad_job_request.json
- Generated payload: outputs/mcp_drive/generated_build_packet.json
- Invalid case detected: True
- Repair successful: True

## Forbidden Action Discipline

- Forbidden action attempted: send_email
- Action blocked locally: True
- External action taken: False

## Human Approval Preservation

- human_approval_required on payload: True
- Human approval response status: BLOCKED
- Automatic execution prevented: True

## Commands Run

- local_schema_validation generated_build_packet: PASS (success)
- local_schema_validation invalid_build_packet: PASS (expected_guardrail_block)
- mcp.refuse_forbidden_action send_email: PASS (expected_guardrail_block)
- C:\Program Files\Python312\python.exe -m pytest -q: PASS (success)

## Artifacts Generated

- outputs/mcp_drive/generated_build_packet.json
- outputs/mcp_drive/generated_build_packet.yaml
- outputs/mcp_drive/invalid_build_packet.json
- outputs/mcp_drive/invalid_build_packet.yaml
- outputs/mcp_drive/forbidden_action_response.json
- outputs/mcp_drive/human_approval_response.json
- outputs/mcp_drive/latest_agent_run_report.json
- outputs/mcp_drive/latest_agent_run_report.md

## Guardrail Boundaries

- send_email remained blocked locally with no external action.
- human_approval_required remained true on the generated payload.
- external_release remained blocked pending human approval.

## What This Proves

- Discovery surfaces were found locally through repo files.
- A synthetic CAD/job-style request was mapped into a machine-readable Build Packet.
- Local schema validation caught an invalid case and the harness repaired it without hiding the failure.
- Forbidden external actions were blocked and human approval gates remained preserved.

## What This Does Not Prove

- This is a bounded local proof loop only.
- This does not prove a live external LLM or real MCP service integration.
- This does not deploy a gateway, send email, call webhooks, or contact suppliers.
