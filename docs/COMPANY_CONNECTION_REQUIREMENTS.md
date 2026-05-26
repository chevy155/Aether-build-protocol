# Company Connection Requirements

## What This Sandbox Demonstrates

The sandbox demonstrates the minimum local artifacts a fabrication company would need in order to connect a project intake flow to Aether Build Protocol:

- a company profile
- a project payload
- a BOM export
- a drawing manifest reference
- a deterministic mapping into `build_packet` and `quote_request`
- a human approval event before any next-stage action
- preview-only outbound notification artifacts
- provenance hashes across the generated artifact chain
- an event log proving that no external action was taken

## Required Behaviors

- Preserve the company project ID through the mapped artifacts.
- Preserve the required capabilities from the company payload.
- Preserve the BOM and drawing-manifest references.
- Record unknowns and assumptions explicitly.
- Require human approval for the next stage.
- Mark the flow as sandbox-only and local-only.
- Mark the flow as not production integration.
- Confirm that no supplier contact, quote routing, fabrication approval, engineering approval, payment approval, or load certification occurred.

## Out of Scope

This sandbox does not provide:

- a real company connection
- a hosted integration service
- a real API server
- a real webhook endpoint
- a real email provider
- real quote distribution
- real fabrication authorization
- real engineering approval
- real load certification

## Success Condition

The sandbox passes when the repository can regenerate the full artifact tree deterministically and the ledger confirms `external_action_taken: false` throughout the event log.
