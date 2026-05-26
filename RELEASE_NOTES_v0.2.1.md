# Aether Build Protocol v0.2.1 — Local Quote Comparison Summary

## Purpose

Aether Build Protocol is the foundational digital coordination layer for machine-readable hardware execution.

It establishes the standardized data highway between upstream design environments such as CAD metadata, structured BOMs, and drawing packages, and downstream fabrication-review systems that need explicit scope, risk, traceable constraints, and deterministic handoff artifacts.

This v0.2.1 milestone proves the local cognitive layer of that network. By ingesting, validating, and deterministically scoring multiple inbound quote responses, the protocol creates a local verification interface for data completeness, structural risk disclosure, lead-time alignment, and human-review readiness.

It remains intentionally narrow. This release does not select contractors, approve hiring, approve fabrication, approve engineering, route suppliers, or trigger autonomous external action.

## What Changed Since v0.1

- the repository became public-ready as an open-core protocol seed
- the sauna reference packet established the local build-intent workflow
- validation, quote request generation, RFQ generation, and agent manifest outputs became reproducible from the repo root

## What Changed In v0.2

- added quote response ingestion and validation
- added build-packet quote-readiness scoring
- added local synthetic negotiation and outcome event generation
- extended the local closed loop from Build Packet to Outcome Event seed

## What Changed In v0.2.1

- added deterministic local quote comparison summary generation
- added two additional sauna quote response examples for comparison scenarios
- added comparison-safe labels such as `MOST_COMPLETE_FOR_HUMAN_REVIEW`, `COMPARISON_READY`, `NEEDS_CLARIFICATION_BEFORE_COMPARISON`, and `NOT_COMPARISON_READY`
- preserved guardrails against contractor selection, hiring approval, build approval, routing, and external communication

## How To Run The Proof Loop

```powershell
python scripts/validate_build_packet.py examples/sauna_node/build_packet.yaml
python scripts/generate_quote_request.py examples/sauna_node/build_packet.yaml
python scripts/generate_rfq_markdown.py examples/sauna_node/quote_request.json
python scripts/generate_agent_manifest.py examples/sauna_node/build_packet.yaml
python scripts/validate_quote_response.py examples/sauna_node/quote_response_example.json
python scripts/score_quote_readiness.py examples/sauna_node/build_packet.yaml
python scripts/generate_negotiation_event.py examples/sauna_node/quote_request.json examples/sauna_node/quote_response_example.json
python scripts/generate_outcome_event.py examples/sauna_node/quote_response_example.json
python scripts/generate_quote_comparison_summary.py examples/sauna_node/quote_response_example.json examples/sauna_node/quote_response_example_2.json examples/sauna_node/quote_response_example_3.json
python -m pytest tests/ -v
```

## Test Status

Placeholder for release cut: replace with the latest passing test count at tag time.

## Guardrails

- no marketplace
- no contractor selection
- no hiring approval
- no build approval
- no supplier routing
- no payments
- no hosted API
- no autonomous external action
- human review required throughout

## Known Limitations

- quote comparison is informational only
- no real quote negotiation transport
- no supplier outreach
- no CAD plugin
- no hosted API
- no private deployment layer yet
- outcome events remain synthetic examples

## Recommended Next Action

Package the repository for controlled public review with a clean tag, short demo walkthrough, and structured reviewer packet before adding new protocol capability.
