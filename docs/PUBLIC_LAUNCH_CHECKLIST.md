# Public launch checklist

**Purpose:** P0/P1/P2 gates before `git remote` visibility flips to **public** or a broad distribution tag (`v0.1.0`) ships.  
**Not legal advice.** This is an engineering and operations gate; counsel sign-off is P0.

**Related:** [`OPEN_SOURCE_READINESS.md`](./OPEN_SOURCE_READINESS.md) · [`SBOM_POLICY.md`](./SBOM_POLICY.md) · [`GITHUB.md`](../GITHUB.md)

---

## Priority tiers

| Tier | Owner | Meaning |
|------|-------|---------|
| **P0** | Human maintainer (+ counsel where noted) | Block public mirror until complete |
| **P1** | Maintainer or agent when CI green | Required for **release-grade** tag; may ship repo public with documented gaps |
| **P2** | Post-launch hygiene | Improves enterprise trust; not a visibility blocker |

---

## P0 — before `git remote` goes public

| # | Item | Status | Evidence / action |
|---|------|--------|-------------------|
| P0-1 | **Legal / trademark counsel sign-off** | ⏳ Pending | Engineering audit complete — [`TRADEMARK_BRAND_AUDIT.md`](./TRADEMARK_BRAND_AUDIT.md), [`BRAND_USAGE_POLICY.md`](./BRAND_USAGE_POLICY.md), [`TERMINOLOGY.md`](./TERMINOLOGY.md). Counsel must sign off README, workstream naming, and issuer references before public flip. |
| P0-2 | **Secret scan green on `main`** | ✅ Infra | [`gitleaks`](../.gitleaks.toml) in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) — fails on `main`/`master` push |
| P0-3 | **No committed secrets** | ⏳ Verify | Rotate any keys ever committed; confirm `SPACX_SEC_USER_AGENT` stays in GitHub Secrets only |
| P0-4 | **Compliance level / CFA distribution gates** | ⏳ Human | Default deployment **level 2–3** per [`COMPLIANCE.md`](./COMPLIANCE.md). No level ≥4 external distribution without compliance review. See [`CFA_RESEARCH_POLICY.md`](./CFA_RESEARCH_POLICY.md). |
| P0-5 | **Listing status language** | ✅ Done | [`LISTING_STATUS.md`](./LISTING_STATUS.md) — proposed symbol SPCX until 424B4 |
| P0-6 | **SECURITY.md triage path** | ✅ Done | Private disclosure before public issues |

---

## P1 — release-grade (tag + assets)

| # | Item | Status | Evidence / action |
|---|------|--------|-------------------|
| P1-1 | **SBOM artifact in releases** | ✅ Infra | CI `supply-chain` job → `sbom.json`; attach to GitHub Release. Policy: [`SBOM_POLICY.md`](./SBOM_POLICY.md) |
| P1-2 | **`requirements-lock.txt` snapshot** | ✅ Infra | CI `pip freeze` artifact; optional weekly PR commit (documented in SBOM policy) |
| P1-3 | **Signed tags policy** | ✅ Policy | Maintainer creates annotated **signed** tags: `git tag -s v0.1.0 -m "..."` with GPG key on GitHub profile. Verify: `git tag -v v0.1.0` |
| P1-4 | **Release checksum manifest** | ⏳ Manual | On tag, publish `SHA256SUMS` for `sbom.json`, `requirements-lock.txt`, and source tarball |
| P1-5 | **Remove private-only assumptions in GITHUB.md** | ✅ Infra | [`GITHUB.md`](../GITHUB.md) updated for public-clone readiness; visibility flip is separate P0 maintainer action |
| P1-6 | **OPEN_SOURCE_READINESS ≥ 15/21** | ⏳ Track | [`OPEN_SOURCE_READINESS.md`](./OPEN_SOURCE_READINESS.md) |

---

## P2 — post-public hygiene

| # | Item | Status | Notes |
|---|------|--------|-------|
| P2-1 | **Dependabot / Renovate** | ⏳ Optional | Automated dependency PRs |
| P2-2 | **GitHub secret scanning (org)** | ⏳ Optional | Enable GitHub Advanced Security if org tier allows |
| P2-3 | **SPDX 2.3 standalone export** | ⏳ Optional | CycloneDX sufficient for most; see SBOM policy |
| P2-4 | **Release automation workflow** | ⏳ Optional | Attach SBOM + checksums on `release` event |

---

## Signed tags and checksums (maintainer runbook)

```bash
# 1. Ensure main is green (CI + gitleaks)
git checkout main && git pull

# 2. Export lock + SBOM locally (or download CI artifacts)
pip install -e ".[dev]"
pip freeze > requirements-lock.txt
pip install cyclonedx-bom
cyclonedx-py environment -o sbom.json --output-format json

# 3. Checksums
shasum -a 256 sbom.json requirements-lock.txt > SHA256SUMS

# 4. Signed tag
git tag -s v0.1.0 -m "SPACX v0.1.0 — research scaffold"
git push origin v0.1.0

# 5. GitHub Release: attach sbom.json, requirements-lock.txt, SHA256SUMS
```

---

## Trademark review

Counsel should review public-facing use of **SPACX**, **SPCX**, and references to **Space Exploration Technologies Corp. / SpaceX** (issuer, not affiliate).

- **When audit exists:** link from this section to [`TRADEMARK_BRAND_AUDIT.md`](./TRADEMARK_BRAND_AUDIT.md)
- **Until then:** treat P0-1 as open; do not imply endorsement by SpaceX or the SEC

---

## Agent / CI notes

| Automation | Behavior |
|------------|----------|
| **gitleaks** | Fails `main`/`master` push on leak; PRs warn via same job (non-blocking on PRs) |
| **SBOM + lockfile** | `supply-chain` job uploads artifacts every CI run |
| **Agents** | May commit P1 doc/regen work; **never** flip repo visibility or compliance level without human P0 |
