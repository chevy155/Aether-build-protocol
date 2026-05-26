# Operations Plan

## Operating Model

The company operates Aether Build Protocol as infrastructure, not as an execution system.

The protocol is used to normalize project intent, identify gaps, prepare quote requests, and support later routing decisions.

## How Builders And Companies Could Build On It

- Builders can map their intake systems to the Build Packet.
- Fabricators can normalize inbound RFQs into the Quote Response contract.
- Design companies can attach CAD-derived metadata later.
- Operators can record negotiation and outcome events into a shared ledger.

## Future Quote Routing

Future quote routing should work as a human-approved layer on top of the protocol:

1. Build Packet validated.
2. Quote Request generated.
3. Human reviews scope, risk, unknowns, and licensed trade flags.
4. Human selects target shops or suppliers.
5. Responses are normalized back into Quote Response objects.

## Human Approval Workflow

- Human approves the Build Packet before outbound use.
- Human approves every Quote Request before any supplier sees it.
- Human reviews all Quote Responses before negotiation.
- Human approves any negotiated change that affects scope, cost, lead time, safety, or permits.

## Risk And Safety Operations

- Flag safety-critical items in the packet and manifest.
- Flag licensed-trade requirements in both validation and quote generation.
- Flag code and permit review requirements.
- Preserve site conditions and unknowns.
- Reject any downstream process that attempts to suppress unknowns or approval gates.
