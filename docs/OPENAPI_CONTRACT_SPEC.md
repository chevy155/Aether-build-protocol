# OpenAPI Contract Spec

## Purpose

The OpenAPI contract gives agents and developers a standard machine-readable view of Aether operations without requiring a live hosted API.

## Scope

The contract covers local conceptual endpoints for:

- Build Packet validation
- Quote Request generation
- Quote Response validation
- Quote comparison generation
- Human Approval Event recording
- Provenance manifest generation
- discovery of manifests, schemas, tools, and errors

## Non-Goals

- no hosted deployment
- no supplier routing
- no email sending
- no webhook delivery
- no build or fabrication approval
- no engineering approval
- no payment approval

## Safety Rule

Every endpoint must preserve local-only and human-gated language.