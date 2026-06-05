# Trademark & brand infringement audit

**Date:** 2026-06-05  
**Scope:** Pre-public OSS release review for repository `spacx` (GitHub: `openjay/spacx`)  
**Status:** Engineering checklist complete — **not legal advice**; consult qualified counsel before public launch.

**Related:** [BRAND_USAGE_POLICY.md](./BRAND_USAGE_POLICY.md) · [DATA_PROVENANCE.md](./DATA_PROVENANCE.md) · [COMPLIANCE.md](./COMPLIANCE.md) · [OPEN_SOURCE_READINESS.md](./OPEN_SOURCE_READINESS.md)

---

## Executive summary (EN)

SPACX is a **private research platform** tracking the proposed listing symbol **SPCX** for **Space Exploration Technologies Corp.** (SEC filings). The repository name `spacx`, project codename **SPACX**, and references to SpaceX, Starlink, xAI, Colossus, Anthropic, Nasdaq, Musk, Goldman Sachs, and Morningstar appear throughout evidence tables, agent names, and documentation.

**Default recommendation: KEEP `spacx` as a private-research codename with strengthened disclaimers.** Do **not** rename the git remote or GitHub repository without explicit maintainer sign-off and counsel review. A public launch is **not blocked** by the engineering audit alone, but **is blocked** until P0 counsel sign-off on trademark posture (see [Public launch blockers](#public-launch-blockers-counsel-checklist)).

| Risk area | Severity (public OSS) | Posture |
|-----------|----------------------|---------|
| Repo name `spacx` / codename SPACX | **Medium** | Keep with disclaimers; avoid marketing as “official” SpaceX tooling |
| Ticker reference `SPCX` | **Low–Medium** | Keep as *proposed / expected* symbol with [LISTING_STATUS.md](./LISTING_STATUS.md) guardrails |
| SpaceX / issuer legal name in SEC extracts | **Low** | **Keep** — nominative fair use for research citing primary filings |
| Starlink, Starship, Colossus (segment names) | **Low–Medium** | Keep when sourced from SEC; cite filing; no standalone logos |
| xAI, Anthropic (third-party entities in filings) | **Low** | Citation only; no implied partnership |
| Musk (person name in filing context) | **Low** | Factual reference in governance / risk disclosure; no endorsement framing |
| Nasdaq (exchange reference) | **Low** | Quote S-1/A language (“anticipated listing on Nasdaq”); no Nasdaq logo or “Nasdaq partner” |
| Goldman / Morningstar (research citations) | **Low** | Grade-C external context with source attribution; no logo or “endorsed by” |
| Agent names (`StarlinkAnalystAgent`, etc.) | **Medium** | Acceptable for internal research; add disclaimer footers; avoid consumer-facing product names mirroring trademarks |
| Domain / package `spacx-intelligence` | **Medium** | Monitor for confusion with SpaceX consumer brands; use descriptive OSS description |

**Nominative fair use (generally lower risk):** Quoting SEC filing language that names the issuer, segments, counterparties, exchanges, and proposed ticker — with accession citation and [DATA_PROVENANCE.md](./DATA_PROVENANCE.md) integrity — supports research/education without claiming affiliation.

**Implied endorsement / affiliation (higher risk):** Repo description, badges, or marketing that suggest SpaceX, xAI, Nasdaq, Goldman, or Morningstar **endorse, sponsor, or operate** this project; use of official logos; domains such as `spacex-research.com`; phrases like “official SPCX tracker” or “SpaceX partner API.”

---

## 中文摘要

SPACX 是针对 **Space Exploration Technologies Corp.**（SEC 申报主体）**拟上市代码 SPCX** 的**私人研究平台**。仓库名 `spacx`、项目代号 **SPACX** 以及 SpaceX、Starlink、xAI、Colossus、Anthropic、Nasdaq、Musk、Goldman、Morningstar 等名称广泛出现在证据表、Agent 命名与文档中。

**默认建议：保留 `spacx` 作为带强化免责声明的私人研究代号。** 未经维护者明确批准及律师审查，**不要**重命名 git remote 或 GitHub 仓库。工程审计本身不阻止公开，但**在 P0 商标/法律签字完成前不应公开推广**（见 [公开上线阻塞项](#public-launch-blockers-counsel-checklist)）。

| 风险域 | 公开 OSS 严重度 | 建议 |
|--------|----------------|------|
| 仓库名 `spacx` / 代号 SPACX | **中** | 保留 + 免责声明；勿以「官方 SpaceX 工具」营销 |
| 代码 `SPCX` | **低–中** | 仅作**拟上市/预期**代码，遵守 [LISTING_STATUS.md](./LISTING_STATUS.md) |
| SEC 摘录中的 SpaceX / 发行人法定名称 | **低** | **保留** — 引用申报文件的指称性合理使用 |
| Starlink、Starship、Colossus | **低–中** | 有 SEC 来源时保留并引用；不用独立 logo |
| xAI、Anthropic | **低** | 仅引用；不暗示合作 |
| Musk 姓名 | **低** | 治理/风险披露语境；不暗示背书 |
| Nasdaq | **低** | 引用 S-1/A 表述；不用 Nasdaq logo 或「合作伙伴」 |
| Goldman / Morningstar | **低** | C 级外部研究引用；带来源；不用 logo |
| Agent 命名 | **中** | 内部研究可接受；加免责声明；避免面向消费者的产品名 |
| 包名 `spacx-intelligence` | **中** | 注意与 SpaceX 消费品牌混淆；OSS 描述须清晰 |

**指称性合理使用（风险较低）：** 在引用 SEC 申报文件时准确使用发行人、分部、交易对手、交易所及拟上市代码名称，并附 accession 引用与 [DATA_PROVENANCE.md](./DATA_PROVENANCE.md) 校验。

**暗示背书/关联（风险较高）：** 仓库描述、徽章或营销暗示 SpaceX、xAI、Nasdaq、Goldman、Morningstar **背书、赞助或运营**本项目；使用官方 logo；抢注域名；「官方 SPCX 追踪器」「SpaceX 合作 API」等表述。

---

## Methodology

This audit is an **engineering research checklist**, not a legal opinion. It inventories naming across the repository, classifies uses against common nominative-fair-use vs affiliation patterns, and maps controls already in place (`COMPLIANCE.md`, `DATA_PROVENANCE.md`, `LISTING_STATUS.md`, `TERMINOLOGY.md`).

Counsel should validate against applicable jurisdictions (US Lanham Act, state right-of-publicity, exchange trademark policies, and issuer enforcement history).

---

## Asset inventory

### 1. Repository and package identifiers

| Identifier | Location | Notes |
|------------|----------|-------|
| `spacx` | GitHub repo, `pyproject.toml` name | Homophone/adjacent to “SpaceX”; not identical spelling |
| `SPACX` | README, docs codename | Research platform brand; maps to proposed ticker SPCX |
| `SPCX` | `plugin/manifest.yaml` `asset_primary`, docs | **Proposed / expected** listing symbol per S-1/A |
| `spacx-intelligence` | `plugin/manifest.yaml` id | Plugin identifier; API path `/api/v1/spacx` |

### 2. Issuer and ecosystem references

| Mark / name | Typical use in repo | Source tier |
|-------------|---------------------|-------------|
| **Space Exploration Technologies Corp.** | Issuer legal name in SEC tables | A (EDGAR) |
| **SpaceX** | Shorthand in narrative docs, workstreams | A when quoting filings; B/C in commentary |
| **Starlink** | Segment KPIs, `StarlinkAnalystAgent` | A in Phase 1 tables |
| **Starship** | Milestone agent, Capex / launch risk | A/B |
| **xAI** | AI segment post-merger disclosure | A |
| **Colossus** | xAI compute cluster (filing narrative) | A |
| **Anthropic** | Customer contract in S-1/A | A |
| **Elon Musk** | Governance, voting control disclosures | A |
| **Nasdaq** | Anticipated listing venue (S-1/A language) | A |

### 3. Third-party research marks

| Mark | Use | Grade |
|------|-----|-------|
| **Goldman Sachs** | `workstreams/valuation-research/assumptions/goldman-ai-surge-reuters.yaml` | C — via Reuters/FT summary |
| **Morningstar** | `morningstar-780b.yaml`, ValuationAnalystAgent | C — via Reuters; model not ingested |
| **SEC / EDGAR** | Filing cache, provenance | Public regulator documents |

Cached HTML and reproduction rules: [DATA_PROVENANCE.md](./DATA_PROVENANCE.md).

---

## Nominative fair use vs implied affiliation

### Generally **Keep** (with controls)

| Pattern | Example in SPACX | Required controls |
|---------|------------------|-------------------|
| Quoting issuer name from filings | “Space Exploration Technologies Corp.” in audit tables | Accession + date; no logo |
| Proposed ticker reference | “proposed / expected listing symbol SPCX” | [LISTING_STATUS.md](./LISTING_STATUS.md); never “listed” pre-424B4 |
| Segment names from disclosures | Starlink user count, Anthropic contract terms | SEC excerpt or table cite; EvidenceAuditor grade |
| Exchange as filing fact | “anticipated listing on Nasdaq” | Quote S-1/A; no Nasdaq logo |
| Third-party research attribution | “Morningstar via Reuters — Grade C” | Source YAML; no endorsement language |
| Person name in governance context | Musk voting control % | From risk/governance sections only |

### **Strengthen disclaimers** (required before public OSS)

Apply to: root [README.md](../README.md), [plugin/manifest.yaml](../plugin/manifest.yaml), all [agent READMEs](../plugin/agents/), GitHub repo description (see [BRAND_USAGE_POLICY.md](./BRAND_USAGE_POLICY.md)).

Minimum language:

> **Not affiliated with Space Exploration Technologies Corp. (SpaceX), xAI, Anthropic, Nasdaq, Goldman Sachs, Morningstar, or the SEC.** Research and education only. Not investment advice.

### **Avoid / Forbidden** in public marketing

| Pattern | Risk |
|---------|------|
| SpaceX / Starlink / xAI **logos** or trade dress | Trademark infringement |
| “Official”, “authorized”, “partner”, “endorsed by SpaceX” | Affiliation falsehood |
| Domain squatting (`spacex-ipo.com`, `spcx-official.io`) | Cybersquatting / confusion |
| GitHub topics implying endorsement (`spacex-official`) | Platform discovery confusion |
| Badges mimicking exchange or issuer branding | Trade dress |
| Removing issuer name from SEC extracts to “reduce risk” | **Do not** — breaks provenance; cite instead |

---

## Tiered recommendations

### Tier 1 — **Keep** (default)

- **Repository name `spacx`** and codename **SPACX** for private/open **research** tracking proposed symbol SPCX.
- **SEC filing reproduction** in `workstreams/sec-evidence-phase1/s1*.htm` and derived tables — with [DATA_PROVENANCE.md](./DATA_PROVENANCE.md) SHA-256 and EDGAR link preference for redistribution.
- **Agent and segment naming** aligned to filing vocabulary (`StarlinkAnalystAgent`, `AIComputeAnalystAgent`) — internal research tooling, not consumer product.
- **Third-party marks** (Goldman, Morningstar) as **citation-only** Grade-C assumptions.

### Tier 2 — **Strengthen** (implement before public flip)

- Prominent README disclaimer with full issuer legal name.
- [BRAND_USAGE_POLICY.md](./BRAND_USAGE_POLICY.md) linked from README and CONTRIBUTING.
- Agent README footer (one line + link to policy).
- GitHub description template (no “SpaceX official”).
- `NOTICE` / release notes: no implied affiliation.

### Tier 3 — **Consider rename** (only if counsel or maintainer directs)

Evaluate if public launch draws **cease-and-desist** or platform confusion complaints.

| Candidate | Pros | Cons |
|-----------|------|------|
| `sec-spcx-research` | Descriptive; ties to SEC + proposed ticker | Long; loses SPACX codename; migration cost |
| `orbital-equity-research` | Generic; less issuer-adjacent | Loses SPCX signal; vague for contributors |
| `spacx-research` (rename display only) | Minor clarity | **Does not** materially reduce SpaceX phonetic similarity |
| Keep `spacx` + disclaimers | Zero migration; established CI/tests | Residual phonetic confusion risk |

**Default: keep `spacx` private research with disclaimers.** Rename is **not** recommended by this engineering audit unless counsel advises otherwise or enforcement action occurs.

---

## SEC filing reproduction

SPACX already documents redistribution posture in [DATA_PROVENANCE.md](./DATA_PROVENANCE.md):

- Cached HTML = **research evidence attachments**, not a republishing service.
- Prefer **EDGAR accession URLs** + local SHA-256 over bulk mirrors.
- Derived tables must cite form, date, section; respect 424B4-pending fields.

**Do not remove** SEC-required entity names (issuer, segments, counterparties) from extracts — removal harms audit integrity and does not eliminate nominative need to identify the subject of research.

Cross-link: all new public docs should reference DATA_PROVENANCE for filing copy policy.

---

## Public launch blockers (counsel checklist)

**Not legal advice.** Before flipping repository visibility or marketing SPACX broadly:

| # | Gate | Owner |
|---|------|-------|
| 1 | Counsel review of repo name `spacx`, codename SPACX, and `spacx-intelligence` package id | **P0 — human** |
| 2 | Confirm nominative use defense sufficient for SEC extract redistribution in target jurisdictions | Counsel |
| 3 | Review GitHub public description, social posts, and any website for affiliation language | Maintainer + counsel |
| 4 | Confirm no issuer/exchange/third-party **logos** in repo, README, or release assets | Maintainer |
| 5 | Verify fork/badge policy communicated ([BRAND_USAGE_POLICY.md](./BRAND_USAGE_POLICY.md)) | Maintainer |
| 6 | Document counsel sign-off date in [OPEN_SOURCE_READINESS.md](./OPEN_SOURCE_READINESS.md) | **P0 — human** |
| 7 | Monitor post-launch for confusion reports or takedown notices | Ongoing |

Until row 6 is complete, treat trademark posture as **engineering-complete, legally unsigned**.

---

## Files reviewed (representative)

- [README.md](../README.md), [plugin/manifest.yaml](../plugin/manifest.yaml)
- [docs/COMPLIANCE.md](./COMPLIANCE.md), [docs/LISTING_STATUS.md](./LISTING_STATUS.md), [docs/DATA_PROVENANCE.md](./DATA_PROVENANCE.md)
- [workstreams/sec-evidence-phase1/](../workstreams/sec-evidence-phase1/) (tables + cached HTML)
- [workstreams/valuation-research/assumptions/](../workstreams/valuation-research/assumptions/) (Goldman, Morningstar YAML)
- [plugin/agents/*/README.md](../plugin/agents/) (agent naming)

---

## Revision history

| Date | Change |
|------|--------|
| 2026-06-05 | Initial engineering audit pre-public OSS |
