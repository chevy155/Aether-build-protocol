# Webhook Contract

## Purpose

Describe the preview-only webhook payload written to `outbound/webhook_payload.json`.

## Required Behavior

- preview-only payload
- `webhook_called: false`
- references local artifact paths
- confirms that external actions did not occur
- requires human review

## Non-Goal

This contract does not define a real webhook endpoint or delivery mechanism.
