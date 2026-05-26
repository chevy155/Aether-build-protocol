# Public Release Checklist

## Repository Hygiene

- [x] `LICENSE` exists
- [x] `CONTRIBUTING.md` exists
- [x] `CODE_OF_CONDUCT.md` exists
- [x] `SECURITY.md` exists
- [x] `CHANGELOG.md` exists
- [x] `.gitignore` exists
- [x] lightweight `requirements.txt` exists

## Required Files

- [x] README clearly explains what the protocol is and is not
- [x] release notes exist
- [x] demo walkthrough exists
- [x] reviewer packet exists
- [x] feedback form exists
- [x] public positioning doc exists

## GitHub Actions

- [x] `.github/workflows/tests.yml` exists
- [x] workflow installs dependencies from `requirements.txt`
- [x] workflow runs `python -m pytest tests/ -v`
- [x] workflow YAML parses correctly

## README Commands

- [x] build packet validation command listed
- [x] quote request generation command listed
- [x] RFQ generation command listed
- [x] quote response validation command listed
- [x] quote-readiness scoring command listed
- [x] negotiation event generation command listed
- [x] outcome event generation command listed
- [x] quote comparison summary command listed
- [x] test command listed

## Local Proof Commands

- [x] all proof commands run from repo root
- [x] all outputs regenerate locally
- [x] no external communication is required

## Generated Artifacts

- [x] validation report generated
- [x] quote request generated
- [x] RFQ generated
- [x] agent manifest generated
- [x] quote response validation report generated
- [x] quote-readiness score JSON and markdown generated
- [x] negotiation event generated
- [x] outcome event generated
- [x] quote comparison summary JSON and markdown generated

## Tests

- [x] full suite passes locally

## Guardrail Language Audit

- [x] no repo copy implies marketplace launch
- [x] no repo copy implies contractor selection
- [x] no repo copy implies hiring approval
- [x] no repo copy implies build approval
- [x] no repo copy implies supplier routing or outreach
- [x] negative or test-only mentions of forbidden language are acceptable when used for guardrail enforcement

## Release Tag

Recommended tag:

`v0.2.1-local-quote-comparison`

Do not run unless explicitly instructed:

```powershell
git tag -a v0.2.1-local-quote-comparison -m "Aether Build Protocol v0.2.1 local quote comparison"
git push origin v0.2.1-local-quote-comparison
```

## Demo Readiness

- [x] demo walkthrough exists
- [x] demo stays focused on protocol movement, not product UI
- [x] demo closes with guardrails

## Controlled Alpha Readiness

- [x] reviewer packet exists
- [x] alpha feedback form exists
- [x] positioning and guardrails are consistent across release docs
