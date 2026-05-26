# Resource Registry Spec

## Purpose

The resource registry is the top-level inventory of local Aether workspace resources that a future agent may reason over inside the sandbox.

## Required Fields Per Resource

- `resource_id`
- `resource_type`
- `description`
- `manifest_path`
- `source_of_truth_status`
- `trust_level`
- `synthetic_or_real`
- `allowed_read`
- `allowed_write`
- `forbidden_actions`
- `human_approval_required_for`
- `audit_required`
- `provenance_required`

## Registry Rules

- resources must refer to files inside the repository only
- resources must not imply live network discovery
- resources must declare whether they are source-of-truth or simulation-only
- resources must list forbidden actions explicitly
- resources that drive real-world interpretation remain human-review-required

## Non-Goal

The registry is not a system scanner and not a runtime authority engine.