# Machine-to-Machine Print Transaction Sandbox Spec

## Purpose

This specification defines the bounded local-only print transaction sandbox added in v0.2.8.

The sandbox proves that Aether can simulate a designer-to-shop machine transaction without contacting a real shop, authorizing fabrication, or crossing the human-approval boundary.

## Scenario

The reference scenario is a wall-mounted 3D printed cable hook.

- designer request captured in machine-readable form
- Build Packet mapped locally
- Quote Request derived locally
- fake shop profiles matched locally
- quote responses simulated locally
- negotiation simulated locally
- fulfillment and delivery simulated locally
- outcome recorded locally
- provenance and guardrail evidence written locally

## Primary Run Command

```powershell
python scripts/simulate_print_transaction.py
```

## Artifact Root

`transactions/print_job_sandbox/`

## Core Guarantees

- local-only
- fake shops only
- no external action
- no shop contacted
- no payment authorized
- no print approved
- no fabrication approved
- no delivery approved
- no engineering approval
- no load certification
- human approval required

## Transaction Outputs

The sandbox writes a deterministic artifact chain covering:

- designer request inputs
- mapped Build Packet and Quote Request
- required capabilities and human approval event
- fake shop profiles and match results
- simulated quote responses and comparison summary
- simulated negotiation events
- simulated work order, print status, delivery event, and outcome event
- provenance manifest, guardrail audit, machine responses, and closeout reports

## Machine Response Integration

The sandbox records deterministic machine response envelopes for:

- `VALIDATION_PASSED`
- `HUMAN_APPROVAL_REQUIRED`
- `EXTERNAL_ACTION_FORBIDDEN`
- `ENGINEERING_REVIEW_REQUIRED`
- `LOAD_CERTIFICATION_NOT_PROVIDED`

These responses remain local artifacts only and do not authorize external execution.

## Non-Goals

- no real print quote
- no real shop integration
- no supplier routing
- no hosted marketplace
- no production transaction processing
- no external MCP connection
- no automated publishing