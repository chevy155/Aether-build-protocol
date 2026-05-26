# Master Doctrine

## Core Position

Aether Build Protocol exists to support physical execution infrastructure.

It describes build intent. It does not execute builds.

## Non-Negotiable Rules

- The system never autonomously builds, orders, pays, contracts, or contacts suppliers.
- Human approval is required before any external action.
- Licensed trades must be explicitly flagged.
- Code review and permit review requirements must be explicitly flagged.
- Unknowns must be preserved as first-class protocol fields.
- Safety-critical work must remain visible in every downstream object.
- Quote responses must include assumptions, exclusions, confidence, lead time, risk notes, and clarifications.
- Outcome events become the long-term trust moat.

## Strategic Thesis

The long-term moat is not the schema itself. The moat is the outcome ledger: quote accuracy, build performance, cost variance, delay patterns, clarification patterns, risk patterns, and builder reliability over time.

## Operating Boundary

v0.2 is an internal-only protocol seed.

It may ingest, validate, compare, and record local quote-response, negotiation, and seed outcome objects.

Do not build:

- marketplace logic
- frontend product surfaces
- payments
- contractor onboarding
- autonomous quote submission
- autonomous material ordering
- supplier contact flows
- hosted services
