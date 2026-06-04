# SPACX

**SPACX** is a research and execution platform for public equity tied to the Musk / SpaceX ecosystem — listed ticker **SPCX** (Space Exploration Technologies Corp.). This repository is the project home for structured evidence, audits, and planned AI-native workflows. It is **not** an IPO research repo by identity: SEC filing work is **Workstream 1** only.

## Disclaimer

This repository is for **research and education**. It is **not investment advice**, not a solicitation, and not affiliated with SpaceX, xAI, or the SEC. Verify all figures against current SEC filings and your own diligence before any decision.

**Integrated audit synthesis (Workstream 1):** [workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md](workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)

## Workstreams

| Workstream | Path | Status | Focus |
|------------|------|--------|--------|
| **SEC evidence (Phase 1)** | [`workstreams/sec-evidence-phase1/`](workstreams/sec-evidence-phase1/) | **Done** | S-1 / S-1/A tables, Tracks A–D audit, cached filing HTML |
| **SEC watchlist (Phase 2)** | [`workstreams/sec-evidence-phase2/`](workstreams/sec-evidence-phase2/) | **Done** | Starlink / AI / Starship quality tables → [`plugin/metrics/registry.yaml`](plugin/metrics/registry.yaml) |
| **AI-native intelligence plugin** | [`plugin/`](plugin/) | **V0 scaffold** | `spacx-intelligence` — [AGENTS](docs/AGENTS.md), [MODELS](docs/MODELS.md), [manifest](plugin/manifest.yaml); compliance level 2 |
| **Trading workflows** | *(planned)* | Planned | Signal → execution research (non-production) |

Roadmap detail: [docs/ROADMAP.md](docs/ROADMAP.md)

## Clone

```bash
git clone git@github.com:openjay/spacx.git
# or
git clone https://github.com/openjay/spacx.git
```

Private repo — access via the `openjay` GitHub account. Remote notes: [GITHUB.md](GITHUB.md)

## Repository layout

| Path | Contents |
|------|----------|
| `docs/ROADMAP.md` | Workstream roadmap |
| `docs/ARCHITECTURE.md` | Plugin layers, scheduler, compliance 0–6 (EN + 中文) |
| `plugin/` | Intelligence plugin manifest, schemas, `api/` stubs |
| `workstreams/sec-evidence-phase1/` | Phase 1 SEC tables (`00`–`04`), `audit/`, `s1*.htm` |
| `LICENSE` | MIT |
| `GITHUB.md` | Remote URL and branch notes |

## License

MIT — see [LICENSE](LICENSE).

---

## 中文简介

**SPACX** 是围绕马斯克 / SpaceX 生态上市股权（股票代码 **SPCX**）的研究与执行平台仓库，而非以「IPO 研究」命名的项目。当前已完成 **工作流 1**：仅基于 SEC 申报文件的 Phase 1 证据表与 A–D 轨审计；**工作流 2** 正在建设 [`plugin/`](plugin/) 下的 AI 原生情报插件（7×24 研究、告警、行动建议，V0 不自动交易）。内容仅供研究学习，**不构成投资建议**。综合审计结论见 [workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md](workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)。
