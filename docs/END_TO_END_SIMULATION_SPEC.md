# End-to-End Simulation Spec

## Purpose

This document defines the local-only end-to-end simulation harness introduced in v0.2.3.

The harness exists to prove that Aether Build Protocol can take builder-side design intent, convert it into machine-readable protocol artifacts, hand those artifacts to a deterministic fabricator simulator, and log the full flow with explicit guardrails.

## Simulation Actors

- Builder Simulator: creates mock CAD metadata, mock drawing metadata, a raw BOM, and project intake fields.
- Aether Protocol Engine: transforms builder inputs into a Build Packet, validation report, quote request, RFQ, agent manifest, quote-readiness score, comparison summary, negotiation event, and outcome event.
- Fabricator Simulator: ingests the Aether artifact set and produces a deterministic feasibility review and informational quote response.
- Monitoring Agent Stack: records telemetry, audits guardrails, tracks lineage, and writes the final ledger summary.

## Artifact Lifecycle

Builder package -> Build Packet -> Validation Report -> Quote Request -> RFQ -> Agent Manifest -> Fabricator Review -> Quote Response -> Quote Response Validation -> Quote Comparison Summary -> Negotiation Event -> Outcome Event -> Ledger Summary -> Final Simulation Report.

## Builder Simulator

The builder simulator writes a local mock package for an industrial-style steel utility hook.

Artifacts include:

- mock CAD metadata
- mock drawing metadata
- raw BOM rows
- builder intake YAML

The builder package preserves unknowns, assumptions, engineering review requirements, and the human approval gate.

## Aether Protocol Engine

The protocol engine reuses the deterministic local Python logic already present in the repository.

It generates:

- `simulations/industrial_hook/aether_workspace/build_packet.yaml`
- `simulations/industrial_hook/aether_workspace/validation_report.md`
- `simulations/industrial_hook/aether_workspace/quote_request.json`
- `simulations/industrial_hook/aether_workspace/RFQ.md`
- `simulations/industrial_hook/aether_workspace/agent_manifest.json`
- `simulations/industrial_hook/aether_workspace/quote_readiness_score.json`
- `simulations/industrial_hook/aether_workspace/quote_readiness_score.md`
- `simulations/industrial_hook/aether_workspace/quote_comparison_summary.json`
- `simulations/industrial_hook/aether_workspace/quote_comparison_summary.md`
- `simulations/industrial_hook/aether_workspace/negotiation_event.json`

The generated RFQ remains local-only and states that no fabrication, lifting approval, engineering approval, or external action is authorized.

## Fabricator Simulator

The deterministic fabricator profile models a small-batch metal fabrication shop with bounded capabilities and constraints.

Capabilities:

- CNC laser cutting
- CNC plasma cutting
- deburring
- press brake forming
- powder coating
- small-batch fabrication

Constraints:

- bounded thickness capability
- bounded tolerance capability
- bounded part size
- declared coating options
- engineering review required for load-bearing parts
- no certification without engineer stamp

Outputs:

- `simulations/industrial_hook/fabricator_workspace/fabricator_profile.json`
- `simulations/industrial_hook/fabricator_workspace/received_packet_manifest.json`
- `simulations/industrial_hook/fabricator_workspace/feasibility_review.json`
- `simulations/industrial_hook/fabricator_workspace/quote_response.json`
- `simulations/industrial_hook/fabricator_workspace/quote_response_validation_report.md`

## Monitoring Agents

### Telemetry Agent

Logs every major stage transition to `simulations/industrial_hook/monitor_workspace/telemetry_log.jsonl`.

### Guardrail Auditor

Audits the simulation for forbidden approval, routing, supplier-contact, payment, and certification language and writes `simulations/industrial_hook/monitor_workspace/guardrail_audit.json`.

### Protocol Observer

Tracks lineage across the builder package, Build Packet, quote request, RFQ, fabricator response, validation report, and outcome event in `simulations/industrial_hook/monitor_workspace/simulation_trace.json`.

### Ledger Clerk

Writes `simulations/industrial_hook/monitor_workspace/ledger_summary.json` and `simulations/industrial_hook/monitor_workspace/outcome_event.json`.

## Guardrails

The simulation is local-only and deterministic.

It does not:

- contact suppliers
- route quotes externally
- select contractors
- approve hiring
- approve building
- approve engineering
- certify load use
- process payments
- place autonomous orders

The industrial-style hook artifact is a simulation only. It is not certified, not approved for lifting, and not approved for real fabrication without qualified human review.

## Run Command

```powershell
python scripts/simulate_industrial_hook_pipeline.py
```

## Expected Outputs

The simulation should populate the full `simulations/industrial_hook/` tree, including builder, Aether, fabricator, monitor, and report artifacts.

## Pass/Fail Criteria

PASS requires all of the following:

- all required artifacts are generated
- the Build Packet validates
- the fabricator simulator can ingest the packet
- the quote response validates
- the guardrail audit passes
- human review and engineering review warnings are preserved
- no forbidden approval, routing, payment, or certification language appears

## Known Limitations

- simulated CAD metadata only
- no real SolidWorks parser
- no real fabricator quote
- no supplier communication
- no engineering certification
- no load-rating validation

## Why This Helps Reviewers

Reviewers can see a concrete builder-to-fabricator handoff rather than only reading about schemas. The harness makes the protocol legible by showing what a fabricator receives, what remains unknown, what is blocked by guardrails, and what gets logged across the full local workflow.
