# API Contract

## Inbound Contract

The sandbox accepts three local inputs:

- `inbound/company_project_payload.json`
- `inbound/company_bom_export.csv`
- `inbound/company_drawing_manifest.json`

## Required Payload Concepts

- company project ID
- project name and description
- required capabilities
- BOM reference
- drawing manifest reference
- material and finish targets
- dimensions summary
- unknowns
- assumptions
- human approval required

## Mapping Target

These inputs map into:

- `mapped/build_packet.yaml`
- `mapped/quote_request.json`

The contract is deterministic and local-only. No network endpoint is called.
