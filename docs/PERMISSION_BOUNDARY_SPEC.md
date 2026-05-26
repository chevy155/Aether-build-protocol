# Permission Boundary Spec

## Purpose

Permission boundaries define the ceiling for sandbox behavior.

## Boundary Classes

- globally allowed local actions
- globally forbidden actions
- actions that require explicit human approval

## Required Safety Outcomes

- no email sending
- no webhook calling
- no supplier contact
- no quote routing
- no contractor selection
- no build approval
- no fabrication approval
- no engineering approval
- no payment approval
- no load certification
- no reading outside the repository
- no external API calling
- no network scanning

## Human-Gated Actions

Publishing, external sharing, company pilot start, production integration, supplier contact, and enabling real outbound integrations remain human-gated.