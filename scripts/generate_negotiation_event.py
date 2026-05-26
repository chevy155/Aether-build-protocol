from __future__ import annotations

import sys
from pathlib import Path

from protocol_utils import EXAMPLE_DIR, OUTPUT_DIR, build_negotiation_event, load_json, validate_payload, write_json


def main() -> int:
    base_dir = EXAMPLE_DIR
    quote_request_path = Path(sys.argv[1]) if len(sys.argv) > 1 else base_dir / "quote_request.json"
    quote_response_path = Path(sys.argv[2]) if len(sys.argv) > 2 else base_dir / "quote_response_example.json"

    quote_request = load_json(quote_request_path)
    quote_response = load_json(quote_response_path)
    response_errors = validate_payload(quote_response, "quote_response.schema.json")
    if response_errors:
        for item in response_errors:
            print(item)
        return 1

    payload = build_negotiation_event(quote_request, quote_response)
    event_errors = validate_payload(payload, "negotiation_event.schema.json")
    if event_errors:
        for item in event_errors:
            print(item)
        return 1

    output_path = OUTPUT_DIR / "negotiation_event_latest.json"
    example_path = base_dir / "negotiation_event_example.json"
    write_json(output_path, payload)
    write_json(example_path, payload)

    print(f"Wrote: {output_path}")
    print(f"Wrote: {example_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
