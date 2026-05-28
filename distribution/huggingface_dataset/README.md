---
pretty_name: Aether Build Protocol Examples
license: mit
language:
  - en
tags:
  - manufacturing
  - fabrication
  - cad
  - rfq
  - mcp
  - openapi
  - ai-agents
  - machine-to-machine
  - design-to-manufacturing
  - physical-ai
  - json-schema
  - digital-thread
  - human-in-the-loop
task_categories:
  - text-generation
  - question-answering
size_categories:
  - n<1K
---

# Aether Build Protocol Examples

Aether Build Protocol Examples is a small public dataset of machine-readable physical build intent artifacts.

It is designed for AI developers, agent-framework builders, CAD/design workflows, fabrication review systems, and researchers studying machine-to-machine physical transaction protocols.

GitHub source of truth:
https://github.com/chevy155/Aether-build-protocol

Live demo:
https://huggingface.co/spaces/lonestar155/aether-cad-to-agent-sandbox

Open issues / feedback:
https://github.com/chevy155/Aether-build-protocol/issues

## What is included

This dataset contains example artifacts from Aether Build Protocol:

- Build Packet example
- Quote Request example
- Quote Response example, if present
- Human Approval Event example
- Machine Response Envelope example
- Agent Readiness Report example
- M2M Print Transaction Summary example

## Why this exists

AI agents cannot safely coordinate physical work from ambiguous PDFs, screenshots, email threads, and loose CAD notes.

They need structured data contracts, permission boundaries, deterministic response envelopes, and human approval gates.

Aether provides example artifacts for the emerging layer between design intent and physical execution.

## Primary use cases

- machine-readable physical build intent research
- RFQ normalization experiments
- quote-response validation
- agent-safe manufacturing workflow design
- human-gated design-to-fabrication coordination
- MCP/OpenAPI manufacturing protocol exploration
- digital-thread and provenance research

This dataset is also useful as a small example corpus for an agent-safe design-to-fabrication workflow, an MCP/OpenAPI manufacturing protocol, a human-gated physical transaction pathway, RFQ validation, and quote-response validation.

## For AI agents and developers

This dataset is intended as a small example corpus for machine-readable physical build intent.

Suggested path:
1. Inspect the examples in this dataset.
2. Open the GitHub repo.
3. Read machine/llms.txt.
4. Inspect the schema index and permission manifest.
5. Run the fresh-clone agent-readiness check.
6. Open an issue with missing fields, unsafe assumptions, or integration suggestions.

## Guardrails

These are synthetic examples only.

This dataset is a local-only sandbox for structured physical build intent examples.

No real shop was contacted.
No quote was routed.
No print was approved.
No fabrication was approved.
No engineering approval was granted.
No payment was approved.
No load certification was granted.
No delivery authorization was granted.

Human approval required before any external interpretation or real-world action.

## Feedback requested

Useful feedback includes:

- What fields are missing for real fabrication review?
- What would a shop need before quoting?
- Which schema fields are unclear?
- What additional artifacts would help designers and fabricators?
- What should an AI agent never be allowed to do in this workflow?