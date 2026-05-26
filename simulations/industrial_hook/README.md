# Industrial Hook End-to-End Simulation

This simulation demonstrates a local-only builder-to-fabricator handoff using an industrial-style steel utility hook as the mock physical artifact.

## Purpose

The goal is to show how raw builder intent can move through Aether Build Protocol without contacting suppliers, routing quotes externally, approving fabrication, or implying engineering or lifting approval.

## Run

```powershell
python scripts/simulate_industrial_hook_pipeline.py
```

## Guardrails

- simulated only
- not certified
- not approved for lifting
- engineering review required
- human approval required before real fabrication
- no supplier contact
- no external action authorized

## Workspaces

- `builder_workspace/` contains mock CAD metadata, drawing metadata, raw BOM rows, and intake data.
- `aether_workspace/` contains the derived Build Packet and protocol artifacts.
- `fabricator_workspace/` contains the deterministic fabricator profile, feasibility review, and quote response.
- `monitor_workspace/` contains telemetry, guardrail audit results, lineage trace, and outcome summary.
- `outputs/` contains the final simulation report.
