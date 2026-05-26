from __future__ import annotations

import sys
from pathlib import Path

from protocol_utils import EXAMPLE_DIR, OUTPUT_DIR, build_quote_comparison_summary, load_json, render_quote_comparison_summary, write_json, write_text


def main() -> int:
    input_paths = [Path(arg) for arg in sys.argv[1:]]
    if not input_paths:
        input_paths = [
            EXAMPLE_DIR / "quote_response_example.json",
            EXAMPLE_DIR / "quote_response_example_2.json",
            EXAMPLE_DIR / "quote_response_example_3.json",
        ]

    quote_responses = [load_json(path) for path in input_paths]
    summary = build_quote_comparison_summary(quote_responses)
    report = render_quote_comparison_summary(summary)

    json_path = OUTPUT_DIR / "quote_comparison_summary_latest.json"
    md_path = OUTPUT_DIR / "quote_comparison_summary_latest.md"
    example_json_path = EXAMPLE_DIR / "quote_comparison_summary.json"
    example_md_path = EXAMPLE_DIR / "quote_comparison_summary.md"

    write_json(json_path, summary)
    write_text(md_path, report)
    write_json(example_json_path, summary)
    write_text(example_md_path, report)

    print(f"Compared responses: {summary['response_count']}")
    print(f"Wrote: {json_path}")
    print(f"Wrote: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
