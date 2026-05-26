# Deterministic Error Catalog

## Purpose

Agents need exact failure surfaces. The deterministic error catalog gives them stable error codes, likely causes, and safe next actions.

## What It Enables

- consistent local correction loops
- safer agent self-correction
- clearer human review handoffs
- fewer ambiguous failure states

## Key Errors

- `BUILD_PACKET_SCHEMA_INVALID`
- `QUOTE_REQUEST_GENERATION_FAILED`
- `QUOTE_RESPONSE_SCHEMA_INVALID`
- `QUOTE_RESPONSE_MISSING_ASSUMPTIONS`
- `QUOTE_RESPONSE_MISSING_EXCLUSIONS`
- `QUOTE_RESPONSE_MISSING_LEAD_TIME`
- `HUMAN_APPROVAL_REQUIRED`
- `ENGINEERING_REVIEW_REQUIRED`
- `LOAD_CERTIFICATION_NOT_PROVIDED`
- `EXTERNAL_ACTION_FORBIDDEN`
- `EMAIL_PREVIEW_ONLY`
- `WEBHOOK_PREVIEW_ONLY`
- `PROVENANCE_HASH_MISSING`
- `UNSAFE_APPROVAL_LANGUAGE_DETECTED`
- `FABRICATOR_REJECTION_REQUIRED`
- `REAL_CAD_PARSER_NOT_AVAILABLE`
- `REAL_COMPANY_SYSTEM_NOT_CONNECTED`

## Safety Rule

Deterministic errors should guide agents toward local correction or human escalation, not unsafe automation.