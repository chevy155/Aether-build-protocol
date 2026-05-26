# Company Integration Architecture

## Purpose

Aether Build Protocol v0.2.4 adds a fake company integration sandbox for Northstar Fabrication Systems. The goal is to show how a fabrication company could map its local project payload into Aether-native artifacts without contacting anyone or authorizing any real-world work.

## Architecture

1. Local company payload enters through `integrations/company_sandbox/inbound/`.
2. The sandbox maps that payload into Aether-native artifacts under `integrations/company_sandbox/mapped/`.
3. Human-review and preview-only outbound artifacts are written to `integrations/company_sandbox/outbound/`.
4. Provenance and event tracking artifacts are written to `integrations/company_sandbox/ledger/`.

## Inputs

- `company_profile.json`
- `inbound/company_project_payload.json`
- `inbound/company_bom_export.csv`
- `inbound/company_drawing_manifest.json`

## Mapped Aether Artifacts

- `mapped/build_packet.yaml`
- `mapped/quote_request.json`
- `mapped/human_approval_event.json`

## Preview-Only Outbound Artifacts

- `outbound/notification_event.json`
- `outbound/email_preview.md`
- `outbound/webhook_payload.json`

## Ledger Artifacts

- `ledger/integration_event_log.jsonl`
- `ledger/company_integration_summary.json`
- `ledger/artifact_provenance_manifest.json`

## Guardrails

- Fake company only.
- Local-only sandbox.
- No real API server.
- No real email provider.
- No real webhook delivery.
- No supplier contact.
- No quote routing.
- No build approval.
- No fabrication approval.
- No engineering approval.
- No payment approval.
- No load certification.
- Human approval remains required before any external release.

## Run Command

```powershell
python scripts/simulate_company_integration.py
```
