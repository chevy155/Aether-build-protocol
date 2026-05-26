# Negotiation Event Spec

## Purpose

Record a local, human-reviewed change event tied to a quote request and quote response.

## Required Fields

- `negotiation_event_id`
- `quote_request_id`
- `quote_response_id`
- `event_type`
- `actor`
- `timestamp`
- `change_summary`
- `before`
- `after`
- `human_approval_required`

## v0.2 Boundary

Negotiation events in v0.2 are synthetic local examples only.

They do not imply real supplier communication, acceptance, counterparty routing, or contract formation.

## Guardrail

Every negotiation event must preserve the human approval gate.
