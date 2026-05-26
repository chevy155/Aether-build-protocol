# Protocol Overview

## Protocol Stack

1. Build Packet
2. Quote Request
3. Quote Response
4. Negotiation Event
5. Outcome Event

## Build Packet Lifecycle

- Project intent is captured.
- BOM, geometry summary, site conditions, and risk fields are attached.
- Unknowns and assumptions are preserved.
- Validation confirms structural completeness.
- Packet is marked ready for human review, not autonomous execution.

## Quote Request Lifecycle

- Quote scope is derived from the Build Packet.
- Required capabilities and categories are listed.
- Assumptions and clarifications are made explicit.
- Human approval is required before external use.

## Quote Response Lifecycle

- Suppliers or builders answer in a normalized structure.
- Price ranges, lead times, assumptions, exclusions, and clarifications are captured.
- Confidence and risk notes are preserved for auditability.

## Negotiation Lifecycle

- Every material change is recorded as a Negotiation Event.
- Before and after values remain visible.
- Human approval gates remain attached to changes.

## Outcome Ledger Lifecycle

- Final costs, timeline, delivery, inspection status, disputes, and lessons learned are recorded.
- These events become the evidence layer for future trust scoring and routing quality.
