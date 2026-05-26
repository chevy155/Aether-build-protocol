# Aether Build Protocol v0.2.1 — Local Quote Comparison Summary

## Purpose

This release proves that Aether Build Protocol can compare multiple local quote responses for information quality without becoming a marketplace, vendor-selection engine, or hiring workflow.

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
