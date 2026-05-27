# Hacker News Draft

Show HN: Aether Build Protocol, a local-only machine-readable manufacturing sandbox

This repo now includes a deterministic print transaction sandbox that simulates the path from designer request to fake quote responses and local fulfillment artifacts.

The interesting constraint is that every step preserves the no-external-action boundary: no real shop contact, no quote routing, no fabrication approval, no payment approval, and machine responses stay explicit about `external_action_taken: false`.

Feedback I want most: where the schema, state machine, or guardrails are too loose for real machine-to-machine interoperability research.