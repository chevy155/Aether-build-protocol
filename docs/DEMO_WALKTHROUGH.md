# Demo Walkthrough

## Goal

Show a physical project moving through a local protocol, not through an app.

## 3-Minute Script

1. Explain what Aether Build Protocol is: open infrastructure for physical build intent, not a marketplace, not a hosted SaaS product, and not a contractor-selection tool.
2. Open `examples/sauna_node/build_packet.yaml` and point out the project scope, unknowns, safety notes, licensed-trade flags, and permit/code review fields.
3. Run `python scripts/validate_build_packet.py examples/sauna_node/build_packet.yaml` and show the validation report.
4. Run `python scripts/generate_quote_request.py examples/sauna_node/build_packet.yaml` and show the machine-readable quote request.
5. Run `python scripts/generate_rfq_markdown.py examples/sauna_node/quote_request.json` and show the review-only RFQ.
6. Run `python scripts/validate_quote_response.py examples/sauna_node/quote_response_example.json` and show that assumptions, exclusions, price range, lead time, confidence, substitutions, risk notes, and clarification questions are checked.
7. Run `python scripts/score_quote_readiness.py examples/sauna_node/build_packet.yaml` and show that the packet is ready for human quote review, not approved to build.
8. Run `python scripts/generate_negotiation_event.py examples/sauna_node/quote_request.json examples/sauna_node/quote_response_example.json` and `python scripts/generate_outcome_event.py examples/sauna_node/quote_response_example.json` to show the local synthetic ledger path.
9. Run `python scripts/generate_quote_comparison_summary.py examples/sauna_node/quote_response_example.json examples/sauna_node/quote_response_example_2.json examples/sauna_node/quote_response_example_3.json` and show that the system compares quote information quality only.
10. Run `python -m pytest tests/ -v` and show the full local suite passing.
11. Close with guardrails: local-only, no contractor selection, no hiring approval, no build approval, no routing, no supplier contact, no payments.

## Closing Line

This demo shows a physical build moving through a machine-readable protocol. It does not show a marketplace, a hiring decision, or an autonomous build system.
