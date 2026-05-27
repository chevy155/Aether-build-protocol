# M2M Transaction Guardrails

## Guardrail Objective

The Machine-to-Machine Print Transaction Sandbox must remain a local simulation boundary, not a live procurement or manufacturing workflow.

## Required Constraints

- local-only sandbox
- fake shops only
- human approval required
- external actions forbidden by default
- no winner selection
- no real quote routing
- no real fabrication authorization
- no real payment authorization
- no real delivery authorization
- no engineering approval
- no load certification

## Explicitly Forbidden Actions

- send email
- call webhook
- contact supplier
- route quote
- select contractor or shop as winner
- approve print
- approve fabrication
- approve engineering
- approve payment
- approve delivery
- certify load rating
- call external APIs
- scrape networks

## Allowed Local Actions

- generate local transaction artifacts
- validate local payloads
- compare fake shop profiles
- simulate quotes and negotiation
- simulate fulfillment states
- write provenance manifests and guardrail audits
- generate deterministic machine responses

## Reviewer Guidance

If an artifact looks operational, read the guardrail fields before interpreting it.

No artifact in this sandbox should be treated as:

- a real quote
- a selected vendor
- a production work order
- a real shipment
- an engineering signoff
- a payment event

## Approval Boundary

The required human approval event remains limited to:

`decision: approved_for_internal_review_only`

It does not approve:

- external quote routing
- real shop contact
- fabrication
- payment
- delivery
- installation
- engineering
- load certification