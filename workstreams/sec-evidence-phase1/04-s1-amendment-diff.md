# Table 4 — S-1 Amendment Diff Audit

**Compared filings:**

| Version | Filed | Accession (index) | Main document |
|---------|-------|-------------------|---------------|
| Form S-1 | 2026-05-20 | 0001628280-26-036936 | `spaceexplorationtechnologi.htm` |
| Form S-1/A #1 | 2026-06-01 | 0001628280-26-039276 | `spaceexplorationtechnologi.htm` |
| Form S-1/A #2 | 2026-06-03 | 0001628280-26-040364 | `spaceexplorationtechnologib.htm` |

**Method:** Plain-text extraction from SEC HTML (machine compare of key terms + manual read of cover, Anthropic, offering blocks).

---

| Topic | S-1 (May 20) | S-1/A #1 (Jun 1) | S-1/A #2 (Jun 3) |
|-------|--------------|------------------|------------------|
| **Offering price** | Cover: **“between $ and $ per share”** (range blank) | Same **blank range** on cover | Cover: **$135.00 per share** (fixed expected price); net proceeds math uses **$135.00** |
| **Primary share count** | Cover: **“We are offering shares”** (count blank) | Same (count blank) | **555,555,555** Class A shares stated on cover and *The Offering* |
| **Greenshoe / total** | Not quantified on cover | Not quantified on cover | **83,333,333** option; **638,888,888** total if full exercise |
| **Net proceeds** | Not stated with fixed price | Not stated with fixed price | **~$74.4B** base / **~$85.7B** full greenshoe (at $135) |
| **Anthropic — economics** | **$1.25B/month through May 2029**; ramp reduced fee May–Jun 2026 | Same | Same |
| **Anthropic — GPU scale** | **Not disclosed** | **~325,000 NVIDIA GPUs** + infrastructure detail added | Retained (same as A#1) |
| **Anthropic — termination** | **90 days’ notice** (no “initial three-month” carveout in extracted text) | **After initial three-month period**, then **90 days’ notice** | Same as A#1 |
| **Anthropic — wording** | “monetize **unused** compute capacity” | “monetize **a portion of** compute capacity” + dual-use language | Same as A#1 |
| **Lock-up / resale** | Timed release framework present (evolved in later pages) | **7.8B** share >1-year restriction language appears | Full staged schedule + **extended lock-up** tranches through **day 366**; Musk **no early release**; **60%** post-IPO vs **>63%** pre-IPO (different denominators) |
| **Governance / voting** | Dual-class; Musk control disclosed; **82.4%** not on cover in same form | Similar; controlled company | **82.4%** Musk voting on cover; **11.5% / 88.5%** Class A/B split post-IPO in *The Offering* |
| **Nasdaq Texas entity name** | “Nasdaq Texas, **Inc.**” on cover | “Nasdaq Texas, **LLC**” | “Nasdaq Texas, **LLC**” |
| **Material new risks** | Baseline risk factor set | Largely same structure; Anthropic/GPU detail in business | No wholesale new risk *category* identified via diff counters; AI/customer credit themes reinforced |
| **Financial restatements** | “Restate” ~28 hits; material weakness ~5 | ~29 / ~5 | ~29 / ~5 — **no amendment-driven restatement event flagged** in diff |

---

## Interpretation (audit notes)

1. **Biggest economic disclosure jump:** S-1/A #2 fixes **$135** and **555.6M share count** — converts a placeholder-range IPO into a **fixed-price mega offering** narrative.
2. **Biggest AI disclosure jump:** S-1/A #1 adds **Anthropic GPU scale** and **three-month termination carveout** vs original S-1.
3. **S-1 → S-1/A #1** is primarily **refinement** (Anthropic/COLOSSUS detail), not price/size finalization.
4. **S-1/A #1 → S-1/A #2** is **pricing and sizing** finalization in the registration statement (still subject to 424B4).

---

## 424B4 status

| Document | Status |
|----------|--------|
| Form **424B4** (final prospectus) | **Pending** — CIK 0001181412 EDGAR feed (checked **2026-06-04**) shows only S-1 / S-1/A filings; no 424B4 |
