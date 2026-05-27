# Changelog

## v0.2.8 - MCP Drive Agent Proof

- added a bounded local MCP Drive Agent Proof harness for deterministic repo discovery, machine/MCP surface discovery, synthetic CAD/job request mapping, Build Packet validation, invalid-case repair, forbidden-action blocking, and proof artifact generation
- added focused regression coverage for the MCP-drive proof flow and verified the generated JSON and Markdown proof reports under `outputs/mcp_drive/`
- preserved local-only boundaries with no hosted API, no live external MCP integration, no real webhooks or email delivery, no external actions, and no production gateway claim

## v0.2.7 - Fresh Clone Agent Readiness Test

- added a fresh-clone agent readiness spec, test plan, optional checklist, and deterministic local readiness check script
- added human-readable and machine-readable readiness reports proving repo discovery, safe-tool discovery, forbidden-action discovery, and local workflow execution
- preserved local-only boundaries with no hosted API, no real MCP deployment, no real external agent connection, no external actions, and no production readiness claim

## v0.2.6 - Deterministic Machine Response Envelopes

- added a deterministic machine response envelope schema, response templates, response examples, and a local response generator
- aligned the machine gateway, OpenAPI contract, and MCP skeleton around the standard response envelope shape
- preserved local-only execution with explicit forbidden actions, human approval gates, and `external_action_taken: false` in every machine response

## v0.2.5 - Machine-to-Machine Agent Gateway

- added machine-readable discovery files including `llms.txt`, agent manifest, schema index, tool catalog, permission manifest, deterministic error catalog, and machine-readable examples
- added a contract-only OpenAPI description and a local-only MCP skeleton for safe agent discovery and tool interpretation
- preserved local-only boundaries with no hosted API, no external calls, and no unsafe approval or routing actions

## v0.2.5 - ASI Network Sense Sandbox

- added a local-only manifest-based ASI network sense sandbox for safe future-agent workspace understanding
- added resource registry, capability manifests, trust map, data lineage map, and permission boundary files under `network/`
- added ASI network sense simulation outputs and regression coverage while preserving the existing company sandbox, industrial hook, and sauna proof loops

## Unreleased

- added Integration Findings Report template for company sandbox pilots

## v0.2.4 - Fake Company Integration Sandbox

- added a deterministic fake company integration sandbox for Northstar Fabrication Systems under `integrations/company_sandbox/`
- added a local company payload to Aether mapping flow that generates `build_packet`, `quote_request`, and a required human approval event
- added preview-only email and webhook artifacts plus an integration event log with `external_action_taken: false`
- added artifact provenance hashing, sandbox architecture/spec docs, and regression coverage while preserving the existing industrial-hook and sauna proof loops

## v0.2.3 - End-to-End Fabrication Simulation Harness

- added a deterministic local-only builder-to-fabricator simulation harness for an industrial-style steel utility hook
- added builder, Aether, fabricator, monitor, and report artifact generation under `simulations/industrial_hook/`
- added monitoring telemetry, guardrail audit, protocol trace, ledger summary, and final simulation reporting
- added simulation documentation and regression coverage while preserving the existing sauna proof loop and local guardrails

## v0.2.2 - Public Release Candidate

- added public release notes, checklist, demo walkthrough, reviewer packet, feedback form, and positioning docs
- hardened README for five-minute stranger review and reproducible local proof commands
- completed release-candidate language audit for marketplace, hiring, build-approval, and routing guardrails
- preserved the existing local-only proof loop without adding new protocol capability

## v0.2.1 - Local Quote Comparison Summary

- added deterministic local comparison of multiple quote responses for information quality only
- added two additional sauna quote response examples for comparison scenarios
- added machine-readable and human-readable quote comparison summary outputs
- preserved guardrails against contractor selection, hiring approval, and build approval


## v0.2 - Quote Response & Outcome Seed

- added local quote-response validation and comparison-readiness reporting
- added deterministic build-packet quote-readiness scoring outputs
- added local synthetic negotiation event generation
- added local synthetic outcome event generation
- added second small reference project for simpler coverage
- expanded tests for quote response, negotiation, outcome, and quote-readiness scoring
- kept all outputs local with no routing, messaging, hosted APIs, or autonomous action

## v0.1 - Protocol Seed

- established the core protocol project structure
- added build packet, quote request, quote response, negotiation, and outcome schemas
- added sauna reference example and generation scripts
- added validation, RFQ, and agent manifest outputs
- established guardrails, doctrine, and open-core positioning