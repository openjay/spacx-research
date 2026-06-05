# SPACX-Research

**SPACX-Research** is a research and execution platform for equity tied to the Musk / SpaceX ecosystem — **proposed / expected listing symbol SPCX** (Space Exploration Technologies Corp.; pending Form 424B4 and first trading confirmation). This repository is the project home for structured evidence, audits, and planned AI-native workflows. It is **not** an IPO research repo by identity: SEC filing work is **Workstream 1** only.

## Disclaimer

**Not affiliated with Space Exploration Technologies Corp. (SpaceX), xAI, Anthropic, Nasdaq, Goldman Sachs, Morningstar, or the SEC.**

This repository is for **research and education** only — **not investment advice** and not a solicitation. Verify all figures against current SEC filings and your own diligence before any decision. Brand and trademark rules: [docs/BRAND_USAGE_POLICY.md](docs/BRAND_USAGE_POLICY.md) · [docs/TRADEMARK_BRAND_AUDIT.md](docs/TRADEMARK_BRAND_AUDIT.md)

**Integrated audit synthesis (Workstream 1):** [workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md](workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)

## Workstreams

| Workstream | Path | Status | Focus |
|------------|------|--------|--------|
| **SEC evidence (Phase 1)** | [`workstreams/sec-evidence-phase1/`](workstreams/sec-evidence-phase1/) | **Done** | S-1 / S-1/A tables, Tracks A–D audit, cached filing HTML |
| **SEC watchlist (Phase 2)** | [`workstreams/sec-evidence-phase2/`](workstreams/sec-evidence-phase2/) | **Done** | Starlink / AI / Starship quality tables → [`plugin/metrics/registry.yaml`](plugin/metrics/registry.yaml) |
| **AI-native intelligence plugin** | [`plugin/`](plugin/) | **V0 scaffold** | `spacx-research-intelligence` — [AGENTS](docs/AGENTS.md), [MODELS](docs/MODELS.md), [manifest](plugin/manifest.yaml); compliance level 2 |
| **Valuation & external evidence** | [`workstreams/valuation-research/`](workstreams/valuation-research/) · [`plugin/valuation/`](plugin/valuation/) | **Active** | SOTP 4-layer, price anchors, C-tier external models; SEC A-tier authoritative |
| **Web3 / RWA pre-layer** | [docs/RWA_WEB3_STRATEGY.md](docs/RWA_WEB3_STRATEGY.md) · [`plugin/agents/OnchainRWAAgent/`](plugin/agents/OnchainRWAAgent/) | **Planned / pre-layer** | Evidence hash + chain monitor (W1); no auto on-chain trading |
| **Trading workflows** | *(planned)* | Planned | Signal → execution research (non-production) |

Roadmap detail: [docs/ROADMAP.md](docs/ROADMAP.md)

## Clone

```bash
git clone git@github.com:openjay/spacx-research.git
# or
git clone https://github.com/openjay/spacx-research.git
```

Repository visibility is gated by [docs/PUBLIC_LAUNCH_CHECKLIST.md](docs/PUBLIC_LAUNCH_CHECKLIST.md). Until P0 launch gates are signed off, the remote may remain private under the `openjay` GitHub account. Remote notes: [GITHUB.md](GITHUB.md)

## Repository layout

| Path | Contents |
|------|----------|
| `docs/ROADMAP.md` | Workstream roadmap |
| `docs/COMPLIANCE.md` | Compliance levels 0–6, agent boundaries |
| `docs/CFA_RESEARCH_POLICY.md` | CFA-aligned research policy |
| `docs/LISTING_STATUS.md` | SPCX proposed symbol / pre-listing status |
| `docs/TERMINOLOGY.md` | Bilingual securities terminology guardrails |
| `docs/DATA_PROVENANCE.md` | SEC cache provenance and SHA-256 verification |
| `docs/TRADEMARK_BRAND_AUDIT.md` | Trademark / brand risk audit (pre-public OSS) |
| `docs/BRAND_USAGE_POLICY.md` | Allowed vs forbidden third-party mark usage |
| `docs/RWA_WEB3_STRATEGY.md` | Web3/RWA pre-layer strategy (预埋, EN + 中文) |
| `docs/ARCHITECTURE.md` | Plugin layers, `rwa/` data lane, compliance 0–6 (EN + 中文) |
| `plugin/` | Intelligence plugin manifest, schemas, `api/` stubs |
| `workstreams/sec-evidence-phase1/` | Phase 1 SEC tables (`00`–`04`), `audit/`, `s1*.htm` |
| `LICENSE` | MIT |
| `GITHUB.md` | Remote URL and branch notes |

## License

MIT — see [LICENSE](LICENSE).

---

## 中文简介

**SPACX-Research** 是围绕马斯克 / SpaceX 生态**拟上市/预期上市**证券（**预期上市代码 SPCX**；待 Form 424B4 与首笔交易确认）的研究与执行平台仓库，而非以「IPO 研究」命名的项目。**与 Space Exploration Technologies Corp.（SpaceX）、xAI、Anthropic、Nasdaq 及 SEC 均无关联。** 当前已完成 **工作流 1**：仅基于 SEC 申报文件的 Phase 1 证据表与 A–D 轨审计；**工作流 2** 正在建设 [`plugin/`](plugin/) 下的 AI 原生情报插件（7×24 研究、告警、行动建议，V0 不自动交易）。内容仅供研究学习，**不构成投资建议**。商标与品牌规则见 [docs/BRAND_USAGE_POLICY.md](docs/BRAND_USAGE_POLICY.md)。综合审计结论见 [workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md](workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)。上市状态见 [docs/LISTING_STATUS.md](docs/LISTING_STATUS.md)。
