# Transaction State Machine Spec

## Purpose

This specification defines the deterministic state sequence used by the Machine-to-Machine Print Transaction Sandbox.

## State Sequence

1. `REQUEST_CREATED`
2. `BUILD_PACKET_CREATED`
3. `QUOTE_REQUEST_CREATED`
4. `SHOP_MATCH_SIMULATED`
5. `QUOTE_RESPONSES_SIMULATED`
6. `QUOTE_COMPARISON_CREATED`
7. `HUMAN_APPROVAL_REQUIRED`
8. `NEGOTIATION_SIMULATED`
9. `WORK_ORDER_SIMULATED`
10. `DELIVERY_SIMULATED`
11. `OUTCOME_RECORDED`
12. `CLOSED_LOCAL_ONLY`

## Interpretation

These are local transaction lifecycle states only.

They do not imply:

- real RFQ delivery
- vendor selection
- real manufacturing progress
- real shipment progress
- production approval

## Terminal State

`CLOSED_LOCAL_ONLY` means the sandbox completed its local evidence chain and stopped before any external action.

## Approval Behavior

The state machine preserves `HUMAN_APPROVAL_REQUIRED` before any action that would cross the sandbox boundary.