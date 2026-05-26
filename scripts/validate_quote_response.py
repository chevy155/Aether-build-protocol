from __future__ import annotations

import sys
from pathlib import Path

from protocol_utils import EXAMPLE_DIR, OUTPUT_DIR, build_quote_response_validation_report, load_json, validate_payload, write_text


def main() -> int:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else EXAMPLE_DIR / "quote_response_example.json"
    quote_response = load_json(input_path)
    errors = validate_payload(quote_response, "quote_response.schema.json")
    report = build_quote_response_validation_report(quote_response, errors)

    output_path = OUTPUT_DIR / "quote_response_validation_report_latest.md"
    example_path = EXAMPLE_DIR / "quote_response_validation_report.md"
    write_text(output_path, report)
    write_text(example_path, report)

    print(f"Validation result: {'PASS' if not errors else 'FAIL'}")
    print(f"Wrote: {output_path}")
    print(f"Wrote: {example_path}")
    return 0 if "**Result:** PASS" in report else 1


if __name__ == "__main__":
    raise SystemExit(main())
