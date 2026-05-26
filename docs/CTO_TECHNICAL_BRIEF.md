# CTO Technical Brief

## Folder Structure

- `protocols/build_intent/schemas/`: canonical JSON Schemas
- `examples/sauna_node/`: reference build packet and generated artifacts
- `scripts/`: validator and generators
- `tests/`: protocol and script verification
- `outputs/`: latest generated artifacts

## Schema Responsibilities

- `build_packet.schema.json`: canonical project description contract
- `bom_item.schema.json`: BOM item contract
- `capability_requirement.schema.json`: capability requirement contract
- `quote_request.schema.json`: standardized RFQ payload contract
- `quote_response.schema.json`: responder payload contract
- `negotiation_event.schema.json`: audit trail for quote changes
- `outcome_event.schema.json`: delivery and trust ledger event contract

## Script Responsibilities

- `validate_build_packet.py`: schema validation and operational warning summary
- `generate_quote_request.py`: build packet to quote request transformation
- `generate_rfq_markdown.py`: quote request to human-readable RFQ
- `generate_agent_manifest.py`: build packet to machine-readable agent manifest

## Validation Flow

1. Load the build packet YAML.
2. Validate against the Build Packet schema.
3. Report missing or invalid fields.
4. Surface unknowns, safety flags, licensed-trade requirements, and review requirements.
5. Generate downstream artifacts only after the packet is structurally valid.

## Test Plan

- Accept the sauna build packet.
- Reject a packet missing required fields.
- Verify quote request generation contains required fields.
- Verify RFQ output contains the review-only warning.
- Verify the agent manifest includes capabilities and unknowns.
- Verify guardrails appear in both README and Guardrails documentation.
- Verify the outcome event schema requires trust and outcome fields.

## Known Technical Limitations

- No CAD parser.
- No drawing geometry extraction.
- No transport or API layer.
- No schema version negotiation beyond `protocol_version` string usage.
- No external resolver for supplier-specific quote formats yet.
