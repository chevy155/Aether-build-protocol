from __future__ import annotations

import sys
from pathlib import Path

from protocol_utils import (
    EXAMPLE_DIR,
    OUTPUT_DIR,
    load_yaml,
    render_build_packet_quote_readiness_report,
    score_build_packet_quote_readiness,
    validate_payload,
    write_json,
    write_text,
)


def main() -> int:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else EXAMPLE_DIR / "build_packet.yaml"
    packet = load_yaml(input_path)
    errors = validate_payload(packet, "build_packet.schema.json")
    result = score_build_packet_quote_readiness(packet, errors)
    report = render_build_packet_quote_readiness_report(packet, result)

    json_path = OUTPUT_DIR / "quote_readiness_score_latest.json"
    md_path = OUTPUT_DIR / "quote_readiness_score_latest.md"
    write_json(json_path, result)
    write_text(md_path, report)

    print(f"Score: {result['score']}")
    print(f"Status: {result['status']}")
    print(f"Wrote: {json_path}")
    print(f"Wrote: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())