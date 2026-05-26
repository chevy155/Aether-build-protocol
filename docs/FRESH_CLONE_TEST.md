# Fresh Clone Test

## Goal

Confirm that a new reviewer can clone the repo, install lightweight dependencies, and run the local proof loop from the repo root.

## Steps

```powershell
git clone <repo-url>
cd Fractal_Infinity_Aether
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/validate_build_packet.py examples/sauna_node/build_packet.yaml
python scripts/generate_quote_request.py examples/sauna_node/build_packet.yaml
python scripts/generate_rfq_markdown.py examples/sauna_node/quote_request.json
python scripts/generate_agent_manifest.py examples/sauna_node/build_packet.yaml
python scripts/validate_quote_response.py examples/sauna_node/quote_response_example.json
python scripts/score_quote_readiness.py examples/sauna_node/build_packet.yaml
python scripts/generate_negotiation_event.py examples/sauna_node/quote_request.json examples/sauna_node/quote_response_example.json
python scripts/generate_outcome_event.py examples/sauna_node/quote_response_example.json
python scripts/generate_quote_comparison_summary.py examples/sauna_node/quote_response_example.json examples/sauna_node/quote_response_example_2.json examples/sauna_node/quote_response_example_3.json
python -m pytest tests/ -v
```

## Expected Outcome

All commands complete locally with no external calls and all tests pass.
