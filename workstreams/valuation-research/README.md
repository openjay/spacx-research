# Valuation Research Workstream

**Status:** Active (CFA external evidence layer)  
**Authority:** SEC A-tier from [sec-evidence-phase1/audit/05-master-evidence-tables.md](../sec-evidence-phase1/audit/05-master-evidence-tables.md) — this workstream does **not** override filing numbers.

## Purpose

Index third-party valuation models and scenario framing for SPCX. All external fair-value claims are **C-tier** unless sourced from SEC primary documents.

## Assumption packets

Structured C-tier external research ingested as `ExternalResearchPacket` YAML:

| Packet | File |
|--------|------|
| Morningstar ~$780B (Reuters 2026-06-02) | [`assumptions/morningstar-780b.yaml`](./assumptions/morningstar-780b.yaml) |
| New Constructs reverse DCF (~$500B bear) | [`assumptions/new-constructs-reverse-dcf.yaml`](./assumptions/new-constructs-reverse-dcf.yaml) |
| Goldman AI surge (Reuters/FT) | [`assumptions/goldman-ai-surge-reuters.yaml`](./assumptions/goldman-ai-surge-reuters.yaml) |

Schema: [`plugin/schemas/ExternalResearchPacket.json`](../../plugin/schemas/ExternalResearchPacket.json). Policy: [CFA_RESEARCH_POLICY.md §3.1](../../docs/CFA_RESEARCH_POLICY.md).

## External model index (C-tier)

| Provider | Fair value / EV | Implied price | Tier | Conflict flags |
|----------|-----------------|---------------|------|----------------|
| **Morningstar** (via Reuters) | ~$780B | ~$60/sh | C | `EXTERNAL_DCF_NOT_VERIFIED`, `BELOW_IPO_ISSUE_ANCHOR` |
| **New Constructs** | ~$500B | ~$38/sh | C | `EXTERNAL_DCF_NOT_VERIFIED`, bear stress vs IPO anchor |
| **Goldman Sachs** (AI surge narrative) | Not fixed — thematic | N/A | C | `THEMATIC_ONLY`, `NO_VERIFIED_MODEL` |

Implementation: `plugin/valuation/price_anchors.yaml`, `plugin/schemas/ExternalResearchPacket.json`, `ValuationAnalystAgent`.

## SEC anchors (A-tier)

| Anchor | Value | Source |
|--------|-------|--------|
| Expected IPO price | **$135.00/sh** | S-1/A #2 Cover; *The Offering* |
| Implied market cap | **~$1.75T** | 13,075,865,175 shares × $135 |
| FY2025 consolidated revenue | **$18,674M** | Note 3 / Table 2 |
| FY2025 consolidated Adj. EBITDA | **$6,584M** | Table 2 |

## Plugin paths

| Path | Role |
|------|------|
| [`plugin/valuation/`](../../plugin/valuation/) | SOTP, anchors, reverse DCF, implied multiples |
| [`plugin/agents/ValuationAnalystAgent/`](../../plugin/agents/ValuationAnalystAgent/) | Agent contract |
| [`plugin/metrics/registry.yaml`](../../plugin/metrics/registry.yaml) | `valuation_metrics` block |

## Audit

Full conflict matrix and assumption log: **[VALUATION_AUDIT.md](./VALUATION_AUDIT.md)**

## Observation band (no fundamental claim)

`fomo_trading_band` ($185–300) in `price_anchors.yaml` is **observation-only** (D-tier sentiment). It must not be cited as fair value.
