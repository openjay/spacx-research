# Research & planning end-to-end retrospective — Audit Track RES

**Audit date:** 2026-06-10 (T-1 to expected pricing 2026-06-11; T-2 to expected first trade 2026-06-12)
**Scope:** Research quality, CFA compliance, planning robustness — full project retrospective (v0.1.0, public repo)
**Auditor:** Audit Track RES (agent-assisted; human review pending)
**Not investment advice. Not legal advice.**

Related: [LISTING_STATUS.md](../LISTING_STATUS.md) · [CFA_RESEARCH_POLICY.md](../CFA_RESEARCH_POLICY.md) · [ROADMAP.md](../ROADMAP.md) · [C-gap-register.md](../../workstreams/sec-evidence-phase1/audit/C-gap-register.md)

---

## Executive summary (EN)

The 5-step master plan is structurally sound and substantially executed for its pre-listing scope: the SEC evidence base (Phase 1 + Tracks A–D), the three flywheel tracking tables (Phase 2), the OBSERVE_ONLY gate discipline, and the lock-up supply model are all delivered and traceable. Tests pass (65/65). **Estimated plan completion: ~70% overall (~95% of the pre-listing scope; steps 4–5 are event-gated by design but lack execution tooling).**

**P0 findings (live SEC check, 2026-06-10):**

1. **Form 424B4 is NOT yet filed** as of this check — consistent with expected pricing on 2026-06-11. Blockers (`FINAL_PROSPECTUS_PENDING`, `LOCKUP_DAY0_UNKNOWN`, `FIRST_EARNINGS_PENDING`) are **correctly still active**.
2. **LISTING_STATUS.md is stale**: EDGAR shows **four FWP filings not recorded in the repo** — 2026-06-05 (×2: `0001628280-26-041150`, `0001628280-26-041013`), 2026-06-08 (`0001628280-26-041365`, EU interview transcript), 2026-06-09 (`0001628280-26-041761`, CFO interview). `last_sec_check_date` is 2026-06-04 — six days stale during pricing week. The repo's own `scripts/check_sec_feed_sync.py` **fails** when run today (`undocumented_filings`), but CI only triggers on push/PR, and the repo has been quiet since 2026-06-05, so the drift went undetected.
3. **Evidence-hash retention is documented but unpopulated**: `workstreams/sec-evidence-phase1/cache/` (FWP cache + `manifest.json`) described in LISTING_STATUS.md **does not exist**; no actual SHA-256 digest values are stored anywhere in the repo. CFA Standard V(A) record-retention claims currently exceed implementation.

**Top blind spots:** no scheduled (cron) EDGAR polling; no market-data lane for day-1 metrics; no playbook for IPO postponement / price revision / same-day 424B4 mechanics; no 10-Q/earnings parser for plan step 4; no index-inclusion or post-listing corporate-events lane.

**Recommendation:** Execute Phase 3 "listing-day readiness" immediately (see §7) — the next 48 hours are the highest-information-density window in the project's life, and current automation will not catch the 424B4 without a manual or scheduled trigger.

---

## 执行摘要（中文）

五步主计划在「上市前」范围内基本执行到位：S-1/S-1A 证据底座（Phase 1 + A–D 审计轨）、Starlink / AI / Starship 三条独立跟踪表（Phase 2 + 指标注册表）、OBSERVE_ONLY 观察仓纪律、解禁供给日历模型均已交付且可追溯，测试全部通过（65/65）。**计划完成度估计：整体约 70%（上市前范围约 95%；第 4、5 步按设计为事件门控，但缺乏执行工具）。**

**P0 发现（2026-06-10 实时 SEC 核查）：**

1. **424B4 截至本次核查尚未提交** — 与预期 6/11 定价一致，三个 blocker 保持激活是**正确的**。
2. **LISTING_STATUS.md 已过期**：EDGAR 上有 **4 份未入账的 FWP**（6/5 两份、6/8 欧盟访谈记录、6/9 CFO 访谈），最后核查日期停留在 6/4 — 定价周内信息滞后 6 天。仓库自带的 SEC 同步检查脚本今日运行即报失败，但 CI 仅在 push/PR 时触发，6/5 之后仓库无提交，漂移因此未被发现。
3. **证据哈希留存「有文档、无落地」**：LISTING_STATUS.md 描述的 FWP 缓存目录与 manifest.json **不存在**，仓库内没有任何实际 SHA-256 哈希值。CFA V(A) 记录留存承诺目前超出实际实现。

**主要盲区：** 无定时（cron）EDGAR 轮询；无行情数据通道（上市首日指标无法计量）；无 IPO 推迟/改价/424B4 当日机制预案；无 10-Q/财报解析器（主计划第 4 步无工具支撑）；无指数纳入（纳指 100）与上市后公司事件通道。

**建议：** 立即启动 Phase 3「上市日就绪」（见 §7）— 未来 48 小时是项目信息密度最高的窗口，而当前自动化在无人触发的情况下不会捕获 424B4。

---

## 1. Plan-vs-execution matrix

Master plan (5 steps + supporting commitments) → status → evidence → residual gap.

| # | Planned item | Status | Evidence | Residual gap |
|---|--------------|--------|----------|--------------|
| 1 | 读 S-1/S-1A 完整证据底座 | ✅ **Done** | `workstreams/sec-evidence-phase1/` tables 00–04; Tracks A–D audit workpapers; cached `s1*.htm`; integrated audit opinion | Anthropic contract exhibit (G-14), RPT exhibit schedule (G-34) never pulled from EDGAR index; gap register itself flags 36 items, 5 of them P0 — all 424B4/10-Q-gated by design |
| 2 | Starlink / AI / Starship 三条独立跟踪表 | ✅ **Done** | `workstreams/sec-evidence-phase2/` (starlink-quality, ai-compute-quality, starship-milestones); `plugin/metrics/registry.yaml` 3 flywheels / 21 flywheel metrics with SEC baselines | Tables are static snapshots of Q1 2026 / FY 2025; no refresh mechanism until a 10-Q parser exists (see step 4) |
| 3 | 首发只允许观察仓 | ✅ **Encoded & operating** | `ActionProposal` default `OBSERVE_ONLY`; 3 active blockers in registry; runtime receipts (`runtime/data/jsonl/`) show `observation_only: true`, `blockers_clear: false` on every snapshot; CFA policy §6 | Gate flipping procedure exists on paper only — no rehearsal of what unlocking actually looks like (who flips, what evidence is required, what the first post-flip artifact is) |
| 4 | 等上市后第一份财报验证 | ⏳ **Pending (by design) — tooling absent** | `FIRST_EARNINGS_PENDING` blocker; W03–W08 watch metrics declared with `10-Q` source priority | **No 10-Q/earnings parser, no earnings-calendar lane, no XBRL ingestion.** When the first 10-Q lands, every quarterly metric requires manual extraction. The plan can *wait* but cannot yet *verify* |
| 5 | 等解禁供给被消化后再判断仓位 | ⏳ **Encoded — pending day-0** | `B-lock-up-schedule.md` (full tranche calendar: days 70/90/91/105/120/135/180, earnings gates, $175.50 price trigger, Musk 366d no-early-release); `LockupFloatAgent`; W10, G04–G07 metrics | Day-0 unknown until 424B4 (correct); **no float-consumption data source** (volume vs released shares needs market data); price-trigger tranche (≥130% × IPO for 5-of-10 days) needs daily closes nobody ingests yet |
| 6 | 12 watch metrics | ✅ **Done** | `registry.yaml`: W01–W12 with formulas, source priority, baselines, amber/red thresholds; `threshold_engine.py` | W02 (first-day pop) and all `daily_post_ipo` cadences have **no data source** — see blind spot BS-2 |
| 7 | Valuation anchors ($60 C-tier DCF / $135 A-tier IPO / $185–300 FOMO band) | ✅ **Done** | `plugin/valuation/` (sotp, reverse DCF, anchors, scenario bands); `valuation_metrics` in registry; 3 `ExternalResearchPacket` YAMLs with tiering + conflict flags | Anchors freeze at $135 expected price; **no procedure for re-anchoring when 424B4 prints a different final price** (every baseline keyed to `IPO_issue_anchor_135` must be re-derived) |
| 8 | Web3/RWA pre-layer (预埋) | 🟡 **Partial (W1 of W1–W4)** | `RWA_WEB3_STRATEGY.md`; `plugin/rwa/`, `OnchainRWAAgent` contract; constitutional rules documented | Evidence-hash manifests — the core W1 deliverable — **not populated** (see P0-3); W2–W4 planned only |
| 9 | AI-native autonomy + human P0 gates | 🟡 **Mostly done (V0)** | 9 agent contracts; compliance level 2; scheduler.yaml; runtime worker/poll/persistence/health; human gates (`thesis_publish`, `hash_mismatch_investigation`) | Runtime is **not deployed anywhere persistent** — last runtime event 2026-06-05; autonomy exists only when a human starts the worker |

**Completion arithmetic:** steps 1–3 + items 6–7 ≈ complete (5/9), items 8–9 partial (~0.5 + 0.8), steps 4–5 encoded-but-unexecutable (~0.2 + 0.6) → **≈ 70% overall; ~95% of what could be done pre-listing.** The honest framing: the *research* plan is nearly complete; the *operational* plan (what happens when events fire) is roughly half-built.

---

## 2. Live SEC check (P0) — EDGAR CIK 0001181412, checked 2026-06-10

Source: `https://data.sec.gov/submissions/CIK0001181412.json` (fetched live during this audit).

| Filing date | Form | Accession | Primary doc | In repo? |
|-------------|------|-----------|-------------|----------|
| **2026-06-09** | FWP | `0001628280-26-041761` | `fwp_cfointerview.htm` | ❌ **Not recorded** |
| **2026-06-08** | FWP | `0001628280-26-041365` | `eu_interviewtranscript06.htm` | ❌ **Not recorded** |
| **2026-06-05** | FWP | `0001628280-26-041150` | `spacexagreementfwp.htm` | ❌ **Not recorded** |
| **2026-06-05** | FWP | `0001628280-26-041013` | `japanfwp_06042026.htm` | ❌ **Not recorded** |
| 2026-06-04 | FWP | `0001628280-26-040874` | `spacexukfwp.htm` | ✅ |
| 2026-06-04 | FWP | `0001628280-26-040610` | `spacexfwp.htm` | ✅ |
| 2026-06-03 | S-1/A | `0001628280-26-040364` | (Amendment No. 2) | ✅ |
| 2026-06-01 | S-1/A | `0001628280-26-039276` | (Amendment No. 1) | ✅ |
| 2026-05-20 | S-1 | `0001628280-26-036936` | (Original) | ✅ |

### Findings

- **F-1 (P0): 424B4 status = `pending` is still CORRECT.** No 424B4, no 8-K, no RW/withdrawal on the feed as of this check. With pricing expected 2026-06-11, the 424B4 will likely hit EDGAR within ~24–48h of this audit. Blockers must not be flipped yet — but the project must be ready to flip them (see §7).
- **F-2 (P0): Four undocumented FWPs.** `LISTING_STATUS.md` front-matter (`last_sec_check_date: 2026-06-04`) and `latest_known_filings` are six days stale during the single most filing-dense week of the deal. The repo's own gate, `scripts/check_sec_feed_sync.py`, returns `status: fail / undocumented_filings` when run today — the control works; the *trigger* doesn't (CI runs on push/PR only; no commits since 2026-06-05 → no CI run → silent drift).
- **F-3 (P1): Filing pattern is informative and unclassified.** UK / Japan / EU / CFO-interview FWPs indicate an international retail-facing communications push under Rule 433 in pricing week. The repo treats all FWPs as undifferentiated "offering communications"; there is no sub-classification (marketing vs terms-bearing). A terms-bearing FWP (e.g., a price-range update) would deserve different handling than an interview transcript.
- **F-4 (P0, conditional): FWP ingest automation has never run end-to-end.** LISTING_STATUS.md states FWPs are downloaded to `workstreams/sec-evidence-phase1/cache/fwp/` with SHA-256 in `cache/manifest.json` and a sealed tier-A `EvidencePacket`. **The `cache/` directory does not exist.** The documented chain of custody for the 6/4 FWPs (and obviously the four new ones) was not produced.

---

## 3. Freshness audit (claims vs 2026-06-10)

| Artifact | Claimed date / horizon | Status today | Verdict |
|----------|------------------------|--------------|---------|
| `LISTING_STATUS.md` `last_sec_check_date` | 2026-06-04 | 4 newer FWPs on EDGAR | ❌ **Stale (P0)** — worst possible week for it |
| `LISTING_STATUS.md` "Last updated" | 2026-06-05 | Narrative still accurate (424B4 pending) but filing list incomplete | 🟡 Partially stale |
| Runtime EDGAR receipts (`audit_receipt.jsonl`) | Last poll 2026-06-05T04:29Z | No polls in 5 days | ❌ **Stale** — runtime not running |
| `morningstar-780b.yaml` | as_of 2026-06-02, expires 2026-07-02 | Within window | ✅ Fresh |
| `new-constructs-reverse-dcf.yaml` | as_of 2026-06-01, expires 2026-07-01 | Within window | ✅ Fresh |
| `goldman-ai-surge-reuters.yaml` | as_of 2026-06-04, expires 2026-07-04 | Within window | ✅ Fresh |
| Phase 1 tables / audit (as-of S-1/A #2, 2026-06-03) | Point-in-time | S-1/A #2 remains the latest terms-bearing filing | ✅ Still authoritative |
| Registry baselines (Q1 2026 / `IPO_issue_anchor_135`) | Pre-pricing | Correct until 424B4 prints final price | ✅ / ⚠ re-anchor procedure missing |
| `GITHUB.md` "HEAD: 55e0bf9" | — | Actual HEAD differs (self-referential doc can never match) | 🟡 Minor; drop the field or automate |

**Conclusion:** External C-tier research is within its declared freshness windows (the `expires_at` discipline works). The freshness failure is concentrated exactly where it hurts most: **the SEC feed during pricing week**, because all freshness machinery is event-driven on repo activity rather than time-driven.

---

## 4. CFA standards conformance scorecard

| Dimension | Standard | Score | Evidence & notes |
|-----------|----------|-------|------------------|
| Facts vs opinions separation | V(A), V(B) | **A** | Structural separation enforced: SEC tables vs narrative; schema fields vs LLM prose; "LLM may not invent filing numbers or upgrade grades" codified. Phase 1/2 tables cite form, date, section consistently |
| Source tiering (A/B/C/D) applied | V(A) | **A−** | Tiering consistently applied: A-tier SEC anchors vs C-tier external DCFs ($780B Morningstar, $500B New Constructs) vs D-tier FOMO band explicitly marked "observation-only, must not be cited as fair value". Minor: tier assignment for FWP interview transcripts (A-tier *filings* containing B-tier-quality *content*) is unaddressed |
| Conflict-of-interest flags | VI(A) | **A** | `LEAD_UNDERWRITER`, `UNVERIFIED_FT_REPORT` flags live in `goldman-ai-surge-reuters.yaml`; underwriter conflict template in policy; Goldman lock-up waiver discretion flagged in lock-up audit |
| OBSERVE_ONLY discipline traceable | III(C), V(A) | **A−** | Traceable end-to-end: policy §6 → registry blockers → runtime receipts showing `observation_only: true` on every metric snapshot. Deduction: receipts stop 2026-06-05; discipline is only evidenced when the runtime runs |
| Record retention / evidence hashes | V(C) | **D** | **Documented, not populated.** No SHA-256 digest values exist anywhere in the repo; `cache/manifest.json` absent; `EvidencePacket` sealing never executed against real filings. The 7-year retention target and `hash_mismatch_investigation` gate are aspirational. This is the single largest gap between stated policy and practice — and it is now public |
| Freshness / diligence currency | V(A) | **C+** | `expires_at` discipline on external packets: good. SEC feed currency: failed during the critical week (§3). A reasonable-basis standard requires checking the feed before relying on "424B4 pending" |
| Fair dealing / distribution gates | III(B) | **A** | Level 0–4 distribution gates; retail distribution prohibited; provenance footers required; public-repo disclaimers and approved-wording list in place |

**Overall: B+.** Policy architecture is genuinely CFA-grade; the failures are operational (retention unpopulated, feed stale), not conceptual. Both are fixable in days.

---

## 5. Blind-spot register (planning robustness)

Scenarios the current plan does not handle, ranked by proximity × impact.

| ID | Blind spot | Why it bites | Mitigation |
|----|-----------|--------------|------------|
| **BS-1** | **No scheduled EDGAR polling.** CI sync gate fires on push/PR only; runtime poller requires a human to start it. A 424B4 filed at 17:00 ET on 6/11 reaches the repo only when someone manually checks | The single most important filing of the project will arrive within ~48h and nothing will notice | Add `schedule:` cron to CI (e.g. every 2–4h through June, respecting EDGAR rate guidance) that runs `check_sec_feed_sync.py` and opens an issue/fails loudly on drift; pricing week: manual twice-daily check as backstop |
| **BS-2** | **No market-data lane.** W02 (first-day pop), W10 (float at gates), `IMPLIED_MARKET_CAP_USD`, `PRICE_VS_DCF_ANCHOR_PCT`, and the $175.50 lock-up price trigger all need daily (or intraday) prices. No source, no schema, no ingestion contract exists | Day-1 is un-measurable; the lock-up +10% tranche trigger (5-of-10 days ≥130% of IPO price ending at first earnings) cannot be tracked from day 1, and it needs history from day 1 | Define a `MarketDataPacket` (B-tier: exchange/consolidated tape via reputable API) before first trade; even a manual daily-close CSV with provenance beats nothing; record day-1 OHLCV by hand if needed |
| **BS-3** | **No 424B4-day mechanics or deal-change playbook.** Plan assumes binary pending→filed. Reality: same-day pricing (file overnight 6/11→6/12), upsize/downsize, price-range revision via new FWP/S-1/A, postponement, or full withdrawal (RW). Every registry baseline is keyed `IPO_issue_anchor_135` with no re-anchor procedure | If 424B4 prints e.g. $150 or the deal is postponed, all 4 valuation metrics, the lock-up price trigger ($175.50 = 130% × $135), G-01/02/06, and LISTING_STATUS wording need coordinated same-day updates with no checklist | Write a 424B4-day runbook now: fields to extract (final price, shares, spread, listing date), files to touch (registry baselines, price_anchors.yaml, LISTING_STATUS, lock-up trigger price), blocker-flip criteria, and a postponement/withdrawal branch |
| **BS-4** | **No 10-Q/earnings tooling (plan step 4 has no implementation).** First earnings is the plan's designated verification event — and the lock-up calendar's biggest tranche gates (Q2 earnings ≈20%+10%, Q3 ≈28%) hang off earnings dates | When the first 10-Q lands (~Aug 2026), Anthropic revenue recognition (G-11), customer concentration (G-19), segment KPI refresh — all manual; earnings-date capture itself has no lane | Phase 3.5: XBRL/10-Q extraction pipeline reusing Phase 1 table schemas; an `EARNINGS_CALENDAR` metric (8-K/press-release sourced) so lock-up day math is computable the moment dates are announced |
| **BS-5** | **No post-listing corporate-events lane (index inclusion, 8-K).** Nasdaq-100 fast-track (and eventual S&P eligibility debates), milestone-vesting 8-Ks (G-32), EchoStar close (G-25), RPT events — no agent, no metric, no watch surface | Index inclusion is a *flow* event of the same nature as lock-up supply (the plan's core thesis lens) — passive demand is the mirror image of unlock supply, and the plan models only the supply side | Add an `IndexInclusionAgent`/watch metric (criteria: seasoning rules, float thresholds — float % already computed in W10); route 8-K forms through the existing poller (already in `watched_forms`) into classified events |
| BS-6 | FWP content classification absent (terms-bearing vs marketing) | A price-revision FWP would be processed identically to a CFO interview transcript | Add a lightweight classifier step in `fwp_ingest.py`: flag FWPs containing $ figures/share counts for human review |
| BS-7 | Gate-flip rehearsal never performed | First real flip of `FINAL_PROSPECTUS_PENDING` will be done under time pressure, untested | Dry-run the flip on a branch: simulate a 424B4, run the full pipeline, verify downstream effects |

---

## 6. Risk register

| Risk | Assessment | Mitigation |
|------|------------|------------|
| **Single-maintainer bus factor** | All judgment, gate flips, and runtime operation depend on one person; pricing week coincides with whatever else is on their calendar. Receipts show zero activity 6/5–6/10 — the bus factor is already *observable* | Cron-based automation (BS-1) is the cheapest bus-factor reduction; document the 424B4 runbook (BS-3) so any competent contributor could execute it; consider a second maintainer with merge rights |
| **EDGAR rate limits / fair access** | SEC guidance: ≤10 req/s, declared User-Agent. Current code honors UA via `SPACX_SEC_USER_AGENT`. Risk rises if cron + runtime + manual checks stack up, or if a public fork hammers the feed with the repo's identity string | Keep polling ≥ minutes-scale intervals; cache submissions JSON; document rate policy in `runtime/README.md`; never embed a real contact email in public CI logs |
| **Public repo invites scrutiny of claims** | Now public (since 2026-06-05): (a) the hash-retention gap (§4, grade D) is a *visible* policy-vs-practice contradiction; (b) stale LISTING_STATUS could be quoted as the repo "saying" 424B4 is pending after it files; (c) approved-wording discipline ("proposed symbol") must survive the excitement of listing day; (d) cached SEC HTML redistribution caveats now apply for real | Fix retention first (it's also the W1 RWA deliverable); make freshness automatic, not manual; pre-write listing-day language updates now, while calm; keep the "not investment advice / not retail research" posture on every new artifact including this one |
| **Anchor obsolescence at pricing** | $135 anchor permeates baselines, trigger prices, valuation metrics | BS-3 runbook; grep-able anchor key (`IPO_issue_anchor_135`) makes the blast radius enumerable — good prior design |

---

## 7. Phase 3 recommendation — listing-day readiness (next 48h, then 2 weeks)

**Immediate (before 2026-06-11 US market open):**

1. **Sync LISTING_STATUS.md** — record the four new FWPs; reset `last_sec_check_date` (this audit's EDGAR pull is the evidence).
2. **Backfill the evidence cache** — create `cache/fwp/`, download all six FWPs + three S-1 documents, write `manifest.json` with real SHA-256 values. Closes the CFA V(C) grade-D finding and delivers RWA W1 in one move.
3. **Add CI cron** (every 2–4h) running `check_sec_feed_sync.py`; failure → loud signal (issue/notification).
4. **Write the 424B4-day runbook** (BS-3): extraction fields, files to touch, blocker-flip criteria, postponement branch.

**Listing window (6/11–6/12):**

5. On 424B4: execute runbook — flip `FINAL_PROSPECTUS_PENDING`, set lock-up day-0, recompute the $-trigger (130% × final price), re-anchor valuation metrics, update approved wording only after first-trade confirmation.
6. **Capture day-1 market data manually** if no feed exists yet (OHLCV + source + timestamp) — the lock-up price-trigger clock starts immediately.

**Phase 3 proper (2 weeks):**

7. Market-data lane: `MarketDataPacket` schema, B-tier source, daily ingestion feeding W02/W10/valuation metrics (BS-2).
8. Earnings-calendar metric + 8-K event routing (BS-4, BS-5 first half).
9. FWP/filing classifier (BS-6) and gate-flip dry-run on a branch (BS-7).
10. Defer: 10-Q/XBRL parser (Phase 3.5, before ~Aug 2026 first earnings); index-inclusion agent (post-listing, pre-seasoning-window).

---

## Appendix — audit method

- Live EDGAR pull: `data.sec.gov/submissions/CIK0001181412.json` (2026-06-10, declared UA).
- Repo state: commit `7cb5f1a` (main, clean tree); test suite 65 passed.
- Verification runs: `scripts/check_sec_feed_sync.py` → `status: fail / undocumented_filings` (4 FWPs); filesystem checks for `cache/`, hash values (`[a-f0-9]{64}` grep: zero matches outside cached SEC HTML).
- This document contains facts (tables, accession numbers, file/dir existence) separated from opinions (scores, rankings, recommendations) per [CFA_RESEARCH_POLICY.md](../CFA_RESEARCH_POLICY.md) §1.
