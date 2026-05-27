from __future__ import annotations

import json

import gradio as gr


FORBIDDEN_ACTIONS = [
    "send_email",
    "call_webhook",
    "contact_supplier",
    "route_quote",
    "approve_print",
    "approve_fabrication",
    "approve_payment",
    "approve_delivery",
    "certify_load_rating",
]


def preview_transaction(project_name: str, quantity: int, material: str, human_note: str):
    build_packet = {
        "project_id": "m2m-print-hook-001",
        "project_name": project_name,
        "quantity": quantity,
        "material": material,
        "sandbox_only": True,
        "human_approval_required": True,
    }
    human_approval_event = {
        "approval_event_id": "hae-m2m-print-hook-001",
        "decision": "approved_for_internal_review_only",
        "note": human_note,
        "not_approved_actions": [
            "external quote routing",
            "real shop contact",
            "fabrication",
            "payment",
            "delivery",
        ],
    }
    machine_response = {
        "response_type": "human_approval_required",
        "status": "BLOCKED",
        "external_action_taken": False,
        "message": "External release remains blocked in the sandbox.",
        "forbidden_actions": FORBIDDEN_ACTIONS,
    }
    summary = {
        "artifact_family": "Machine-to-Machine Print Transaction Sandbox",
        "local_only": True,
        "fake_shops_only": True,
        "next_safe_actions": [
            "review local artifacts",
            "inspect comparison summary",
            "propose next action under human review",
        ],
    }
    return (
        json.dumps(build_packet, indent=2),
        json.dumps(human_approval_event, indent=2),
        json.dumps(machine_response, indent=2),
        json.dumps(summary, indent=2),
    )


with gr.Blocks(title="Aether M2M Print Transaction Sandbox") as demo:
    gr.Markdown(
        "# Aether Build Protocol Sandbox\n"
        "Preview only. This draft Space demonstrates local artifacts and never contacts a real shop."
    )
    with gr.Row():
        project_name = gr.Textbox(value="Wall-Mounted 3D Printed Cable Hook", label="Project Name")
        material = gr.Textbox(value="PETG", label="Preferred Material")
    with gr.Row():
        quantity = gr.Number(value=12, precision=0, label="Quantity")
        human_note = gr.Textbox(
            value="Internal review only. No external release approved.",
            label="Human Review Note",
        )
    run_button = gr.Button("Generate Preview")
    build_packet_output = gr.Code(label="Build Packet Preview", language="json")
    approval_output = gr.Code(label="Human Approval Event Preview", language="json")
    machine_response_output = gr.Code(label="Machine Response Preview", language="json")
    summary_output = gr.Code(label="Sandbox Summary", language="json")

    run_button.click(
        preview_transaction,
        inputs=[project_name, quantity, material, human_note],
        outputs=[
            build_packet_output,
            approval_output,
            machine_response_output,
            summary_output,
        ],
    )


if __name__ == "__main__":
    demo.launch()