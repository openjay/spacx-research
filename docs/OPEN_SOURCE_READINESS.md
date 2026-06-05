# Open source readiness checklist

**Target:** release-grade compliance for public mirror of SPACX-Research (AI-native P1).  
**Not legal advice.** Use this as an engineering gate before flipping repository visibility or tagging `v0.1.0`.

**Launch gate:** [`PUBLIC_LAUNCH_CHECKLIST.md`](./PUBLIC_LAUNCH_CHECKLIST.md)

---

## Verdict

**Basic open-source hygiene:** pass.
**Release-grade public launch:** infrastructure in place; P0 legal/trademark and first signed release remain before broad distribution.

## Checklist

| # | Item | Status | Evidence / notes |
|---|------|--------|------------------|
| 1 | **LICENSE** (MIT) | ✅ Done | [`LICENSE`](../LICENSE) |
| 2 | **NOTICE** (copyright) | ✅ Done | [`NOTICE`](../NOTICE) |
| 3 | **THIRD_PARTY_NOTICES** (direct deps) | ✅ Done | [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) — PyYAML, jsonschema, pytest |
| 4 | **Dependency license inventory** | ✅ Done | [`docs/DEPENDENCY_LICENSES.md`](./DEPENDENCY_LICENSES.md); CI optional drift warning in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| 5 | **CONTRIBUTING** | ✅ Done | [`CONTRIBUTING.md`](../CONTRIBUTING.md) — includes AI-native workflow |
| 6 | **SECURITY** policy | ✅ Done | [`SECURITY.md`](../SECURITY.md) |
| 7 | **Code of Conduct** | ✅ Done | [`CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) |
| 8 | **CI** (tests + compile) | ✅ Done | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) — test, compile, supply-chain |
| 9 | **Terminology / translation guard** | ✅ Done | [`docs/TERMINOLOGY.md`](./TERMINOLOGY.md) + `tests/test_terminology.py`; blocks literal `greenshoe` mistranslations |
| 10 | **Secret scan** | ✅ Done | [`gitleaks`](../.gitleaks.toml) in CI — blocks `main`/`master` push; PRs non-blocking |
| 11 | **SEC cache / DATA_PROVENANCE** | ✅ Done | [`docs/DATA_PROVENANCE.md`](./DATA_PROVENANCE.md) — redistribution rules, SHA-256 |
| 12 | **Research / compliance disclaimers** | ✅ Done | [`docs/COMPLIANCE.md`](./COMPLIANCE.md), [`docs/CFA_RESEARCH_POLICY.md`](./CFA_RESEARCH_POLICY.md) |
| 13 | **Listing status guardrails** | ✅ Done | [`docs/LISTING_STATUS.md`](./LISTING_STATUS.md) + `scripts/check_sec_feed_sync.py`; pre-listing language and live-feed drift gate |
| 14 | **pyproject license metadata** | ✅ Done | [`pyproject.toml`](../pyproject.toml) `license = { file = "LICENSE" }` |
| 15 | **Public remote / access** | ⚠️ Gap | Repo currently private — see [`GITHUB.md`](../GITHUB.md); flip after P0 in launch checklist |
| 16 | **Signed releases / tags** | ⏳ Policy | Runbook in [`PUBLIC_LAUNCH_CHECKLIST.md`](./PUBLIC_LAUNCH_CHECKLIST.md); no `v0.1.0` tag yet |
| 17 | **Dependency pinning / SPDX SBOM** | ✅ Done | CI `supply-chain` job → `requirements-lock.txt` + `sbom.json`; [`SBOM_POLICY.md`](./SBOM_POLICY.md) |
| 18 | **Trademark / brand audit (engineering)** | ✅ Done | [`TRADEMARK_BRAND_AUDIT.md`](./TRADEMARK_BRAND_AUDIT.md), [`BRAND_USAGE_POLICY.md`](./BRAND_USAGE_POLICY.md); README + manifest disclaimers strengthened |
| 19 | **Public launch checklist** | ✅ Done | [`PUBLIC_LAUNCH_CHECKLIST.md`](./PUBLIC_LAUNCH_CHECKLIST.md) — P0/P1/P2 gates |
| 20 | **Gitleaks allowlist config** | ✅ Done | [`.gitleaks.toml`](../.gitleaks.toml) — SEC cache paths |
| 21 | **SBOM policy doc** | ✅ Done | [`SBOM_POLICY.md`](./SBOM_POLICY.md) |
| 22 | **Trademark counsel sign-off (P0)** | ⚠️ Gap | Checklist in [`TRADEMARK_BRAND_AUDIT.md`](./TRADEMARK_BRAND_AUDIT.md) § Public launch blockers — record approval date here |

**Score:** **18 / 22** complete. Engineering trademark hygiene is in place; **P0 counsel sign-off**, repo visibility, and first signed release remain before broad public distribution.

---

## P0 vs P1 gates (AI-native)

| Tier | Who gates | Examples |
|------|-----------|----------|
| **P0 — human** | Maintainer | 424B4 / listing status, compliance level changes, external publish, SECURITY triage, repo visibility, trademark counsel |
| **P1 — agent** | Cursor / CI agents | THIRD_PARTY_NOTICES, DEPENDENCY_LICENSES regen, tests, registry YAML, evidence drafts, SBOM/lock artifacts |

Agents may commit P1 work when CI is green. P0 items require explicit human approval per [`docs/AGENTS.md`](./AGENTS.md).

---

## Current gaps (action items)

1. **Trademark counsel sign-off (P0-1)** — engineering audit complete in [`TRADEMARK_BRAND_AUDIT.md`](./TRADEMARK_BRAND_AUDIT.md); record counsel approval date in [PUBLIC_LAUNCH_CHECKLIST P0-1](./PUBLIC_LAUNCH_CHECKLIST.md#p0--before-git-remote-goes-public) before public flip.
2. **Tag `v0.1.0`** — signed tag + release assets (`sbom.json`, `requirements-lock.txt`, `SHA256SUMS`) per launch checklist.
3. **Flip visibility** — when P0 complete in [`PUBLIC_LAUNCH_CHECKLIST.md`](./PUBLIC_LAUNCH_CHECKLIST.md).

---

## Verification commands

```bash
# Tests (required)
pip install -e ".[dev]"
pytest --tb=short -q

# Dependency license report (optional)
pip install pip-licenses
pip-licenses --format=markdown --with-urls > docs/DEPENDENCY_LICENSES.md

# SBOM + lock snapshot (optional — mirrors CI supply-chain job)
pip freeze > requirements-lock.txt
pip install cyclonedx-bom
cyclonedx-py environment -o sbom.json --output-format json

# SEC cache integrity (sample)
shasum -a 256 workstreams/sec-evidence-phase1/s1a2-main.htm
```
