# Quote Response Ingestion Spec

## Purpose

Normalize inbound quote responses into a comparable local object.

## Required Fields

- quote response id
- quote request id
- responder name and type
- quoted scope
- price range
- lead-time range
- assumptions
- exclusions
- substitutions
- confidence score
- risk notes
- clarification questions
- human review required

## Comparison Doctrine

A quote response is not comparison-clean if it omits assumptions, exclusions, price range, lead time, confidence, substitutions, risk notes, or clarification questions.

## Operating Boundary

v0.2 ingests and validates locally only.

It does not send messages, route quotes, or contact suppliers.
