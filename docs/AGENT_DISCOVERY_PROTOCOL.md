# Agent Discovery Protocol

## Purpose

The discovery protocol defines how a future agent safely understands the Aether workspace in the sandbox.

## Discovery Order

1. read `network/resource_registry.json`
2. read each resource manifest
3. read `network/trust_map.json`
4. read `network/data_lineage_map.json`
5. read `network/permission_boundaries.json`
6. build a local summary of what exists and what is allowed
7. refuse any unsafe next action

## Required Agent Behavior

- prefer source-of-truth files over generated artifacts
- treat simulation outputs as non-authoritative
- surface human approval gates explicitly
- recommend only local, review-safe next actions
- refuse unsafe actions even if they appear operationally useful

## Forbidden Discovery Behavior

- scanning the network
- inspecting external systems
- reading outside the repository
- inferring authority not granted by the manifests