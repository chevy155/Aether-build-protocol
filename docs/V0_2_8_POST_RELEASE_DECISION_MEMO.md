# v0.2.8 Post-Release Decision Memo

## Status

COMPLETE.

v0.2.8 successfully moved Aether from agent-readable documentation into bounded agent-proof behavior. The release proves that a local agent-style workflow can discover protocol surfaces, map a synthetic CAD/job request into a valid Build Packet, run local validation, detect and repair invalid output, block forbidden external actions, preserve human approval requirements, and emit proof artifacts.

## Final Validation

- `python scripts/run_mcp_drive_agent_test.py` -> PASS
- `python -m pytest tests/agent_readiness/test_mcp_drive_agent_proof.py -q` -> 1 passed
- `python -m pytest -q` -> 30 passed
- `outputs/mcp_drive/latest_agent_run_report.json` -> `proof_status: PASS`

## Release State

- GitHub release published.
- Tag `v0.2.8-agent-proof` pushed.
- PR #1 merged into `main`.
- `main` validated green after merge.

## Guardrail State

- No Path B scope added.
- No live API gateway.
- No mTLS.
- No webhooks.
- No email relay.
- No hosted API behavior.
- No production MCP integration.
- No ERP connectivity.
- No external company integration.

## Decision

Do not begin implementation of the live gateway yet.

## Recommended Next Vector

Run Alpha Triage + v0.3 Architecture Scoping, not v0.3 implementation.

## Reason

The protocol now has local agent proof. The next risk is not "can we build more?" The next risk is "what should the live gateway actually expose, and what do real reviewers misunderstand, distrust, or need before connecting a company system?"

Path B should begin only as architecture/specification, not production code.

## Next Bounded Phase

v0.2.9 or v0.3-planning - Edge Node Architecture Decision Record.

## Scope

- Read alpha reviewer feedback.
- Extract trust concerns, integration blockers, unclear terminology, and buyer objections.
- Draft live gateway architecture without implementation.
- Define mTLS, webhook, email relay, ERP adapter, approval boundary, tenant isolation, and audit trail requirements.
- Produce a GO / NO-GO gate for actual Path B implementation.

## Explicit Non-Goals

- Do not write live gateway code yet.
- Do not add real external integrations yet.
- Do not create production secrets or hosted behavior yet.

## Final Recommendation

Close v0.2.8. Start a new planning branch for v0.3 architecture only.