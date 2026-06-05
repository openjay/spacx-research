# Brand usage policy

**Applies to:** SPACX maintainers, contributors, agents, and fork operators.  
**Not legal advice.** See [TRADEMARK_BRAND_AUDIT.md](./TRADEMARK_BRAND_AUDIT.md) for risk analysis.

**Related:** [DATA_PROVENANCE.md](./DATA_PROVENANCE.md) · [COMPLIANCE.md](./COMPLIANCE.md) · [LISTING_STATUS.md](./LISTING_STATUS.md)

---

## Purpose

SPACX references third-party trademarks and entity names **only** to describe securities research subjects and cite sources. This policy separates **allowed nominative use** from **forbidden affiliation marketing**.

---

## Allowed uses

### SEC filing quotes and derived tables

- **Space Exploration Technologies Corp.** and shorthand **SpaceX** when quoting or summarizing EDGAR filings, with form, date, and accession citation.
- Segment and product names disclosed in filings: **Starlink**, **Starship**, **Colossus** (in filing context), **xAI** (post-merger segment).
- Counterparty names from filings: **Anthropic**, **Anthropic PBC**, etc.
- **Elon Musk** in governance, voting control, or risk-factor context from primary documents.
- **Nasdaq** when reproducing S-1/A language (e.g., anticipated listing venue) — text only, no logo.
- **Proposed / expected listing symbol SPCX** — never “listed ticker” until [LISTING_STATUS.md](./LISTING_STATUS.md) is updated for 424B4 and first trade.

### Third-party research (Grade C)

- **Goldman Sachs**, **Morningstar**, **New Constructs**, **Reuters**, **FT** — name the provider, link or cite the intermediary article, label as third-party / Grade C. Example:

  > Morningstar (via Reuters), Grade C — not independently verified by SPACX.

### Project naming

- **SPACX** as research platform codename and **spacx** as repository name, with disclaimer (below).
- Internal agent names mirroring filing segments (`StarlinkAnalystAgent`) in code and docs.

---

## Forbidden uses

### Marketing and positioning

- SpaceX, Starlink, xAI, Anthropic, Nasdaq, Goldman Sachs, Morningstar, or SEC **logos**, icons, or color trade dress.
- Words implying endorsement: **official**, **authorized**, **partner**, **sponsored by**, **endorsed by**, **affiliated with SpaceX**.
- Consumer-facing product names that could be confused with issuer brands (e.g., “Starlink Research Pro by SPACX” as a commercial SKU).
- **Domain squatting** patterns: `spacex-*`, `spcx-official.*`, `starlink-tracker.*` implying issuer operation.

### Ticker and listing misrepresentation

- Calling SPCX a **listed**, **trading**, or **publicly traded** ticker before 424B4 and first trade confirmation.
- GitHub badges styled as exchange or issuer securities branding.

### SEC extracts

- **Do not strip** issuer or entity names from filing copies to avoid trademark exposure — use citation and disclaimer instead ([DATA_PROVENANCE.md](./DATA_PROVENANCE.md)).

---

## Required disclaimer (copy-paste)

Use in README, manifest, agent READMEs, and any public export:

```text
Not affiliated with Space Exploration Technologies Corp. (SpaceX), xAI, Anthropic,
Nasdaq, Goldman Sachs, Morningstar, or the SEC. Research and education only.
Not investment advice.
```

中文（可选并列）:

```text
与 Space Exploration Technologies Corp.（SpaceX）、xAI、Anthropic、Nasdaq、
Goldman Sachs、Morningstar 及 SEC 均无关联。仅供研究学习，不构成投资建议。
```

---

## GitHub public repository description (template)

Use when flipping visibility to public:

```text
Open research platform for SEC-filing evidence on proposed symbol SPCX (Space
Exploration Technologies Corp.; pre-listing). Not affiliated with SpaceX or the SEC.
MIT · research/education only · not investment advice.
```

**Avoid:**

```text
Official SpaceX IPO tracker · SPCX stock research · Nasdaq partner tools
```

### Topics (allowed vs avoid)

| Allowed | Avoid |
|---------|-------|
| `sec`, `edgar`, `research`, `python`, `financial-analysis` | `spacex-official`, `spcx-stock`, `starlink` (as sole topic) |

---

## Badges and derivatives / forks

### Badges

- **Allowed:** CI status, license (MIT), Python version, generic “research” labels you own.
- **Forbidden:** Badges that incorporate SpaceX, Nasdaq, or exchange logos; “verified by SpaceX” style shields.

### Forks

Fork operators **must**:

1. Change the GitHub description to state they are an **independent fork**, not SpaceX or SPACX maintainer team.
2. Retain or strengthen the [Required disclaimer](#required-disclaimer-copy-paste).
3. Not use `spacx` or `SPACX` in a **commercial product name** without separate counsel review.
4. Not add issuer logos or “official” branding.

Suggested fork description prefix:

```text
[FORK — unofficial] Independent fork of spacx research tooling. Not affiliated with SpaceX.
```

---

## Agent and plugin naming

| Element | Rule |
|---------|------|
| `plugin/manifest.yaml` `disclaimer` | Must include full issuer legal name + not affiliated |
| Agent READMEs | One-line disclaimer footer linking here |
| Published reports | Footer with disclaimer + [COMPLIANCE.md](./COMPLIANCE.md) level |

---

## Enforcement (project)

- CI terminology tests: [tests/test_terminology.py](../tests/test_terminology.py)
- Listing language: [scripts/check_sec_feed_sync.py](../scripts/check_sec_feed_sync.py)
- Violations in PRs: request disclaimer fix or rename; escalate P0 to maintainer

---

## Revision history

| Date | Change |
|------|--------|
| 2026-06-05 | Initial policy aligned with TRADEMARK_BRAND_AUDIT |
