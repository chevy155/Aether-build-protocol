# Hugging Face Deployment Closeout

- deployment timestamp: 2026-05-27T13:06:17-07:00
- namespace: lonestar155
- dataset repo: lonestar155/aether-build-protocol-examples
- space repo: lonestar155/aether-cad-to-agent-sandbox
- source folders uploaded:
  - distribution/huggingface_dataset
  - distribution/huggingface_space
- commands used:
  - hf auth whoami
  - python fallback via huggingface_hub.HfApi.create_repo(..., exist_ok=True)
  - python fallback via huggingface_hub.HfApi.upload_folder(...)
  - python -m pytest tests/ -v
- public URLs:
  - https://huggingface.co/datasets/lonestar155/aether-build-protocol-examples
  - https://huggingface.co/spaces/lonestar155/aether-cad-to-agent-sandbox
- guardrails verified:
  - sandbox only
  - local-only or local-first wording present
  - no real shop contacted
  - no quote routed
  - no print approved
  - no fabrication approval
  - no engineering approval
  - no payment approval
  - no load certification
  - human approval required
- no token stored in repo
- no secrets committed
- no external manufacturing action
- manual checks remaining:
  - Dataset README renders
  - Dataset examples visible
  - Sandbox warnings visible
  - No secrets uploaded
- known limitations:
  - Hugging Face Space is a demo only
  - no real shop contact
  - no real quote routing
  - no fabrication approval
  - no engineering approval
  - no payment approval
  - no load certification

## Metadata + Space Config Repair

- dataset README metadata patched: complete
- space README config patched: complete
- space app reviewed: gradio import present, launch block present, no secrets required, no external API calls, sandbox warnings present
- re-upload timestamp: 2026-05-27T13:10:59.8291433-07:00
- guardrails verified:
  - no real shop contact
  - no quote routing
  - no print approval
  - no fabrication approval
  - no engineering approval
  - no payment approval
  - no load certification
  - no external manufacturing action
- manual checks remaining:
  - Dataset metadata warning cleared
  - Dataset README renders
  - Dataset examples visible
  - Space config error cleared
  - Space build completes
  - Space app launches
  - Sandbox warnings visible

## Space Runtime Repair

- dataset status: PASS
- space runtime fix applied: python pinned to 3.12 in Space README YAML
- space requirements minimal: gradio==5.47.2 only
- space status: pending manual rebuild verification
- space re-upload timestamp: 2026-05-27T13:17:18.0091314-07:00
- public Space page status after latest compatibility repair: Building...
- new runtime error observed after Python fix: gradio 5.0.0 imports HfFolder, which is missing from the current huggingface_hub runtime
- compatibility repair applied: pinned Space SDK and requirements to gradio 5.47.2, which includes huggingface_hub 1.x compatibility

## Space Runtime Repair Follow-Up

- local smoke test package reduced to:
  - gradio==4.44.1
  - huggingface_hub==0.33.4
- local validation completed:
  - python -m pip install -r distribution/huggingface_space/requirements.txt
  - python -m py_compile distribution/huggingface_space/app.py
  - python -c "import gradio, huggingface_hub; from huggingface_hub import HfFolder"
  - python distribution/huggingface_space/app.py
- local launch result: PASS
- local Gradio URL observed: http://127.0.0.1:7860
- remote repo verification: PASS
- remote README.md verification: sdk_version 4.44.1, python_version 3.12, app_file app.py
- remote requirements.txt verification: gradio==4.44.1 and huggingface_hub==0.33.4
- remote app.py verification: latest self-contained deterministic sandbox app uploaded
- runtime error captured after first 4.44.1 deploy:
  - ImportError: cannot import name 'HfFolder' from 'huggingface_hub'
- root cause: Hugging Face runtime resolved an incompatible huggingface_hub version for Gradio 4.44.1
- corrective action: pinned huggingface_hub==0.33.4 in distribution/huggingface_space/requirements.txt
- space re-upload timestamp: 2026-05-27T13:22:17.0637310-07:00
- dependency-fix re-upload timestamp: 2026-05-27T13:24:20.7187332-07:00
- runtime restart issued after dependency fix: PASS
- current public runtime status: BUILDING
- public Space URL: https://huggingface.co/spaces/lonestar155/aether-cad-to-agent-sandbox
- direct Space URL: https://lonestar155-aether-cad-to-agent-sandbox.hf.space/
- repo regression status: PASS
- pytest result: 32 passed
- no secrets committed
- no external manufacturing action

## Space Launch Boundary Fix

- second runtime error captured after dependency repair:
  - ValueError: When localhost is not accessible, a shareable link must be created. Please set share=True or check your proxy settings to allow access to localhost.
- root cause: the Gradio app was launching on the default localhost bind instead of an externally reachable Space host boundary
- corrective action: changed the Space launch call to demo.launch(server_name="0.0.0.0", server_port=7860)
- local launch verification after host-binding fix: PASS
- local URL observed after host-binding fix: http://0.0.0.0:7860
- final launch-fix re-upload timestamp: 2026-05-27T13:26:46.3080314-07:00
- runtime restart issued after launch fix: PASS
- current public runtime status: BUILDING

## Space Web Stack Pin

- request-path failure observed after launch fix while the control plane alternated between RUNNING and HTTP 500 at the root endpoint
- leading symptom in captured remote trace: TypeError: unhashable type: 'dict' during gradio route template rendering
- local serving path validated with explicit root requests:
  - GET /
  - GET /?__theme=system
- corrective action: pinned fastapi==0.116.1 and starlette==0.47.1 alongside gradio==4.44.1 and huggingface_hub==0.33.4
- local dependency verification after web-stack pin: PASS
- web-stack pin re-upload timestamp: 2026-05-27T13:29:24.9883475-07:00
- runtime restart issued after web-stack pin: PASS
- current public runtime status: BUILDING

## Final Space Runtime Verification

- final public runtime status: RUNNING
- direct Space endpoint status: HTTP 200
- direct Space domain status: READY
- public Space build status: PASS
- public Space app launch status: PASS
- live UI verification: PASS
- live inputs observed:
  - Part Name
  - Material
  - Process
  - Quantity
  - Tolerance
  - Finish
  - Unknowns
- live outputs observed:
  - Build Packet Preview
  - Quote Request Preview
  - Human Approval Required Response
  - Machine Response Envelope
  - Forbidden Actions List
- guardrails still visible in the served app: PASS
- no secrets uploaded: no evidence observed