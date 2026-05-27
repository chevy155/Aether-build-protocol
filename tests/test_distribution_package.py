from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISTRIBUTION_ROOT = ROOT / "distribution"


def test_distribution_package_is_complete_and_manual_only() -> None:
    required_files = [
        DISTRIBUTION_ROOT / "README.md",
        DISTRIBUTION_ROOT / "PUBLISHING_CHECKLIST.md",
        DISTRIBUTION_ROOT / "huggingface_space" / "app.py",
        DISTRIBUTION_ROOT / "huggingface_space" / "requirements.txt",
        DISTRIBUTION_ROOT / "huggingface_space" / "README.md",
        DISTRIBUTION_ROOT / "huggingface_dataset" / "README.md",
        DISTRIBUTION_ROOT / "huggingface_dataset" / "examples_index.json",
        DISTRIBUTION_ROOT / "huggingface_dataset" / "examples" / "build_packet.example.json",
        DISTRIBUTION_ROOT / "huggingface_dataset" / "examples" / "human_approval_event.example.json",
        DISTRIBUTION_ROOT / "huggingface_dataset" / "examples" / "machine_response_envelope.example.json",
        DISTRIBUTION_ROOT / "huggingface_dataset" / "examples" / "agent_readiness_report.example.json",
        DISTRIBUTION_ROOT / "huggingface_dataset" / "examples" / "m2m_print_transaction_summary.example.json",
        DISTRIBUTION_ROOT / "github_pages" / "index.md",
        DISTRIBUTION_ROOT / "github_pages" / "_config.yml",
        DISTRIBUTION_ROOT / "mcp_registry" / "README.md",
        DISTRIBUTION_ROOT / "mcp_registry" / "aether-build-protocol-draft-listing.json",
        DISTRIBUTION_ROOT / "posts" / "linkedin_draft.md",
        DISTRIBUTION_ROOT / "posts" / "hacker_news_draft.md",
        DISTRIBUTION_ROOT / "posts" / "devto_draft.md",
        DISTRIBUTION_ROOT / "posts" / "fabrication_forum_draft.md",
        DISTRIBUTION_ROOT / "posts" / "design_community_draft.md",
    ]
    for path in required_files:
        assert path.exists(), str(path)

    checklist = (DISTRIBUTION_ROOT / "PUBLISHING_CHECKLIST.md").read_text(encoding="utf-8")
    distribution_readme = (DISTRIBUTION_ROOT / "README.md").read_text(encoding="utf-8")
    space_app = (DISTRIBUTION_ROOT / "huggingface_space" / "app.py").read_text(encoding="utf-8")
    dataset_card = (DISTRIBUTION_ROOT / "huggingface_dataset" / "README.md").read_text(encoding="utf-8")
    github_page = (DISTRIBUTION_ROOT / "github_pages" / "index.md").read_text(encoding="utf-8")
    registry_listing = json.loads((DISTRIBUTION_ROOT / "mcp_registry" / "aether-build-protocol-draft-listing.json").read_text(encoding="utf-8"))
    examples_index = json.loads((DISTRIBUTION_ROOT / "huggingface_dataset" / "examples_index.json").read_text(encoding="utf-8"))

    assert "manual login required" in checklist.lower()
    assert "nothing in `distribution/` publishes automatically" in checklist.lower()
    assert "no auto-post script" in checklist.lower()
    assert "manual login required" in distribution_readme.lower()
    assert "import gradio as gr" in space_app
    assert "requests" not in space_app
    assert "httpx" not in space_app
    assert "no network calls" in (DISTRIBUTION_ROOT / "huggingface_space" / "README.md").read_text(encoding="utf-8").lower()
    assert "local-only sandbox" in dataset_card.lower()
    assert "human approval required" in dataset_card.lower()
    assert "not published automatically" in github_page.lower()
    assert registry_listing["status"] == "draft"
    assert registry_listing["hosted_server"] is False
    assert registry_listing["automatic_submission"] is False
    assert examples_index["status"] == "draft"
    assert examples_index["local_only"] is True

    example_packet = json.loads((DISTRIBUTION_ROOT / "huggingface_dataset" / "examples" / "build_packet.example.json").read_text(encoding="utf-8"))
    example_machine_response = json.loads((DISTRIBUTION_ROOT / "huggingface_dataset" / "examples" / "machine_response_envelope.example.json").read_text(encoding="utf-8"))
    example_summary = json.loads((DISTRIBUTION_ROOT / "huggingface_dataset" / "examples" / "m2m_print_transaction_summary.example.json").read_text(encoding="utf-8"))

    assert example_packet["sandbox_only"] is True
    assert example_packet["external_action_taken"] is False
    assert example_machine_response["external_action_taken"] is False
    assert example_summary["current_state"] == "CLOSED_LOCAL_ONLY"