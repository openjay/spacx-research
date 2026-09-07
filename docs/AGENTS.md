# SPACX agent orchestration

Nine intelligence agents under `plugin/agents/`. Scheduler: [`plugin/scheduler.yaml`](../plugin/scheduler.yaml). Compliance: [`COMPLIANCE.md`](COMPLIANCE.md). Phase 1 evidence baseline: [integrated audit opinion](../workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md).

## Agent roster

| Agent | Primary function | Schedule source |
|-------|------------------|----------------|
| **SECFilingAgent** | EDGAR monitor; FWP review; 424B4 P0 | `agent.yaml` / scheduler |
| **EvidenceAuditorAgent** | A/B/C/D grading; gap register | `agent.yaml` / scheduler |
| **StarlinkAnalystAgent** | Connectivity KPIs | `agent.yaml` / scheduler |
| **AIComputeAnalystAgent** | AI segment / Anthropic | `agent.yaml` / scheduler |
| **StarshipMilestoneAgent** | Space / Starship milestones | `agent.yaml` / scheduler |
| **LockupFloatAgent** | Float path model | `agent.yaml` / scheduler |
| **ValuationAnalystAgent** | C-tier valuation anchors; reverse DCF; no SEC override | `agent.yaml` / scheduler |
| **MacroLiquidityAgent** | Macro liquidity context | `agent.yaml` / scheduler |
| **OnchainRWAAgent** | RWA + evidence hash (**no trading**) | `agent.yaml` / scheduler |

## Source and execution boundaries

Agent contracts live in `plugin/agents/<Agent>/agent.yaml`; their READMEs explain
the roles. Read [DATA_PROVENANCE.md](DATA_PROVENANCE.md) for source handling and
[LISTING_STATUS.md](LISTING_STATUS.md) with its dated evidence when listing status
matters. Fetch figures, dates and thresholds from the maintained input artifacts.
A role description, scheduler declaration or historical report does not prove
current data, runtime activation or authorization.

Preserve typed events, metric IDs, source grades and forbidden actions. FWP remains
an offering communication and cannot clear a 424B4 blocker. EvidenceAuditor retains
material-gap gating; MacroLiquidity context remains C/D, not SEC-primary evidence.
SEC-primary
financial anchors cannot be overwritten by third-party estimates. A hash binds
bytes, not claim truth. Label assumptions and unresolved contradictions; report
verification scope. OnchainRWA remains monitor-and-hash, with no wallet, custody,
order-routing or auto-trading operations.

## Human-over-the-loop gates

| Gate ID | Owner trigger | Blocks until human OK |
|---------|---------------|------------------------|
| `p0_424b4_review` | SECFilingAgent P0 | Phase 2 table refresh, final offering column |
| `material_gap_resolution` | EvidenceAuditorAgent | Bull/Base/Bear thesis update |
| `day0_anchor_confirmation` | LockupFloatAgent | Production tradable-float chart |
| `thesis_publish` | Daily scheduler 18:00 ET | External distribution of daily report |
| `A_grade_promotion` | EvidenceAuditorAgent | Any claim promoted to grade A |
| `hash_mismatch_investigation` | OnchainRWAAgent | Artifact restore from manifest |

Automation may **draft** reports and alerts; it may **not** bypass gates for external channels (compliance level ≥ 2).

## Historical context

The [Phase 1 audit](../workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)
is a dated baseline, not current listing, pricing or gate status. Read the maintained
[listing-status record](LISTING_STATUS.md) and any subsequent dated adjudication
before carrying its B-007/B-008 findings into a new report. A later evidenced closure
must not be silently reopened by a stale template; conversely, a historical closure
or “only active blocker” statement does not establish today's status. If current
evidence is unavailable, report that limit rather than assuming a gate is open or
closed. Preserve the original reports and their evidence periods.
