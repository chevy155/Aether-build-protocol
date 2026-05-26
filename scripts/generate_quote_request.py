from __future__ import annotations

import sys
from pathlib import Path

from protocol_utils import EXAMPLE_DIR, OUTPUT_DIR, build_quote_request, load_yaml, validate_payload, write_json


def main() -> int:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else EXAMPLE_DIR / "build_packet.yaml"
    packet = load_yaml(input_path)
    errors = validate_payload(packet, "build_packet.schema.json")
    if errors:
        for item in errors:
            print(item)
        return 1

    quote_request = build_quote_request(packet)

    output_path = OUTPUT_DIR / "quote_request_latest.json"
    example_path = EXAMPLE_DIR / "quote_request.json"
    write_json(output_path, quote_request)
    write_json(example_path, quote_request)

    print(f"Wrote: {output_path}")
    print(f"Wrote: {example_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
