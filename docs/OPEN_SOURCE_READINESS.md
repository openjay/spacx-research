# Open source readiness checklist

**Target:** release-grade compliance for public mirror of SPACX (AI-native P1).  
**Not legal advice.** Use this as an engineering gate before flipping repository visibility or tagging `v0.1.0`.

---

## Checklist

| # | Item | Status | Evidence / notes |
|---|------|--------|------------------|
| 1 | **LICENSE** (MIT) | ✅ Done | [`LICENSE`](../LICENSE) |
| 2 | **NOTICE** (copyright) | ✅ Done | [`NOTICE`](../NOTICE) |
| 3 | **THIRD_PARTY_NOTICES** (direct deps) | ✅ Done | [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) — PyYAML, jsonschema, pytest |
| 4 | **SBOM / dependency licenses** | ✅ Done | [`docs/DEPENDENCY_LICENSES.md`](./DEPENDENCY_LICENSES.md); CI optional regen in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| 5 | **CONTRIBUTING** | ✅ Done | [`CONTRIBUTING.md`](../CONTRIBUTING.md) — includes AI-native workflow |
| 6 | **SECURITY** policy | ✅ Done | [`SECURITY.md`](../SECURITY.md) |
| 7 | **Code of Conduct** | ✅ Done | [`CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) |
| 8 | **CI** (tests + compile) | ✅ Done | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| 9 | **Secret scan** | ⏳ Placeholder | Commented `gitleaks` step in CI — enable before public launch |
| 10 | **SEC cache / DATA_PROVENANCE** | ✅ Done | [`docs/DATA_PROVENANCE.md`](./DATA_PROVENANCE.md) — redistribution rules, SHA-256 |
| 11 | **Research / compliance disclaimers** | ✅ Done | [`docs/COMPLIANCE.md`](./COMPLIANCE.md), [`docs/CFA_RESEARCH_POLICY.md`](./CFA_RESEARCH_POLICY.md) |
| 12 | **Listing status guardrails** | ✅ Done | [`docs/LISTING_STATUS.md`](./LISTING_STATUS.md) — pre-listing language |
| 13 | **pyproject license metadata** | ✅ Done | [`pyproject.toml`](../pyproject.toml) `license = { file = "LICENSE" }` |
| 14 | **Public remote / access** | ⚠️ Gap | Repo currently private — see [`GITHUB.md`](../GITHUB.md) |
| 15 | **Signed releases / tags** | ⚠️ Gap | No tagged release or checksum manifest yet |
| 16 | **Dependency pinning / lockfile** | ⚠️ Gap | Minimum versions only; no `requirements.lock` or SBOM SPDX export |
| 17 | **Trademark / issuer naming review** | ⚠️ Gap | Counsel review before broad distribution (SpaceX ecosystem naming) |

**Score:** **11 / 17** complete (4 partial/placeholder, 3 open gaps).

---

## P0 vs P1 gates (AI-native)

| Tier | Who gates | Examples |
|------|-----------|----------|
| **P0 — human** | Maintainer | 424B4 / listing status, compliance level changes, external publish, SECURITY triage |
| **P1 — agent** | Cursor / CI agents | THIRD_PARTY_NOTICES, DEPENDENCY_LICENSES regen, tests, registry YAML, evidence drafts |

Agents may commit P1 work when CI is green. P0 items require explicit human approval per [`docs/AGENTS.md`](./AGENTS.md).

---

## Current gaps (action items)

1. **Enable secret scanning** — uncomment or add `gitleaks` / `trufflehog` in CI before public mirror.
2. **Tag `v0.1.0`** — attach release notes linking this checklist and `THIRD_PARTY_NOTICES.md`.
3. **Lockfile or SPDX SBOM** — consider `pip-tools` lock or CycloneDX export for enterprise consumers.
4. **Legal / trademark pass** — confirm README and workstream naming for public redistribution.
5. **Flip visibility** — when checklist ≥ 14/17 and P0 maintainer sign-off.

---

## Verification commands

```bash
# Tests (required)
pip install jsonschema pyyaml pytest
pytest --tb=short -q

# Dependency license report (optional)
pip install pip-licenses
pip-licenses --format=markdown --with-urls > docs/DEPENDENCY_LICENSES.md

# SEC cache integrity (sample)
shasum -a 256 workstreams/sec-evidence-phase1/s1a2-main.htm
```
