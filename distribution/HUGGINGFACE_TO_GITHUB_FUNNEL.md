# Hugging Face to GitHub Funnel

## Purpose

This document defines how Aether Build Protocol uses Hugging Face as a discovery layer that pushes qualified traffic to GitHub, where the source-of-truth schemas, docs, tests, OpenAPI contract, MCP skeleton, and issue tracker live.

## Public surfaces

- GitHub: https://github.com/chevy155/Aether-build-protocol
- Hugging Face Space: https://huggingface.co/spaces/lonestar155/aether-cad-to-agent-sandbox
- Hugging Face Dataset: https://huggingface.co/datasets/lonestar155/aether-build-protocol-examples

## Desired user path

1. Try the Space as an interactive sandbox.
2. Inspect the Dataset as an example corpus.
3. Visit GitHub for the source of truth.
4. Star or fork the repo if the direction is useful.
5. Open an issue with critique, missing fields, dangerous assumptions, or workflow corrections.
6. Request sandbox review if relevant.

## Desired agent path

1. Discover the Space and Dataset as public entry points.
2. Follow GitHub links to the canonical repo.
3. Read machine/llms.txt.
4. Inspect machine/aether_agent_manifest.json and machine/permission_manifest.json.
5. Inspect openapi/aether.openapi.yaml and mcp/mcp_manifest.json.
6. Run local readiness or review flows.
7. Route substantive feedback to GitHub Issues.

## Calls to action

- Star the GitHub repo.
- Fork the repo for local evaluation.
- Open a GitHub issue with critique or missing schema fields.
- Request sandbox review if the workflow is relevant.
- Request a company integration pilot if the protocol direction is promising.

## What counts as qualified traffic

- GitHub star
- GitHub fork
- GitHub issue
- Hugging Face like
- Hugging Face duplicate
- credible feedback from CAD, fabrication, operator, or developer audiences
- request for sandbox review
- request for company integration pilot

## What not to optimize for

- raw views
- low-quality likes
- vague comments
- hype

## Manual monitoring checklist

- Confirm the Space README links GitHub near the top.
- Confirm the Space app UI shows GitHub and Issues links.
- Confirm the Dataset README points to GitHub as source of truth.
- Confirm both Hugging Face surfaces preserve guardrails.
- Confirm no tracking scripts, cookies, or personal data collection are introduced.
- Confirm no secrets are uploaded.
- Review GitHub stars, forks, and issues for signal quality instead of vanity metrics.