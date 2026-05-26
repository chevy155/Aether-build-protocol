from __future__ import annotations

import sys
from pathlib import Path

from protocol_utils import EXAMPLE_DIR, OUTPUT_DIR, load_json, write_text


def render_rfq(quote_request: dict) -> str:
    lines = [
        "# Request For Quote",
        "",
        "This document is for review and quoting only.",
        "",
        "It does not imply contractor approval, engineering approval, permit approval, guaranteed pricing, or authorization to begin work.",
        "",
        f"**Quote Request ID:** {quote_request['quote_request_id']}  ",
        f"**Project ID:** {quote_request['project_id']}",
        "",
        "## Scope Summary",
        "",
        quote_request["scope_summary"],
        "",
        "## Requested Quote Categories",
        "",
    ]
    lines.extend(f"- {item}" for item in quote_request["requested_quote_categories"])
    lines.extend(["", "## Required Capabilities", ""])
    lines.extend(f"- {item}" for item in quote_request["required_capabilities"])
    lines.extend(["", "## Assumptions To Confirm", ""])
    lines.extend(f"- {item}" for item in quote_request["assumptions_to_confirm"])
    lines.extend(["", "## Exclusions To State", ""])
    lines.extend(f"- {item}" for item in quote_request["exclusions_to_state"])
    lines.extend(["", "## Risk Questions", ""])
    lines.extend(f"- {item}" for item in quote_request["risk_questions"])
    lines.extend(["", "## Human Approval Gate", "", f"- Human approval required: {quote_request['human_approval_required']}"])
    return "\n".join(lines) + "\n"


def main() -> int:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else EXAMPLE_DIR / "quote_request.json"
    quote_request = load_json(input_path)
    rfq = render_rfq(quote_request)

    output_path = OUTPUT_DIR / "rfq_latest.md"
    example_path = EXAMPLE_DIR / "RFQ.md"
    write_text(output_path, rfq)
    write_text(example_path, rfq)

    print(f"Wrote: {output_path}")
    print(f"Wrote: {example_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
