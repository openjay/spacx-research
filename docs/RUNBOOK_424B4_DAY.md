# 424B4-day runbook / 424B4 当日操作手册

**Scope:** What to do, in order, when Form 424B4 (final prospectus) for Space Exploration Technologies Corp. (CIK `0001181412`) appears on EDGAR — plus contingency branches and day-1 trading notes.
**Context:** Expected pricing 2026-06-11; expected first trade 2026-06-12 (proposed symbol **SPCX**, Nasdaq). Current A-tier anchor: **$135.00/share**, **555.6M** shares offered, ~$1.75T implied cap (S-1/A #2).
**Trigger:** `sec-cron.yml` drift issue, `scripts/check_sec_feed_sync.py` failure `424b4_filed_doc_pending`, or manual EDGAR check.
**Not investment advice. Not legal advice.**

Related: [LISTING_STATUS.md](./LISTING_STATUS.md) · [B-lock-up-schedule.md](../workstreams/sec-evidence-phase1/audit/B-lock-up-schedule.md) · [price_anchors.yaml](../plugin/valuation/price_anchors.yaml) · [registry.yaml](../plugin/metrics/registry.yaml) · [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md)

---

## English

### Step 0 — Confirm the filing (5 min)

1. Pull `https://data.sec.gov/submissions/CIK0001181412.json` with a declared User-Agent (`SPACX_SEC_USER_AGENT`).
2. Confirm form type is exactly **424B4** (not another FWP, not 424B3/424B5). Record accession number, filing date, primary document name.
3. If the form is **8-K**, **RW**, or a price-revision **S-1/A**/**FWP** instead → jump to [Contingencies](#contingencies).

### Step 1 — Ingest + hash (chain of custody first)

1. Download the primary HTML from `https://www.sec.gov/Archives/edgar/data/1181412/<accession-no-dashes>/<primary_document>`.
2. Cache to `workstreams/sec-evidence-phase1/cache/` (sibling of `fwp/`, e.g. `cache/424b4/`) using the dated naming convention `<filing_date>_<accession>_<primary_doc>`.
3. Compute SHA-256 of the raw bytes; append an entry (`form: "424B4"`, accession, date, `cache_path`, `sha256`, `bytes`, `ingested_at`) to `workstreams/sec-evidence-phase1/cache/manifest.json` (same entry shape as the FWP entries written by `runtime/fwp_ingest.py`).
4. Do nothing else until the hash is recorded — every downstream number must cite this artifact.

### Step 2 — Extract final terms and diff vs expectations

From the 424B4 cover page and "The Offering" section, extract and diff against the S-1/A #2 anchor:

| Field | Expected (S-1/A #2) | Final (424B4) |
|-------|---------------------|----------------|
| Price per share | $135.00 | __ |
| Shares offered | 555,600,000 | __ |
| Over-allotment (greenshoe) | record | __ |
| Underwriting discount / spread | TBD | __ |
| Total shares outstanding post-IPO | 13,075,865,175 | __ |
| Prospectus date (= lock-up Day 0 anchor) | TBD | __ |
| Expected first trade date | 2026-06-12 | __ |

If price ≠ $135 or shares ≠ 555.6M → also execute the [re-anchor procedure](#c-1--final-price--135-re-anchor-procedure).

### Step 3 — Update LISTING_STATUS.md

1. Frontmatter: add the 424B4 entry to `latest_known_filings`; set `form_424b4_status: filed`; set `form_424b4_update_flag: true`; set `last_sec_check_date` to today.
2. Body: replace "**Not filed**" language in the 424B4 row with the final price, share count, and expected listing date (cite accession). Keep **proposed symbol** wording — do NOT switch to "listed" until first trade is confirmed by exchange/primary source.
3. Run `python scripts/check_sec_feed_sync.py` → must PASS.

### Step 4 — Re-anchor `price_anchors.yaml`

Update `ipo_issue_anchor` in `plugin/valuation/price_anchors.yaml`:

- `filing: Form 424B4`, `filing_date`, `sec_citation: Cover; The Offering`
- `price_usd_per_share`, `shares_count`, recomputed `implied_market_cap_usd_bn` / `enterprise_value_usd_bn`
- Remove `FINAL_PROSPECTUS_PENDING` from `conflict_flags`; update `as_of`
- In `fomo_trading_band` notes: recompute the lock-up pop trigger reference (130% × final price; $175.50 only if price is exactly $135)

### Step 5 — Lock-up Day 0 + schedule regeneration

1. Day 0 = **prospectus date** (424B4 date). Record it at the top of `workstreams/sec-evidence-phase1/audit/B-lock-up-schedule.md`.
2. Regenerate concrete calendar dates for days **70 / 90 / 91 / 105 / 120 / 135 / 180**, extended-tranche days **280 / 340 / 366**, and Musk day **366** (earnings-gated tranches stay TBD until earnings dates are announced).
3. Recompute the +10% tranche price trigger: **130% × final IPO price** (replaces $175.50 if price changed).

### Step 6 — Flip blockers in registry baselines

In `plugin/metrics/registry.yaml`:

1. `FINAL_PROSPECTUS_PENDING` → `active: false` (note 424B4 accession in description/citation).
2. `LOCKUP_DAY0_UNKNOWN` → `active: false` (note Day 0 date).
3. `FIRST_EARNINGS_PENDING` stays **active**.
4. If price changed, update every baseline keyed `baseline_period: IPO_issue_anchor_135` (see C-1).

### Step 7 — Regenerate snapshots, verify, commit

```bash
PYTHONPATH=. python3 plugin/valuation/export_snapshots.py
pytest -q                                  # all tests green
python3 -m compileall -q plugin runtime scripts
python3 scripts/check_sec_feed_sync.py     # PASS
git add -A && git commit -m "feat(sec): 424B4 final terms"
```

Push to `main`; confirm CI (including `sec-feed-sync` job) is green; close the "SEC filing drift detected" issue if open.

### Contingencies

#### C-1 — Final price ≠ $135 (re-anchor procedure)

The blast radius is enumerable by design: `grep -rn "IPO_issue_anchor_135\|135.0\|175.50" plugin/ workstreams/`.

1. `price_anchors.yaml` → `ipo_issue_anchor` per Step 4.
2. `registry.yaml` valuation baselines (all `baseline_period: IPO_issue_anchor_135` → rename to `IPO_issue_anchor_<final>`):
   - `IMPLIED_MARKET_CAP_USD` = final price × final post-IPO share count
   - `EV_TO_REVENUE_FY25`, `EV_TO_ADJ_EBITDA_FY25` = recompute from new implied EV over unchanged FY25 SEC denominators
   - `PRICE_VS_DCF_ANCHOR_PCT` = (final price / 60.0 − 1) × 100
3. Lock-up price trigger = 130% × final price (`B-lock-up-schedule.md` + any registry/anchor notes referencing $175.50).
4. The C-tier DCF ($60) and FOMO band ($185–300) anchors do not move — they are external/observational; only re-evaluate `BELOW_IPO_ISSUE_ANCHOR`-style relative flags.

#### C-2 — Upsize / downsize (share count change)

- Recompute post-IPO shares outstanding, implied cap, and float-dependent metrics (W10 float-at-gates denominators).
- Lock-up tranche share maximums in `B-lock-up-schedule.md` scale with the pools defined in the 424B4 — re-extract the "Shares Eligible for Future Sale" table rather than scaling the old numbers.
- Directed share program: 5% of *final* offered shares.

#### C-3 — Postponement (no 424B4; pricing slips)

- **Keep all three blockers active.** Do not touch baselines.
- Log the event: update `LISTING_STATUS.md` body ("pricing postponed per <source, date>" — A/B-tier source only), bump `last_sec_check_date`.
- Watch for a fresh S-1/A or FWP carrying revised timing/range; ingest + hash like any filing.
- `sec-cron.yml` keeps polling; no schedule change needed.

#### C-4 — Withdrawal (Form RW)

- Ingest + hash the RW filing. Update `LISTING_STATUS.md`: offering withdrawn; symbol language becomes historical ("was proposed").
- Blockers stay active permanently (or repo enters archive mode); valuation metrics flagged inactive — **never** delete the evidence base.
- Open a maintainer issue to decide repo disposition (archive vs pivot to next filing window).

### Day-1 trading notes (2026-06-12 expected)

- **Known gap (Phase 3):** there is **no market-data lane** — W02 (first-day pop), W10 (float at gates), `IMPLIED_MARKET_CAP_USD` live, and the 130% price-trigger tracking have no automated source.
- **Interim manual price capture procedure** (until `MarketDataPacket` lane ships):
  1. After Nasdaq close, record OHLCV + official close from a reputable consolidated-tape source (exchange site, major data vendor).
  2. Save as a dated CSV row under `runtime/data/` (or a committed `workstreams/market-data-interim/` CSV) with columns: `date, open, high, low, close, volume, source, captured_at_utc, captured_by`.
  3. The price-trigger clock (5-of-10 sessions ≥ 130% × IPO price, ending at First Earnings Release Date) starts on day 1 — capture **every** session from day 1; gaps cannot be backfilled to A/B-tier standard.
- First-trade confirmation (exchange/primary source) — only then may repo language change from "proposed symbol" to "listed symbol" (see LISTING_STATUS.md approved wording).

---

## 中文

### 第 0 步 — 确认申报（5 分钟）

1. 用声明式 User-Agent（`SPACX_SEC_USER_AGENT`）拉取 `https://data.sec.gov/submissions/CIK0001181412.json`。
2. 确认表格类型确为 **424B4**（不是又一份 FWP，也不是 424B3/424B5）。记录 accession 号、申报日期、主文档文件名。
3. 如果出现的是 **8-K**、**RW** 或改价的 **S-1/A**/**FWP** → 跳到[应急分支](#应急分支)。

### 第 1 步 — 抓取 + 哈希（先固化证据链）

1. 从 `https://www.sec.gov/Archives/edgar/data/1181412/<accession去横线>/<主文档>` 下载主 HTML。
2. 缓存到 `workstreams/sec-evidence-phase1/cache/`（与 `fwp/` 平级，如 `cache/424b4/`），命名格式 `<申报日>_<accession>_<主文档名>`。
3. 对原始字节计算 SHA-256，按 FWP 条目同样的结构追加进 `cache/manifest.json`（`form: "424B4"`、accession、日期、`cache_path`、`sha256`、`bytes`、`ingested_at`）。
4. 哈希未入账前不做任何后续操作——所有下游数字必须引用此证据。

### 第 2 步 — 提取最终条款并与预期对照

从 424B4 封面与 “The Offering” 提取并对照 S-1/A #2 锚点：最终价格（预期 $135.00）、发行股数（预期 555.6M）、超额配售选择权（greenshoe）、承销价差、IPO 后总股本（预期 13,075,865,175）、招股书日期（= 解禁 Day 0 锚）、预计首日交易日（2026-06-12）。价格 ≠ $135 或股数 ≠ 555.6M → 同时执行 [C-1 重锚程序](#c-1--最终价--135重锚程序)。

### 第 3 步 — 更新 LISTING_STATUS.md

1. Frontmatter：`latest_known_filings` 加入 424B4 条目；`form_424b4_status: filed`；`form_424b4_update_flag: true`；`last_sec_check_date` 设为当日。
2. 正文：424B4 行的 “**Not filed**” 替换为最终价格、股数、预计上市日（引用 accession）。继续使用 **proposed symbol（拟上市代码）** 措辞——首日交易经交易所/一级来源确认前**不得**改为“已上市”。
3. 运行 `python scripts/check_sec_feed_sync.py` → 必须 PASS。

### 第 4 步 — 重锚 `price_anchors.yaml`

更新 `ipo_issue_anchor`：`filing: Form 424B4`、申报日期、最终每股价格、股数、重新计算的隐含市值/EV；从 `conflict_flags` 移除 `FINAL_PROSPECTUS_PENDING`；更新 `as_of`。`fomo_trading_band` 注释中的解禁触发价改为 130% × 最终价。

### 第 5 步 — 解禁 Day 0 + 日历重算

1. Day 0 = **招股书日期**（424B4 日期），记入 `B-lock-up-schedule.md` 顶部。
2. 重算第 **70/90/91/105/120/135/180** 天、延长档第 **280/340/366** 天、马斯克第 **366** 天的具体日历日期（财报门控档在财报日公布前保持 TBD）。
3. 重算 +10% 档价格触发：**130% × 最终发行价**（价格变了则替换 $175.50）。

### 第 6 步 — 翻转 registry 中的 blocker

`plugin/metrics/registry.yaml`：`FINAL_PROSPECTUS_PENDING` → `active: false`（注明 accession）；`LOCKUP_DAY0_UNKNOWN` → `active: false`（注明 Day 0 日期）；`FIRST_EARNINGS_PENDING` **保持激活**。价格有变则按 C-1 更新所有 `IPO_issue_anchor_135` 基线。

### 第 7 步 — 重导快照、验证、提交

依次运行 `export_snapshots.py`、`pytest -q`、`compileall`、`check_sec_feed_sync.py`（须 PASS），然后提交 `feat(sec): 424B4 final terms` 并推送 `main`；确认 CI 全绿；关闭未结的 “SEC filing drift detected” issue。

### 应急分支

#### C-1 — 最终价 ≠ $135（重锚程序）

影响面可枚举：`grep -rn "IPO_issue_anchor_135\|135.0\|175.50" plugin/ workstreams/`。依次更新：① `price_anchors.yaml` 的 `ipo_issue_anchor`；② `registry.yaml` 所有 `baseline_period: IPO_issue_anchor_135` 基线（隐含市值 = 最终价 × 最终总股本；EV 倍数按新 EV / 不变的 FY25 SEC 分母重算；`PRICE_VS_DCF_ANCHOR_PCT` = (最终价/60 − 1) × 100），并把基线键改名为 `IPO_issue_anchor_<最终价>`；③ 解禁触发价 = 130% × 最终价。C 档 DCF（$60）与 FOMO 区间（$185–300）为外部/观察锚，不动。

#### C-2 — 增发 / 缩发（股数变化）

重算 IPO 后总股本、隐含市值、流通盘相关指标（W10 分母）。解禁各档股数上限须**重新提取** 424B4 的 “Shares Eligible for Future Sale” 表，不要按比例缩放旧数。定向配售 = 最终发行股数的 5%。

#### C-3 — 推迟（无 424B4，定价延期）

**三个 blocker 全部保持激活**，基线不动。在 `LISTING_STATUS.md` 正文记录事件（仅 A/B 档来源），更新 `last_sec_check_date`。关注携带新时间表/价格区间的 S-1/A 或 FWP，照常抓取+哈希。`sec-cron.yml` 持续轮询，无需改频率。

#### C-4 — 撤回（Form RW）

抓取+哈希 RW 文件；`LISTING_STATUS.md` 改为“发行已撤回”，代码措辞改为历史时态。Blocker 永久保持激活（或仓库转归档模式）；估值指标标记失效——**绝不**删除证据底座。开 maintainer issue 决定仓库去向（归档或转向下一申报窗口）。

### 首日交易备注（预计 2026-06-12）

- **已知缺口（Phase 3）：** 仓库**没有行情数据通道**——W02（首日涨幅）、W10（解禁节点流通盘）、实时隐含市值、130% 触发价跟踪均无自动数据源。
- **临时手工采集程序**（`MarketDataPacket` 通道上线前）：纳斯达克收盘后，从可靠的合并报价来源记录 OHLCV + 官方收盘价，按 `date, open, high, low, close, volume, source, captured_at_utc, captured_by` 列存为带日期的 CSV。
- **触发价时钟从第 1 天开始**（First Earnings Release Date 截止的 10 个交易日中 5 日 ≥ 130% × IPO 价）——必须从第 1 天起逐日采集，漏采无法以 A/B 档标准补录。
- 仅在交易所/一级来源确认首日交易后，仓库措辞才能从“拟上市代码”改为“已上市代码”（见 LISTING_STATUS.md 核准措辞表）。
