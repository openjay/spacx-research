# Track D — Integrated Audit Opinion (Phase 1 Synthesis)

**Lead Synthesis Auditor:** Track D  
**Date:** 2026-06-04  
**Scope limitation:** No Form 424B4 on file; reliance on registrant's Form S-1/A Amendment No. 2 (filed 2026-06-03). This is **not** a statutory audit opinion under PCAOB or ISA standards.  
**Inputs:** Track A (`A-segment-financial-audit.md`), Track B (`B-offering-governance-audit.md`, `B-lock-up-schedule.md`), Track C (`C-risk-disclosure-audit.md`); direct re-read of `s1a2-main.htm` for critical offering and KPI anchors.

---

## 中文执行摘要（Jay）

### 总体结论：**有条件通过（Pass with Exceptions）**

Phase 1 研究包在 **S-1/A #2** 层面与 SEC 主文件**高度一致**。核心发行数字（**555,555,555 股 × $135**、超额配售选择权（greenshoe）**83,333,333** 股、净募资 **~$744 亿 / ~$857 亿**、马斯克投票权 **~82.4%**）经 Track B 与 Track D 独立复核**全部验证**。分部财务数字在申报文件内部**零差异勾稽**（Track A），未发现捏造或算术错误。

**例外事项（必须在 Phase 2 前处理）：**

1. **424B4 尚未申报** — 最终发行价、承销折扣、上市日仍为「预期」而非定价事实。  
2. ~~**Phase 1 工作底稿实质性遗漏（A-001）**~~ — `02-segment-financials.md` 已回写 Note F-23 分部收入；`05-master-evidence-tables.md` 同步。  
3. ~~**风险映射不完整**~~ — `03-risk-metrics-map.md` 已按 Track C 扩展（监管/供应链/ICFR/F-63 脚注/12 项指标）。  
4. **发行条款文档需澄清** — 净募资与毛额之间 **~$6 亿** 隐含费用主要为未填写的承销折扣，不等于 **$55M** 发行费用（Track B）。

### 修正统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **Corrected（已在本轮主表更正）** | **4** | A-001～A-004（1 实质 + 3 非实质） |
| **Confirmed（经三轨验证）** | **47+** | 发行数学、Anthropic 条款、锁定期时间表、KPI 等 |
| **Unverified（待 424B4）** | **5** | 最终价、承销费率、上市日、最终股数确认、最终风险因素修订 |
| **Material gap（披露/研究缺口）** | **8** | 见英文附录 §4 |

### CFA 研究结论（证据驱动，非价格推荐）

| 情景 | 核心论据（仅 SEC 证据） |
|------|-------------------------|
| **Bull** | Connectivity 分部 Adj. EBITDA 利润率 **~64%**（Q1 2026）；Starlink **10.3M** 用户、FY2025 收入 **+49.8%**；Anthropic **$12.5B/年** 合同 run-rate（若 ramp 完成）；IPO 募资 **~$744B** 净额极大增强 AI/发射/星座 Capex 能力。 |
| **Base** | 固定 **$135** 预设均衡价 + **分阶段锁定期**（180 天起释放，马斯克 **366 天** 无提前释放）→ 流通供给路径比首日 pop 更重要；AI Q1 Capex/Revenue **~9.4×**、经营亏损 **$(2,469)M** 吞噬现金；**$20B** 过桥贷款 **2027-09-02** 到期。 |
| **Bear** | 治理：**受控公司 + ~82.4% 投票权**；Anthropic **90 天通知** 终止（初始 3 月后）；AI 客户信用风险；无发射/卫星保险；Customer A 占 consolidated revenue **~21–25%**（FY2023–2025）；Starship 入轨若延迟则 V3 星座部署受阻。 |

### Phase 2 就绪度：**否（有阻塞项）**

| 阻塞项 | 负责动作 |
|--------|----------|
| 424B4 未出 | 定价日重新拉 EDGAR，更新 Table 1 最终列 |
| ~~Phase 1 底稿未同步~~ | `01`/`02`/`03` 已回写；canonical：`05-master-evidence-tables.md` |
| 跟踪表未建 | 按 Track C §4 阈值建立 Phase 2 监控表（见 §6 必做清单） |
| 锁定期锚日未定 | 以 prospectus/定价日为 Day 0 重算释放日历 |

---

## English Technical Appendix

### 1. Scope & reliance

| Item | Detail |
|------|--------|
| Registrant | SPACE EXPLORATION TECHNOLOGIES CORP (CIK 0001181412) |
| Primary document | Form S-1/A #2, accession `0001628280-26-040364`, filed 2026-06-03 |
| Local cache | `s1a2-main.htm` (plus S-1, S-1/A #1 for diff) |
| Out of scope | 424B4, media price targets, non-EDGAR social/video sources |
| Track completion | A ✓ B ✓ C ✓ (polled 2026-06-04; all files present) |

This memorandum synthesizes independent workpapers A/B/C, deduplicates findings, and classifies each item per the Phase 1 taxonomy below.

### 2. Classification taxonomy (merged register)

| ID | Class | Source | Finding | Action taken |
|----|-------|--------|---------|--------------|
| A-001 | **Corrected** | A | FY2024/FY2023 segment revenue mislabeled "not disclosed" in `02-segment-financials.md` | Corrected in `05-master-evidence-tables.md` §2.1 from Note 3 (F-23) |
| A-002 | **Corrected** | A | Q1 2025 segment revenue omitted | Added in master Table 2.1 |
| A-003 | **Corrected** | A | Consolidated reference truncated to Q1 2026 / FY2025 | Expanded in master Table 2.5 |
| A-004 | **Corrected** | A | AI nameplate GW shown as 1.0 vs filing integer 1 | Normalized in master Table 2.4 |
| B-001 | **Confirmed** | B | 555,555,555 × $135 = $74,999,999,925 gross | Verified |
| B-002 | **Confirmed** | B | Greenshoe 83,333,333 (15%); total 638,888,888 | Verified |
| B-003 | **Confirmed** | B | Net proceeds ~$74.4B / ~$85.7B | Consistent with Use of Proceeds |
| B-004 | **Corrected** | B | $55M offering expenses conflated with total fee drag | Clarified: ~$600M implied deduction = primarily blank underwriting spread |
| B-005 | **Corrected** | B | Directed share count absent | Added ~27,777,778 shares (5% of primary) |
| B-006 | **Confirmed** | B | Lock-up staged schedule + Musk 366d no early release | Verified vs `B-lock-up-schedule.md` |
| B-007 | **Unverified** | B/D | Final underwriting discount (% and $) | Pending 424B4 |
| B-008 | **Unverified** | B/D | Listing / first trade date | Pending 424B4 |
| B-009 | **Material gap** | B | 82.4% (voting, *The Offering*) vs 84.4% (*Security Ownership*) | Label metric in models; not a filing error |
| B-010 | **Unverified** | B/D | Form 424B4 | **Not filed** on EDGAR as of 2026-06-05; 2026-06-04 FWPs do not clear this gap |
| C-001 | **Confirmed** | C | Anthropic $1.25B/mo through May 2029; ramp; 90d termination after 3mo | PASS (narrative) |
| C-002 | **Material gap** | C | F-63 footnote omits $ quantum, 3-month carve-out, GPU count | Monitor narrative; footnote is incomplete |
| C-003 | **Confirmed** | C | xAI = merger (Feb 2, 2026), not third-party cloud contract | N/A for contract verification |
| C-004 | **Material gap** | C | `03-risk-metrics-map.md` under-maps regulatory, supply chain, debt, insurance | Expand before Phase 2 (see §6) |
| C-005 | **Corrected** | C | "Material weakness count stable" wording | Rephrase: qualitative ICFR disclosure only |
| C-006 | **Confirmed** | A/C | Segment sums = consolidated (revenue, op income, Adj. EBITDA) 0.0% variance | All five periods |
| C-007 | **Material gap** | A | Customer A = 20.9% / 24.2% / 25.2% consolidated revenue (FY2025–2023) | Add to Phase 2 concentration watch |
| C-008 | **Material gap** | C | $20B bridge (matures Sep 2, 2027); 3.75:1 leverage covenant | Add to Phase 2 debt watch |
| C-009 | **Confirmed** | A/B/C | No segment financial restatement across S-1 → S-1/A #2 | Amendment stability |
| C-010 | **Material gap** | A | Segment gross margin, segment FCF not disclosed | Filing-level gap |

**Summary counts:** Corrected **6** | Confirmed **47+** line items | Unverified **5** | Material gap **8**

### 3. Integrated assertion summary (auditor-style)

| Financial statement area | Occurrence | Completeness | Accuracy | Presentation |
|--------------------------|------------|--------------|----------|--------------|
| Offering terms (S-1/A #2) | Pass | Pass* | Pass | Pass — *final price pending 424B4 |
| Segment KPI table | Pass | Pass | Pass | Pass |
| Note 3 segment revenue | Pass | **Fail** (workpaper) → Corrected in master tables | Pass | Pass |
| Cap table / voting | Pass | Pass | Pass | Minor metric labeling |
| Risk factor mapping | Pass | **Fail** (workpaper breadth) | Pass | Expand Phase 2 |
| Anthropic contract | Pass | Partial (footnote) | Pass | Pass |

**Overall:** Registrant disclosure is internally consistent for tested numerics. Research workpapers required **6 corrections/clarifications**; **no critical math errors** on deal terms or segment figures traced to source.

### 4. Material gaps (filing + research)

1. **424B4 absent** — cannot opine on final economics or listing timeline.  
2. **Underwriting spread blank** — ~$600M base-case gap to net proceeds unexplained in preliminary table.  
3. **Use of proceeds** — no % allocation across AI / launch / satellites.  
4. **Segment gross margin & FCF** — not segment-disclosed.  
5. **Customer concentration** — Customer A ~21–25% consolidated revenue; not in Phase 1 tables.  
6. **Debt wall** — $20B bridge Sep 2027; covenant 3.75:1 (4.25:1 post-qualifying acquisition).  
7. **F-63 vs narrative** — Anthropic footnote less granular than Prospectus Summary.  
8. **Risk map breadth** — 26 themes in Track C vs ~16 rows in `03-risk-metrics-map.md`.

### 5. Amendment audit trail (integrated)

| Event | Date | Material change |
|-------|------|-----------------|
| S-1 | 2026-05-20 | Placeholder price/count; Anthropic economics without GPU scale |
| S-1/A #1 | 2026-06-01 | +325k GPUs; 3-month termination carve-out; "portion of" compute wording |
| S-1/A #2 | 2026-06-03 | **$135** fixed price; **555.6M** shares; net proceeds quantified; full lock-up schedule |

Segment financial numbers: **unchanged** across all three filings (Track A).

### 6. Required actions before Phase 2 tracking tables

| Priority | Action | Owner | Blocker? |
|----------|--------|-------|----------|
| P0 | Monitor EDGAR for **424B4**; on filing, diff vs S-1/A #2 and update Table 1 final column | Research | **Yes** — final price/fees |
| P0 | Set **prospectus date = Day 0** for lock-up calendar (`B-lock-up-schedule.md`) | Research | **Yes** — until priced |
| P1 | Backfill `02-segment-financials.md` from `05-master-evidence-tables.md` §2 | Research | No |
| P1 | Update `01-offering-terms.md` with B-004, B-005 clarifications | Research | No |
| P1 | Expand `03-risk-metrics-map.md` to 26 themes + debt/insurance/regulatory (Track C §3) | Research | No |
| P1 | Fix material-weakness wording in `03-risk-metrics-map.md` | Research | No |
| P2 | Build Phase 2 tracking workbook from Track C §4 (12 metrics + thresholds) | Research | No |
| P2 | Add Customer A concentration + bridge maturity to watch list | Research | No |
| P2 | Model float path using corrected lock-up table + directed shares (~27.8M, no lock-up) | Research | No |
| P3 | Reconcile 82.4% vs 84.4% Musk voting in cap-table models | Research | No |

### 7. Readiness gate for Phase 2

| Gate | Status |
|------|--------|
| Master evidence tables published | **Yes** — `05-master-evidence-tables.md` |
| A/B/C merged & classified | **Yes** — this document |
| Phase 1 workpapers synced to corrections | **Yes** (2026-06-04 follow-up) |
| 424B4 pricing facts | **No** |
| Lock-up anchor date | **No** |
| Phase 2 metric thresholds loaded | **No** — spec ready in Track C §4 |

**Phase 2 tracking tables:** **Not ready** until P0 items clear and P1 backfill completes. Qualitative monitoring may begin using corrected master tables and Track C thresholds immediately.

---

## Sign-off (Track D)

| Field | Value |
|-------|-------|
| **Overall conclusion** | **Pass with exceptions** |
| **Corrections applied (master tables)** | **6** (4 segment + 2 offering/clarification) |
| **Critical failures** | **0** (no wrong deal math; no fabricated SEC numbers) |
| **Phase 2 ready** | **No** — blockers: 424B4, prospectus date; P1 backfill **done** |
| **Next deliverable** | Phase 2 tracking workbook after P0/P1 checklist |

*End of integrated audit opinion.*
