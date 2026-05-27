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

This demo shows how a simple part request can be converted into:

- Build Packet preview
- Quote Request preview
- Human Approval Required response
- Deterministic Machine Response Envelope
- Forbidden Actions list

## Why this matters

Designers, AI agents, and future machine-to-machine systems need a clean way to describe physical work before it becomes a quote, print, fabrication job, or delivery workflow.

Today, physical build requests are often trapped in PDFs, screenshots, loose CAD notes, emails, and ambiguous quote requests. Aether turns the intent into structured artifacts that machines can validate and humans can review.

## Who this is for

- AI developers building agent-safe workflow tools
- CAD designers preparing cleaner quote requests
- fabrication shops tired of incomplete RFQs
- manufacturing operators studying digital-thread workflows
- researchers exploring machine-to-machine physical transaction protocols

## What this demo is

This is a sandbox interface for exploring Aether-style build intent.

It is useful for understanding the protocol shape, response envelopes, and approval boundaries.

## What this demo is not

This demo makes no network calls.
This demo does not contact shops.
This demo does not route quotes.
This demo does not approve printing.
This demo does not approve fabrication.
This demo does not approve engineering.
This demo does not approve payment.
This demo does not certify load rating.
This demo does not perform real manufacturing actions.

## Core phrase

machine-readable physical build intent

## Related project

GitHub:
https://github.com/chevy155/Aether-build-protocol

Dataset:
https://huggingface.co/datasets/lonestar155/aether-build-protocol-examples

## Feedback requested

If you are a fabricator, CAD designer, project engineer, AI developer, or manufacturing operator, the useful feedback is:

- What information is missing before a real shop could quote?
- What assumptions are dangerous?
- What would a fabricator reject?
- What should be added to a Build Packet?
- Does this reduce ambiguity before quoting?