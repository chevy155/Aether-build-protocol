# Shop Profile Spec

## Purpose

This specification defines the fake shop profile format used by the print transaction sandbox.

## Required Fields

- `shop_id`
- `shop_name`
- `shop_type`
- `capabilities`
- `materials_supported`
- `max_part_size`
- `tolerance_capability`
- `finish_options`
- `lead_time_range_days`
- `minimum_order_quantity`
- `requires_engineering_review_for_load_bearing_parts`
- `can_certify_load_rating`
- `sandbox_only`
- `external_contacted`

## Required Safety Semantics

- `can_certify_load_rating` must remain `false`
- `sandbox_only` must remain `true`
- `external_contacted` must remain `false`

## Reference Profiles

### Pacific Layer Works

- FDM, PETG, PLA, ASA
- fast local prototyping
- no SLS
- no engineering certification

### Northstar Additive Lab

- SLS, Nylon PA12, batch production
- stronger nylon options
- longer lead time

### Apex Composite Print

- carbon fiber nylon simulation
- high stiffness material options
- engineering review required
- no load certification in sandbox

## Matching Rule

Shop profiles support human review only.

They may be labeled:

- `MOST_COMPLETE_FOR_HUMAN_REVIEW`
- `NEEDS_CLARIFICATION`
- `NOT_READY_FOR_REAL_RFQ`

They must never be labeled:

- winner
- selected shop
- approved vendor
- proceed to order
- approved to print