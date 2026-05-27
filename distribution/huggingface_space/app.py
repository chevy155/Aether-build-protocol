from __future__ import annotations

import hashlib

import gradio as gr


FORBIDDEN_ACTIONS = [
    "send_email",
    "call_webhook",
    "contact_shop",
    "route_quote",
    "approve_print",
    "approve_fabrication",
    "approve_engineering",
    "approve_payment",
    "certify_load_rating",
]


def _stable_id(*parts: str) -> str:
    joined = "|".join(parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]


def build_previews(
    part_name: str,
    material: str,
    process: str,
    quantity: float,
    tolerance: str,
    finish: str,
    unknowns: str,
):
    quantity_int = max(1, int(quantity))
    part_ref = _stable_id(part_name, material, process, tolerance, finish, unknowns)
    unknown_items = [item.strip() for item in unknowns.splitlines() if item.strip()]

    build_packet = {
        "build_packet_id": f"bp-{part_ref}",
        "artifact_type": "build_packet_preview",
        "part_name": part_name,
        "material": material,
        "process": process,
        "quantity": quantity_int,
        "tolerance": tolerance,
        "finish": finish,
        "unknowns": unknown_items,
        "sandbox_only": True,
        "external_action_taken": False,
        "human_review_required": True,
    }

    quote_request = {
        "quote_request_id": f"rfq-{part_ref}",
        "artifact_type": "quote_request_preview",
        "source_build_packet_id": build_packet["build_packet_id"],
        "scope": "internal_preview_only",
        "requested_process": process,
        "requested_material": material,
        "requested_quantity": quantity_int,
        "requested_tolerance": tolerance,
        "requested_finish": finish,
        "open_questions": unknown_items,
        "external_action_taken": False,
        "human_review_required": True,
    }

    approval_response = {
        "response_type": "human_approval_required",
        "decision": "blocked_for_external_release",
        "reason": "Sandbox preview only. Human approval required before any quote routing or fabrication action.",
        "external_action_taken": False,
        "human_review_required": True,
        "not_approved_actions": FORBIDDEN_ACTIONS,
    }

    machine_response = {
        "envelope_type": "machine_response_envelope",
        "status": "BLOCKED",
        "external_action_taken": False,
        "human_review_required": True,
        "summary": "Local deterministic preview generated. No real shop contact or manufacturing action occurred.",
        "forbidden_actions": FORBIDDEN_ACTIONS,
    }

    forbidden_actions = {
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "sandbox_guards": {
            "no_real_shop_contact": True,
            "no_real_quote_routing": True,
            "no_print_approval": True,
            "no_fabrication_approval": True,
            "no_engineering_approval": True,
            "no_payment_approval": True,
            "no_load_certification": True,
        },
    }

    return build_packet, quote_request, approval_response, machine_response, forbidden_actions


with gr.Blocks(title="Aether CAD-to-Agent Sandbox") as demo:
    gr.Markdown(
        "# Aether CAD-to-Agent Sandbox\n\n"
        "Preview only. This demo is local-only and sandbox-only. It makes no network calls, does not contact shops, does not route quotes, does not approve printing, fabrication, engineering, or payment, and does not certify load rating."
    )

    with gr.Row():
        part_name = gr.Textbox(label="Part Name", value="Wall-Mounted Cable Hook")
        material = gr.Textbox(label="Material", value="PETG")
        process = gr.Dropdown(
            label="Process",
            choices=["FDM 3D Printing", "SLA 3D Printing", "CNC Milling", "Waterjet Cutting"],
            value="FDM 3D Printing",
        )

    with gr.Row():
        quantity = gr.Number(label="Quantity", value=12, precision=0)
        tolerance = gr.Textbox(label="Tolerance", value="+/- 0.25 mm")
        finish = gr.Textbox(label="Finish", value="Deburr and light bead blast")

    unknowns = gr.Textbox(
        label="Unknowns",
        lines=4,
        value="Confirm load case assumptions\nConfirm preferred color\nConfirm packaging constraints",
    )

    run_button = gr.Button("Generate Sandbox Preview")

    build_packet_output = gr.JSON(label="Build Packet Preview")
    quote_request_output = gr.JSON(label="Quote Request Preview")
    approval_output = gr.JSON(label="Human Approval Required Response")
    machine_response_output = gr.JSON(label="Machine Response Envelope")
    forbidden_actions_output = gr.JSON(label="Forbidden Actions List")

    run_button.click(
        build_previews,
        inputs=[part_name, material, process, quantity, tolerance, finish, unknowns],
        outputs=[
            build_packet_output,
            quote_request_output,
            approval_output,
            machine_response_output,
            forbidden_actions_output,
        ],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)