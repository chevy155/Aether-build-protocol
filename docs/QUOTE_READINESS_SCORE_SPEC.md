# Quote Readiness Score Spec

## Purpose

Measure whether a quote response is structured enough to compare against other responses.

## Scoring Fields

The v0.2 score checks whether the response contains:

The v0.2 build-packet quote-readiness score checks:

- required_fields_present
- bom_completeness
- dimensions_and_tolerances
- site_conditions
- licensed_trade_flags
- code_permit_review_flags
- safety_notes
- unknowns_preserved
- assumptions_present
- capability_requirements
- quote_categories
- human_approval_gate

## Interpretation

- 85-100: structured enough for human quote review
- 60-84: needs human completion before quote review
- below 60: not ready for quote review
- missing fields or schema gaps must be listed explicitly

## Status Values

- `READY_FOR_HUMAN_QUOTE_REVIEW`
- `NEEDS_HUMAN_COMPLETION_BEFORE_QUOTE_REVIEW`
- `NOT_READY_FOR_QUOTE_REVIEW`

## Limit

This score never says approved to build.

It only judges whether the build packet is structured enough for human quote review.
