# Agent Discovery Guide

## Discovery Sequence

An agent should begin with the machine-readable beacon files in this order:

1. `machine/llms.txt`
2. `machine/aether_agent_manifest.json`
3. `machine/permission_manifest.json`
4. `machine/schema_index.json`
5. `machine/tool_catalog.json`
6. `machine/error_catalog.json`

## What An Agent Can Learn

- what Aether is
- where schemas live
- which scripts are safe
- which actions are forbidden
- which actions require human approval
- how to interpret deterministic errors

## What An Agent Must Not Assume

- that a hosted API exists
- that MCP is deployed as a live server
- that any external action is permitted
- that simulation outputs are production authority

## Start Rule

Read manifests first. Validate locally. Refuse unsafe actions. Preserve human approval boundaries.