# Capability Manifest Spec

## Purpose

Each resource manifest explains what a resource is for, what artifacts belong to it, what scripts and tests cover it, and what actions a future agent may or may not take around it.

## Required Fields

- `resource_id`
- `purpose`
- `artifacts`
- `schemas_used`
- `scripts_used`
- `tests_covering_resource`
- `generated_outputs`
- `allowed_agent_actions`
- `forbidden_agent_actions`
- `required_human_approvals`
- `known_limitations`
- `evidence_paths`

## Safety Rule

No capability manifest may list a globally forbidden action as an allowed agent action.

## Interpretation Rule

Capability manifests describe local reasoning affordances only. They do not grant production authority.