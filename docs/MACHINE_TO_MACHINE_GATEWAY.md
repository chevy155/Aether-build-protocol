# Machine-to-Machine Gateway

## Purpose

The machine-to-machine gateway makes Aether Build Protocol discoverable and interpretable by agents, orchestration systems, and developer tooling without granting unsafe authority.

## What It Adds

- `machine/llms.txt` for discovery
- `machine/aether_agent_manifest.json` for repo-level agent interpretation
- `machine/schema_index.json` for schema lookup
- `machine/tool_catalog.json` for safe local tools
- `machine/permission_manifest.json` for explicit boundaries
- `machine/error_catalog.json` for deterministic failures
- `openapi/aether.openapi.yaml` as a contract-only local API description
- `mcp/` as a local-only MCP skeleton

## Why It Matters

This is the point where Aether becomes more than human-readable documentation. It becomes structured, discoverable, and safer for machine-to-machine interpretation.

## Boundary

- local-only
- no hosted API
- no external calls
- no supplier contact
- no quote routing
- no fabrication approval
- no engineering approval
- human approval required for external actions