# Approval Workflow

## Sandbox Flow

1. Load the fake company profile and inbound payload.
2. Map the payload into an Aether `build_packet`.
3. Derive an informational `quote_request`.
4. Create a `human_approval_event` with the decision `approved_for_internal_review_only`.
5. Generate preview-only notification artifacts.
6. Record provenance hashes and event-log entries.

## Required Approval Rule

The human approval event is still not a build approval, fabrication approval, engineering approval, or payment approval. It only documents that the next stage still requires human review.
