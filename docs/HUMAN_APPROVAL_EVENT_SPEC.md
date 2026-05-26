# Human Approval Event Spec

## Purpose

The human approval event is the explicit handoff boundary between deterministic artifact generation and any future external action. In v0.2.4 it is still sandbox-only and does not authorize any external step.

## Required Fields

- `approval_event_id`
- `project_id`
- `artifact_id`
- `approval_type`
- `actor_name`
- `actor_role`
- `timestamp`
- `decision`
- `scope_limitations`
- `notes`
- `human_approval_required_for_next_stage`

## Required Decision Value In Sandbox

The v0.2.4 sandbox uses:

- `approved_for_internal_review_only`

## Required Scope Limitations

The sandbox event must state at minimum that it is:

- not approved for fabrication
- not approved for supplier outreach
- not approved for payment
- not approved for hiring
- not engineering approved
- not load certified

## Non-Authorization Rule

Even when the event decision is present, it is still not a build approval, fabrication approval, engineering approval, payment approval, or load certification.
