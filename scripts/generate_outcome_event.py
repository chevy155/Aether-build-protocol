from __future__ import annotations

import sys
from pathlib import Path

from protocol_utils import EXAMPLE_DIR, OUTPUT_DIR, build_outcome_event, infer_project_id_from_quote_response, load_json, load_yaml, validate_payload, write_json


def main() -> int:
    base_dir = EXAMPLE_DIR
    quote_response_path = Path(sys.argv[1]) if len(sys.argv) > 1 else base_dir / "quote_response_example.json"
    build_packet_path = Path(sys.argv[2]) if len(sys.argv) > 2 else base_dir / "build_packet.yaml"

    quote_response = load_json(quote_response_path)
    packet = load_yaml(build_packet_path)
    inferred_project_id = infer_project_id_from_quote_response(quote_response)
    if inferred_project_id != packet.get("project_id"):
        print("quote_response project_id inference does not match build packet")
        return 1

    packet_errors = validate_payload(packet, "build_packet.schema.json")
    response_errors = validate_payload(quote_response, "quote_response.schema.json")
    if packet_errors or response_errors:
        for item in packet_errors + response_errors:
            print(item)
        return 1

    payload = build_outcome_event(packet, quote_response)
    outcome_errors = validate_payload(payload, "outcome_event.schema.json")
    if outcome_errors:
        for item in outcome_errors:
            print(item)
        return 1

    output_path = OUTPUT_DIR / "outcome_event_latest.json"
    example_path = base_dir / "outcome_event_example.json"
    write_json(output_path, payload)
    write_json(example_path, payload)

    print(f"Wrote: {output_path}")
    print(f"Wrote: {example_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
