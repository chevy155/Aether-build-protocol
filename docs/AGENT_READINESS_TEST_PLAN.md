# Agent Readiness Test Plan

## Test Objective

Prove that a fresh-clone local agent can discover Aether Build Protocol through repository files, run only safe local workflows, preserve human approval gates, and generate a deterministic readiness report.

## Assumed Fresh Clone State

- repository cloned locally
- Python environment available
- no internet required
- no real external agent connected
- no external services configured
- no hosted API running
- no real MCP deployment running

## Files The Agent Must Inspect

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

## Commands The Agent Must Run

```powershell
python scripts/run_agent_readiness_check.py
python scripts/generate_machine_response.py --code VALIDATION_PASSED --operation validate_build_packet --artifact-id build_packet_001
python scripts/generate_machine_response.py --code HUMAN_APPROVAL_REQUIRED --operation external_release --artifact-id quote_request_001
python scripts/generate_machine_response.py --code EXTERNAL_ACTION_FORBIDDEN --operation send_email --artifact-id notification_event_001
python scripts/simulate_company_integration.py
python scripts/simulate_industrial_hook_pipeline.py
```

## Artifacts The Agent Must Produce

- outputs/agent_readiness_report.json
- outputs/agent_readiness_report.md
- outputs/machine_response_latest.json
- integrations/company_sandbox/ledger/company_integration_summary.json
- simulations/industrial_hook/outputs/simulation_report.json

## Guardrails The Agent Must Preserve

- local-only behavior
- no hosted API
- no real MCP deployment
- no external API calls
- no email sent
- no webhook called
- no supplier contacted
- no quote routed
- no contractor selected
- no fabrication approval
- no engineering approval
- no payment approval
- no load certification
- human approval required when applicable

## Failure Conditions

- required entrypoints missing
- required manifests or schemas missing
- required scripts missing
- forbidden actions absent from permission manifest
- forbidden actions present in tool allowed_actions
- required safe commands fail
- required outputs missing
- machine responses lose external_action_taken false
- human approval gates are absent where expected
- readiness reports are not generated

## Final Readiness Scoring

- AGENT_READY
- AGENT_PARTIALLY_READY
- AGENT_NOT_READY

AGENT_READY does not mean production-ready.

AGENT_READY means a local agent can discover and run the sandbox safely.