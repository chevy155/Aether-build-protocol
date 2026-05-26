# Quote Response Spec

The Quote Response is a normalized answer to a Quote Request.

Required fields:

- `quote_response_id`
- `quote_request_id`
- `responder_name`
- `responder_type`
- `quoted_scope`
- `price_min`
- `price_max`
- `currency`
- `lead_time_min_days`
- `lead_time_max_days`
- `assumptions`
- `exclusions`
- `substitutions`
- `confidence_score`
- `risk_notes`
- `clarification_questions`
- `human_review_required`

The response must preserve confidence, assumptions, exclusions, and clarification requests.
