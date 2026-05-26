# Controlled Reviewer Packet

## Reviewer Set

Target five early reviewers:

- contractor or builder
- licensed electrician or trade reviewer
- fabrication or CNC shop reviewer
- architect, designer, or project manager
- technical owner-builder or property owner

## What Aether Is

Aether Build Protocol is open infrastructure for physical build intent. It turns project scope, unknowns, risks, and review requirements into local machine-readable protocol objects for validation and quoting review.

## What Reviewers Should Inspect

- whether project scope is understandable in under five minutes
- whether unknowns and risky assumptions remain visible
- whether licensed trade, code, and permit review needs are explicit
- whether the RFQ is conservative and review-only
- whether quote-response validation and comparison reduce ambiguity

## Files To Review

- `examples/sauna_node/build_packet.yaml`
- `examples/sauna_node/quote_request.json`
- `examples/sauna_node/RFQ.md`
- `examples/sauna_node/quote_response_example.json`
- `examples/sauna_node/quote_comparison_summary.md`
- `outputs/validation_report_latest.md`
- `outputs/quote_response_validation_report_latest.md`

## Commands To Run If Technical

```powershell
python scripts/validate_build_packet.py examples/sauna_node/build_packet.yaml
python scripts/generate_quote_request.py examples/sauna_node/build_packet.yaml
python scripts/generate_rfq_markdown.py examples/sauna_node/quote_request.json
python scripts/validate_quote_response.py examples/sauna_node/quote_response_example.json
python scripts/score_quote_readiness.py examples/sauna_node/build_packet.yaml
python scripts/generate_quote_comparison_summary.py examples/sauna_node/quote_response_example.json examples/sauna_node/quote_response_example_2.json examples/sauna_node/quote_response_example_3.json
```

## Questions To Answer

- Could you understand the project scope in under 5 minutes?
- What information was missing before you would quote this?
- What assumptions were dangerous?
- What fields were confusing?
- What risk did the packet expose well?
- What risk did it hide?
- Would this reduce back-and-forth?
- Would this improve quote quality?
- Would this feel like useful structure or extra admin work?
- What would make this commercially useful?
- Would your company ever want a private version of this?

## What Feedback Matters Most

- missing fields that block real quoting
- hidden or dangerous assumptions
- ambiguous scope boundaries
- unclear exclusions
- whether the comparison summary helps or confuses

## Stop Conditions

- reviewers think the repo implies contractor selection
- reviewers think the repo implies build or hiring approval
- reviewers think the repo implies supplier outreach or routing
- safety, code, permit, or licensed-trade fields appear weak or missing

## Guardrails

- local-only
- informational only
- no marketplace behavior
- no contractor selection
- no hiring approval
- no build approval
- no supplier contact
- human review required
