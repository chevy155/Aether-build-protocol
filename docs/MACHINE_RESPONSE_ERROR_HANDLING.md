# Machine Response Error Handling

## Purpose

The deterministic machine response system gives agents a stable way to understand what failed, why it failed, and what the next safe local action should be.

## Why This Matters

In Aether, response envelopes are not just API returns. They teach machines how to behave safely around physical execution workflows.

## Required Error Traits

- deterministic code
- explicit message
- likely cause
- suggested action
- safe retry signal
- human review requirement
- forbidden action boundary

## Human Approval Boundary

If a response indicates `human_approval_required`, the machine must not cross the external boundary on its own.

## Refusal Boundary

If a response is a refusal, the machine must stop the unsafe action and remain inside local-only behavior.