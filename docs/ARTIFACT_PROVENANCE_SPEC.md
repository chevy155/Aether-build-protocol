# Artifact Provenance Spec

## Purpose

The provenance manifest proves which sandbox artifacts were generated, how they relate to each other, and what content hash was assigned to each file.

## Required Fields Per Record

- `artifact_id`
- `artifact_type`
- `path`
- `sha256`
- `generated_by`
- `source_artifacts`
- `timestamp`
- `schema_or_contract`
- `human_review_required`

## Required Sandbox Behavior

- Use `sha256` for every tracked artifact.
- Record the local artifact path.
- Record the source artifact chain.
- Record the script that generated the artifact.
- Preserve deterministic timestamps for repeatable regeneration.
- Treat the manifest as a ledger artifact, not an approval artifact.

## Non-Claim

The provenance manifest proves local file lineage only. It does not prove manufacturability, engineering signoff, certification status, or any external action.
