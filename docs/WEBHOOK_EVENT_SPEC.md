# Webhook Event Spec

## Purpose

The webhook artifact in v0.2.4 is a preview payload only. It exists to show the shape of a possible outbound integration event without making any network call.

## Required Fields

- `event_id`
- `event_type`
- `project_id`
- `artifact_id`
- `status`
- `timestamp`
- `requires_human_review`
- `webhook_called`
- `forbidden_actions_confirmed`
- `artifact_paths`

## Sandbox Rules

- `webhook_called` must be `false`.
- The payload should use the phrase `preview only` or `sandbox` to make the boundary explicit.
- The payload must confirm that no supplier was contacted.
- The payload must confirm that no quote was routed.
- The payload must confirm that no contractor was selected.
- The payload must confirm that no build, fabrication, engineering, payment, or certification action was approved.
- The payload should state `not production integration` when describing the preview boundary.
- The payload must reference the local artifact paths that drove the preview.

## Non-Claim

This file is not evidence of a real company webhook integration. It is only a deterministic preview contract for review.
