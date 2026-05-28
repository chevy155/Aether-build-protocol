---
title: Aether CAD-to-Agent Sandbox
emoji: 🛠️
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: "4.44.1"
python_version: "3.12"
app_file: app.py
pinned: false
short_description: Agent-safe CAD-to-fabrication sandbox.
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
---

# Aether CAD-to-Agent Sandbox

Aether Build Protocol is an open, local-first protocol for machine-readable physical build intent.

This Space is the interactive demo. GitHub is the source of truth.

⭐ Source code, schemas, tests, OpenAPI contract, MCP skeleton, and full protocol docs:
https://github.com/chevy155/Aether-build-protocol

Try the dataset:
https://huggingface.co/datasets/lonestar155/aether-build-protocol-examples

This demo shows how a simple part request can be converted into:

- Build Packet preview
- Quote Request preview
- Human Approval Required response
- Machine Response Envelope
- Forbidden Actions list

## Why this matters

Designers and builders often know what they want made, but the request is trapped in CAD screenshots, rough notes, PDFs, email threads, and incomplete RFQs.

AI agents and future machine-to-machine systems cannot safely coordinate physical work from ambiguous intent.

Aether explores the structured layer between design intent and fabrication review. It is a design-to-fabrication protocol for machine-readable physical build intent, RFQ validation, and an agent-safe manufacturing workflow with human approval gates. The repository also includes deterministic machine response envelopes, OpenAPI surfaces, an MCP skeleton, provenance signals, and a digital thread that can be inspected locally.

## What this demo does

The demo converts a simple part request into:

- Build Packet preview
- Quote Request preview
- Human Approval Required response
- Machine Response Envelope
- Forbidden Actions list

## What to do next

- Star the GitHub repo if this direction is useful.
- Fork it if you want to test the protocol locally.
- Open an issue if a Build Packet field is missing.
- Open an issue if the protocol makes a dangerous assumption.
- Open an issue if you know fabrication, CAD, procurement, or agent tooling and want to critique the workflow.

GitHub:
https://github.com/chevy155/Aether-build-protocol/issues

## What this demo is not

- not a marketplace
- not supplier routing
- not real quote generation
- not autonomous ordering
- not fabrication approval
- not engineering approval
- not payment approval
- not load certification
- no real shop is contacted

This demo makes no network calls, does not route quotes, and does not perform real manufacturing actions.

## For AI agents and developers

Start here:
1. Read machine/llms.txt in the GitHub repo.
2. Inspect machine/aether_agent_manifest.json.
3. Inspect machine/permission_manifest.json.
4. Inspect openapi/aether.openapi.yaml.
5. Inspect mcp/mcp_manifest.json.
6. Run scripts/run_agent_readiness_check.py locally.

This is designed to be machine-readable and human-gated, not autonomous by default.

## Feedback requested

If you are a fabricator, CAD designer, project engineer, AI developer, or manufacturing operator, the useful feedback is:

- What fields are missing before real shop review?
- What would a real shop reject?
- What assumptions are dangerous?
- What should an AI agent never be allowed to do?
- Does this reduce ambiguity before quoting?