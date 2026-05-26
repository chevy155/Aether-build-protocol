# Action Sandbox Spec

## Purpose

The action sandbox constrains the ASI Network Sense Sandbox to read, validate, summarize, and recommend local next steps only.

## Allowed Action Families

- manifest reading
- schema reading
- protocol artifact reading
- local validation
- local report generation
- local gap identification
- reviewer packet generation
- safe next-step recommendation

## Refused Action Families

- sending real email
- calling real webhooks
- contacting suppliers
- routing quotes
- selecting contractors
- approving hiring
- approving build or fabrication
- approving engineering or payment
- certifying load rating
- reading outside the repository
- calling external APIs
- scanning networks

## Output Contract

The sandbox may emit recommendations, but every recommendation must preserve the local-only and human-gated boundary.