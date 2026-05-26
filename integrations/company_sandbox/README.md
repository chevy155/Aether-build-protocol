# Company Sandbox

This folder contains the v0.2.4 fake company integration sandbox for Northstar Fabrication Systems.

## Purpose

Show how a fabrication company could map a local project payload into Aether-native artifacts without any network call or real-world authorization.

## Structure

- `company_profile.json`
- `inbound/`
- `mapped/`
- `outbound/`
- `ledger/`

## Regeneration

```powershell
python scripts/simulate_company_integration.py
```

## Guardrails

- fake company only
- local-only sandbox
- no real API server
- no real email provider
- no real webhook delivery
- no supplier contact
- no quote routing
- no fabrication approval
- no engineering approval
- no payment approval
- no load certification
