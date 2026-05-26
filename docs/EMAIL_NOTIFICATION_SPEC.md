# Email Notification Spec

## Purpose

The email artifact in v0.2.4 is a markdown preview only. It demonstrates how a company-facing notification could be rendered while preserving the sandbox rule that no real message is sent.

## Required Content

The preview must make all of the following clear:

- it is a sandbox-only preview
- no real email sent
- no supplier was contacted
- no quote was routed
- no build was approved
- no fabrication was approved
- no engineering approval was granted
- no webhook called
- not production integration
- human approval is required before any external release

## Allowed Output

A preview file under `integrations/company_sandbox/outbound/email_preview.md`.

## Forbidden Output

- sending a real email
- invoking a provider API
- implying a real quote award or fabrication authorization
