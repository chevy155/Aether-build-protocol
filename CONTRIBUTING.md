# Contributing

## Scope

Contributions should keep Aether Build Protocol infrastructure-first.

Accepted contribution areas:

- schema clarity
- validator improvements
- reference example quality
- deterministic local generators
- docs, tests, and guardrail tightening

Out of scope for this repository stage:

- marketplace features
- UI or frontend work
- supplier routing
- hosted APIs
- payment logic
- autonomous actions

## Workflow

1. Open an issue before major protocol changes.
2. Keep changes narrow and deterministic.
3. Preserve human approval gates, unknowns, and safety flags.
4. Add or update tests for behavior changes.
5. Run `python -m pytest tests/ -v` before opening a pull request.

## Pull Request Expectations

- explain the protocol impact clearly
- note any schema changes explicitly
- update `CHANGELOG.md` for release-relevant changes
- do not introduce external calls or product surfaces outside the repo doctrine
