# Fresh Clone Agent Readiness Spec

## Purpose

This specification defines how a new local agent, new developer, or future machine-readable client should discover and operate Aether Build Protocol from a fresh clone without requiring human explanation.

## What Fresh Clone Readiness Means

Fresh clone readiness means a local agent can enter the repository, discover the machine-readable entrypoints, identify safe tools, preserve forbidden-action boundaries, run the sanctioned local proof workflows, and generate a deterministic readiness report.

Fresh clone readiness does not mean production readiness.

## What An Agent Should Read First

An agent should read the top-level repository overview before moving into the machine-readable discovery surfaces.

## Expected Discovery Path

README.md
-> machine/llms.txt
-> machine/aether_agent_manifest.json
-> machine/schema_index.json
-> machine/tool_catalog.json
-> machine/permission_manifest.json
-> machine/error_catalog.json
-> machine/response_envelope.schema.json
-> mcp/mcp_manifest.json
-> openapi/aether.openapi.yaml

## Allowed Local Actions

- read repository documentation and manifests
- read schema and contract files
- run local validation scripts
- run local deterministic simulations
- generate local reports and local artifacts
- propose next safe local actions

## Forbidden Actions

- send email
- call webhook
- contact supplier
- route quote
- select contractor
- approve build
- approve fabrication
- approve engineering
- approve payment
- certify load rating
- scan network
- read outside the repo

## Human Approval Boundaries

Human approval remains required whenever a workflow attempts to cross the sandbox boundary, describe external release, imply supplier contact, or suggest production enablement.

Fresh clone readiness must preserve those gates instead of bypassing them.

## Required Proof Commands

```powershell
python scripts/run_agent_readiness_check.py
python scripts/generate_machine_response.py --code VALIDATION_PASSED --operation validate_build_packet --artifact-id build_packet_001
python scripts/generate_machine_response.py --code HUMAN_APPROVAL_REQUIRED --operation external_release --artifact-id quote_request_001
python scripts/generate_machine_response.py --code EXTERNAL_ACTION_FORBIDDEN --operation send_email --artifact-id notification_event_001
python scripts/simulate_company_integration.py
python scripts/simulate_industrial_hook_pipeline.py
```

## Expected Outputs

- outputs/agent_readiness_report.json
- outputs/agent_readiness_report.md
- outputs/machine_response_latest.json
- integrations/company_sandbox/ledger/company_integration_summary.json
- simulations/industrial_hook/outputs/simulation_report.json

## Pass/Fail Criteria

Pass requires the agent-readiness check to:

- find the documented entrypoints
- discover the required manifests and schemas
- identify safe local tools
- confirm forbidden actions remain forbidden
- run the sanctioned local commands successfully
- verify key output artifacts exist
- preserve human approval gates
- keep external_action_taken false in deterministic machine responses
- generate both readiness reports

## Known Limitations

- local repository readiness only
- no real external agent connected
- no hosted API
- no real MCP deployment
- no external discovery
- no production permission engine
- no real company system integration
- no proof of production runtime safety