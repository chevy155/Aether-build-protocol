# Machine-to-Machine Gateway

This directory provides the machine-readable beacon layer for Aether Build Protocol.

It is designed for local-only agent discovery, safe tool interpretation, and deterministic error handling.

## Contents

- `llms.txt`
- `aether_agent_manifest.json`
- `schema_index.json`
- `tool_catalog.json`
- `error_catalog.json`
- `permission_manifest.json`
- `m2m_examples/`

## Boundary

- local-only
- no hosted API
- no external API calls
- no email sending
- no webhook delivery
- no supplier contact
- no quote routing
- human approval required for external actions

## Purpose

These files let agents and developers inspect Aether without guessing what exists, what is safe, what is forbidden, and what still requires human approval.