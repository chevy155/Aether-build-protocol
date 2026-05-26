# Machine Response Envelope Spec

## Purpose

The machine response envelope is the deterministic wrapper that Aether returns to agent systems when describing local operations, failures, warnings, refusals, and human approval gates.

## Required Fields

- `response_id`
- `response_type`
- `status`
- `timestamp`
- `protocol_version`
- `operation`
- `artifact_id`
- `human_review_required`
- `external_action_taken`
- `message`
- `next_safe_actions`
- `forbidden_actions`
- `evidence`
- `errors`
- `warnings`

## Safety Rule

`external_action_taken` must always be `false`.

This is the machine-readable proof that Aether did not send an email, call a webhook, contact a supplier, route a quote, approve fabrication, approve payment, or certify anything.

## Response Types

- `success`
- `error`
- `warning`
- `refusal`
- `human_approval_required`

## Additional Rules

- forbidden actions must not appear in `next_safe_actions`
- human approval required responses must keep `human_review_required: true`
- refusal responses must explicitly name the refused action in `forbidden_actions`