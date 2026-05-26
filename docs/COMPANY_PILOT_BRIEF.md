# Company Pilot Brief

## Pilot Offer

**Aether Company Integration Sandbox Pilot**

A local-first, human-gated integration pilot that maps one non-sensitive company project into Aether Build Packets, Quote Requests, Human Approval Events, notification previews, webhook previews, provenance manifests, and a final integration findings report.

This is the first commercially legible Aether package: not a full production integration, not a marketplace connection, and not an automation rollout. It is a scoped pilot that shows how a real company project could be made machine-readable, reviewable, and audit-friendly inside the company's own boundary.

## What The Pilot Is

The pilot is a short, controlled integration exercise using one company-provided project that is safe to use for internal evaluation.

The goal is to prove five things:

- the company's intake data can be structured locally
- the project can be mapped into Aether-native protocol artifacts
- human approval boundaries can be made explicit
- preview-only notification and webhook surfaces can be generated without external action
- provenance and findings can be captured in a way a real operations team can inspect

This is a sandbox pilot, not a production deployment.

## What The Company Provides

The company provides one non-sensitive project package for internal evaluation. That package should usually include:

- one project description or intake summary
- one BOM export or structured parts list
- one drawing manifest, print list, or file inventory
- required capabilities or process notes if known
- known unknowns, constraints, or review questions if available

The project should be suitable for internal review and safe to use in a local-first sandbox exercise. It should not require sharing regulated, highly sensitive, export-controlled, or production-critical data.

## What Aether Generates

For the pilot, Aether generates a deterministic local artifact chain around the company project. That output can include:

- a mapped `build_packet`
- a mapped `quote_request`
- a `human_approval_event`
- preview-only email notification output
- preview-only webhook payload output
- an artifact provenance manifest with `sha256` hashes
- an integration event log showing no external action was taken
- a final integration findings report summarizing fit, gaps, assumptions, and next steps

The point is not to automate execution. The point is to make the company's project handoff legible, reviewable, and auditable.

## What Is Explicitly Not Allowed

This pilot must stay inside strict guardrails.

It does not allow:

- production integration
- real supplier contact
- real quote routing
- real email sending
- real webhook delivery
- fabrication approval
- engineering approval
- payment approval
- hiring approval
- contractor selection
- load certification
- autonomous external action of any kind

Human approval remains required before any future external step.

## What Success Looks Like

The pilot is successful if a company can look at one real but non-sensitive project and say:

- "Yes, this represents our intake data in a recognizable way."
- "Yes, the mapped artifacts are structured enough to be operationally useful."
- "Yes, the human approval boundary is explicit."
- "Yes, the provenance and event trail are credible."
- "Yes, this could become a real internal integration path later."

Success does not mean the company is live in production. Success means the company can clearly see the path from its current project intake format to a future internal integration.

## Deliverables

The pilot deliverables should be simple and inspectable.

- one pilot input package from the company
- one Aether-generated artifact set for that project
- one provenance manifest
- one integration event log
- one findings brief summarizing fit, gaps, assumptions, and recommended next steps
- one review session walking through the outputs and guardrails

If useful later, the findings brief can also identify what would be required for a second pilot phase.

## Later Price Range

This should be framed as a later paid pilot, not as an open-ended implementation commitment.

An initial commercial range could likely sit in the low five figures for one scoped, non-sensitive project pilot with one review cycle and one findings report.

A reasonable placeholder range for later company conversations is:

- roughly `$8,000-$20,000` for a narrowly scoped sandbox pilot

That range would depend on:

- cleanliness of the company's source artifacts
- amount of mapping work required
- number of review iterations
- whether the company wants only a findings brief or also a more explicit phase-two integration plan

## Positioning For A Company Conversation

The clean way to present this is:

"Aether Company Integration Sandbox Pilot is a local-first, human-gated pilot that shows how one company project can be translated into machine-readable build coordination artifacts without triggering any real external action."

That keeps the offer concrete, commercially legible, and inside the current technical truth of the product.