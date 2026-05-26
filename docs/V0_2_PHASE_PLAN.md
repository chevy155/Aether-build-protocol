# v0.2 Phase Plan

## Purpose

Prepare the protocol for a disciplined local closed loop from build intent through synthetic outcome recording while staying public-ready and infrastructure-first.

## Scope

- quote response ingestion
- quote response validation
- negotiation event generation
- outcome event seed generation
- quote-readiness scoring
- second small reference project

## Non-Goals

- marketplace features
- frontend or UI
- accounts
- payments
- supplier routing
- external communication
- hosted services
- CAD plugins
- autonomous actions

## Files Added

- `docs/V0_2_PHASE_PLAN.md`
- `docs/QUOTE_RESPONSE_INGESTION_SPEC.md`
- `docs/QUOTE_READINESS_SCORE_SPEC.md`
- `docs/NEGOTIATION_EVENT_SPEC.md`
- `examples/sauna_node/quote_response_example.json`
- `examples/sauna_node/negotiation_event_example.json`
- `examples/sauna_node/outcome_event_example.json`
- `examples/sauna_node/quote_response_validation_report.md`
- `scripts/validate_quote_response.py`
- `scripts/score_quote_readiness.py`
- `scripts/generate_negotiation_event.py`
- `scripts/generate_outcome_event.py`
- `tests/test_quote_response_schema.py`
- `tests/test_quote_readiness_score.py`
- `tests/test_negotiation_event_schema.py`
- `tests/test_outcome_event_schema.py`

## Run Commands

```powershell
python scripts/validate_build_packet.py examples/sauna_node/build_packet.yaml
python scripts/generate_quote_request.py examples/sauna_node/build_packet.yaml
python scripts/generate_rfq_markdown.py examples/sauna_node/quote_request.json
python scripts/generate_agent_manifest.py examples/sauna_node/build_packet.yaml
python scripts/validate_quote_response.py examples/sauna_node/quote_response_example.json
python scripts/score_quote_readiness.py examples/sauna_node/build_packet.yaml
python scripts/generate_negotiation_event.py examples/sauna_node/quote_request.json examples/sauna_node/quote_response_example.json
python scripts/generate_outcome_event.py examples/sauna_node/quote_response_example.json
python -m pytest tests/ -v
```

## Success Condition

The protocol demonstrates a local closed loop:

Build Packet -> Quote Request -> RFQ -> Quote Response -> Negotiation Event -> Outcome Event seed.

## Most Important Artifact

The quote-response validation report.

It must answer whether the responder clearly stated:

- assumptions
- exclusions
- price range
- lead time
- confidence
- substitutions
- risk notes
- clarification questions

If those fields are not present, the response is not clean enough to compare.

## Acceptance Criteria

- local quote-response validation report generated
- quote-readiness score generated as JSON and markdown
- negotiation event example generated locally
- outcome event example generated locally
- all prior tests still pass
- no non-protocol product surface added

## Known Limitations

- synthetic only for negotiation and outcome examples
- no supplier communication
- no real negotiation transport
- no hosted API
- no private deployment layer yet
