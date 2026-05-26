# Quote Comparison Summary Spec

## Purpose

Compare multiple local quote responses for information quality only.

## Scope

This summary evaluates completeness, disclosure quality, risk clarity, and human-review readiness.

It does not rank contractors, choose vendors, approve hiring, or approve building.

## Inputs

- one or more local quote response JSON files

## Outputs

- `outputs/quote_comparison_summary_latest.json`
- `outputs/quote_comparison_summary_latest.md`

Optional example mirrors may also be written under `examples/sauna_node/`.

## Scoring Categories

- response_completeness
- scope_clarity
- assumptions_clarity
- exclusions_clarity
- price_range_clarity
- lead_time_clarity
- risk_disclosure
- clarification_quality
- human_review_readiness

## Allowed Labels

- `MOST_COMPLETE_FOR_HUMAN_REVIEW`
- `COMPARISON_READY`
- `NEEDS_CLARIFICATION_BEFORE_COMPARISON`
- `NOT_COMPARISON_READY`

## Forbidden Labels

- best contractor
- winner
- approved
- recommended to hire
- ready to build

## Guardrails

- local files only
- no marketplace behavior
- no external communication
- no supplier routing
- no hiring or build approval
- human review required remains visible

## Acceptance Criteria

- multiple quote responses can be scored locally
- each response score is between 0 and 100
- missing fields and clarification needs are visible
- human review requirement is preserved
- highest comparison-ready response can be marked `MOST_COMPLETE_FOR_HUMAN_REVIEW`
- no forbidden language appears in the summary
