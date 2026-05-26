# Aether Build Protocol v0.2.3 End-to-End Fabrication Simulation Harness

Aether Build Protocol is the machine-readable coordination layer between digital design intent and downstream fabrication review systems.

It turns project intent, geometry, BOM data, trade requirements, unknowns, and risk flags into validated protocol objects that can move cleanly between builder-side systems, quote-review workflows, and future execution infrastructure.

## Purpose

Aether Build Protocol serves as the foundational digital coordination network for machine-readable hardware execution.

It establishes a standardized data highway between upstream design environments such as CAD metadata, generative geometry, structured BOMs, and drawing packages, and downstream fabrication-review systems that need explicit scope, risk, and traceable handoff artifacts.

This repository demonstrates the local cognitive layer of that network. It ingests, validates, transforms, and deterministically scores protocol artifacts so teams can inspect data completeness, structural risk, trade constraints, and lead-time alignment before any external action is authorized.

The point is not to claim autonomous fabrication. The point is to make the handoff between design intent and physical execution legible, auditable, and automation-ready while preserving human approval gates and safety-critical unknowns.

## What It Is

- A protocol seed for physical build intent.
- A schema set for Build Packets, Quote Requests, Quote Responses, Negotiation Events, and Outcome Events.
- A validation and document-generation toolkit.
- A reference example proving the protocol can describe a multi-trade sauna build.
- A foundation other companies, agents, CAD systems, and future AGI/ASI systems can build on.

## What It Is Not

- Not a marketplace.
- Not a web app.
- Not a contractor network.
- Not a quoting platform yet.
- Not an autonomous build execution system.
- Not an autonomous ordering system.
- Not a payments product.
- Not supplier routing.
- Not a hosted SaaS service.

## Why It Exists

Physical projects are still described in fragmented ways: CAD files, ad hoc notes, spreadsheets, emails, drawings, and vendor-specific quote formats. That fragmentation slows review, quoting, negotiation, and execution.

Aether Build Protocol creates a common machine-readable language between digital design intent and physical execution systems. It preserves unknowns, flags risk, and standardizes the data needed for later routing, quoting, and controlled automation layers without collapsing the human review boundary.

## AGI/ASI Era Relevance

As AI systems become capable of generating design intent, build plans, and vendor routing strategies, physical execution will need a protocol layer that is explicit, auditable, and safe. Aether Build Protocol is intended to become that layer.

It gives future human, AI, AGI, and ASI systems a structured contract for:

- build intent capture
- quote-readiness validation
- quote request generation
- quote response normalization
- negotiation event tracking
- outcome and trust ledger recording

## How Companies Can Build On It

- Use the schemas as a shared protocol contract.
- Build internal quoting or routing software on top of the validator and generators.
- Add CAD adapters later for SolidWorks, Fusion, Onshape, and other tools.
- Build supplier-routing systems later with explicit human approval gates.
- Build outcome-ledger analytics later using normalized quote and delivery events.

Commercial support, private deployment, and protocol extension work can be offered later, but this repository contains no hosted service or payment links.

## Suggested GitHub Topics

manufacturing, cad, rfq, construction-tech, procurement, schema, json-schema, fabrication, open-protocol, ai-agents, physical-ai, design-to-manufacturing

## Reference Examples

The primary closed-loop reference packet lives in `examples/sauna_node/`.

It demonstrates a multi-trade outdoor sauna project with:

- cedar interior
- stone accent wall
- Harvia heater
- LED lighting
- angled roof
- ventilation
- outdoor shower
- cold plunge pad
- waterproofing and drainage
- electrical scope
- licensed electrician requirement
- code and permit review flags

A second small reference packet lives in `examples/micro_shelter_node/` to prove the protocol can also describe a simpler local project without licensed-trade scope.

## Run Commands

From the repository root:

```powershell
python scripts/simulate_industrial_hook_pipeline.py
python scripts/validate_build_packet.py examples/sauna_node/build_packet.yaml
python scripts/generate_quote_request.py examples/sauna_node/build_packet.yaml
python scripts/generate_rfq_markdown.py examples/sauna_node/quote_request.json
python scripts/validate_quote_response.py examples/sauna_node/quote_response_example.json
python scripts/score_quote_readiness.py examples/sauna_node/build_packet.yaml
python scripts/generate_negotiation_event.py examples/sauna_node/quote_request.json examples/sauna_node/quote_response_example.json
python scripts/generate_outcome_event.py examples/sauna_node/quote_response_example.json
python scripts/generate_quote_comparison_summary.py examples/sauna_node/quote_response_example.json examples/sauna_node/quote_response_example_2.json examples/sauna_node/quote_response_example_3.json
python scripts/generate_agent_manifest.py examples/sauna_node/build_packet.yaml
python -m pytest tests/ -v
```

## End-to-End Fabrication Simulation

Run the local-only end-to-end simulation with:

```powershell
python scripts/simulate_industrial_hook_pipeline.py
```

It simulates a builder-to-fabricator protocol handoff using a mock industrial-style steel utility hook.

- local only
- no real CAD parsing
- no supplier contact
- no fabrication approval
- no engineering approval
- no load certification
- human review required

The harness writes a full artifact chain under `simulations/industrial_hook/`, including builder workspace inputs, Aether protocol artifacts, deterministic fabricator outputs, monitoring logs, and a final simulation report.

## Closed Loop

v0.2 closes the local protocol loop:

Build Packet -> Quote Request -> RFQ -> Quote Response -> Negotiation Event -> Outcome Event seed.

The most important new artifact is the quote-response validation report. It determines whether a response is clean enough to compare by checking assumptions, exclusions, price range, lead time, confidence, substitutions, risk notes, and clarification questions.

## v0.2 Local Extensions

- Quote response validation remains local and synthetic.
- Quote readiness scoring is deterministic and only measures quote-review readiness.
- Negotiation events are local synthetic examples only.
- Outcome events are local synthetic examples only.
- All of these artifacts require human review and do not imply approval to build, engineer, permit, or route.

## v0.2.1 Local Quote Comparison Summary

- Local-only quote comparison summary compares quote response completeness and clarity.
- It compares information quality only and does not select vendors.
- It does not approve hiring.
- It does not approve building.
- Human review remains required.

## Controlled Alpha Status

The repository is in controlled alpha review status. It is public-ready as an open protocol seed, but it is not a marketplace launch, hiring workflow, build approval system, or hosted product.

## How To Run The Local Quote-Response Loop

1. Validate the Build Packet.
2. Generate the Quote Request.
3. Generate the human-readable RFQ.
4. Validate the Quote Response.
5. Score quote-readiness from the Build Packet.
6. Generate synthetic local negotiation and outcome examples.
7. Generate a local quote comparison summary.
8. Run the test suite.

## Guardrails

- Human approval is required before any external quote request is sent.
- The protocol never autonomously builds, orders, contracts, pays, or contacts suppliers.
- Licensed trades must be flagged.
- Code review and permit review requirements must be flagged.
- Safety-critical notes must be preserved.
- Unknowns are first-class fields and must never be hidden.
- Quote responses must preserve assumptions, exclusions, confidence, and clarifications.

See `docs/GUARDRAILS.md` for the canonical guardrail set.

## Current Limitations

- No marketplace.
- No supplier routing.
- No real quote negotiation transport.
- No CAD plugin.
- No automated external actions.
- No hosted service.
- No user accounts.
- No payment flow.

## Controlled Alpha Doctrine

This v0.2 seed should be exercised through controlled internal or partner review only. No public launch.

## Next Build Phase

The next recommended phase is public release packaging and controlled reviewer exposure, while keeping all protocol comparisons local-only and human-reviewed.

## Repo Structure

```text
Fractal_Infinity_Aether/
  README.md
  MASTER_DOCTRINE.md
  docs/
  protocols/build_intent/schemas/
  examples/micro_shelter_node/
  examples/sauna_node/
  scripts/
  tests/
  outputs/
```
