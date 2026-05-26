# ASI Network Sense Report

**Resource count:** 6  
**Recommended next build phase:** Expand manifest coverage and add provenance verification tests before any external enablement.  
**Boundary:** local manifests only, no real network scanning, no external access, no autonomous control.

## Source-of-Truth Resources

- aether_protocol_core
- docs_and_findings

## Simulation-Only Resources

- sauna_reference_example
- industrial_hook_simulation
- company_integration_sandbox

## High-Trust Artifacts

- protocols/build_intent/schemas/build_packet.schema.json
- protocols/build_intent/schemas/quote_request.schema.json
- README.md
- docs/COMPANY_PILOT_BRIEF.md
- docs/INTEGRATION_FINDINGS_REPORT_TEMPLATE.md

## Low-Trust Artifacts

- examples/sauna_node/quote_response_example.json

## Human Approval Gates

- company_pilot_start
- external_share
- paid_engagement
- production_integration
- publish_release
- real_email_enablement
- real_webhook_enablement
- supplier_contact

## Forbidden Actions Summary

- send_email
- call_webhook
- contact_supplier
- route_quote
- select_contractor
- approve_hiring
- approve_build
- approve_fabrication
- approve_engineering
- approve_payment
- certify_load_rating
- read_outside_repo
- call_external_api
- scan_network

## Safe Next Actions

- generate integration findings report
- collect reviewer feedback
- add bad-input simulation
- add human approval event schema tests
- add provenance verification tests

## Refused Unsafe Actions

- send real email
- call webhook
- contact supplier
- approve fabrication
- approve engineering
- certify load rating
- scan network
- read outside repo

## Guardrails

- no fabrication approval
- no engineering approval
- no payment approval
- no supplier contact
- no quote routing
- no load certification
- no network scanning
- human approval required
