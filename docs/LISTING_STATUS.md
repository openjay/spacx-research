# SPCX listing status

**Last updated:** 2026-06-05 · **Not legal advice**

---

## Current status

| Item | Status |
|------|--------|
| **Proposed / expected listing symbol** | **SPCX** (per Form S-1/A #2, filed 2026-06-03) |
| **Issuer** | Space Exploration Technologies Corp. (CIK 0001181412) |
| **Latest EDGAR filings checked** | 2026-06-04 **FWP** accessions `0001628280-26-040874` and `0001628280-26-040610`; FWP is not a final prospectus |
| **Form 424B4 (final prospectus)** | **Not filed** — final price, underwriting spread, and listing date remain **TBD** |
| **First trading confirmation** | **Not occurred** — no exchange listing or first trade has been confirmed in this repository |
| **Repository posture** | Pre-listing research only; default agent mode `OBSERVE_ONLY` |

Until **Form 424B4** is filed on EDGAR **and** first trading is confirmed by an exchange or regulatory primary source, SPACX documentation and agents must **not** describe SPCX as a **listed**, **trading**, or **publicly traded** security.

The 2026-06-04 FWPs are SEC-filed offering communications under Rule 433. They can be ingested as filing events for monitoring, but they do **not** clear `FINAL_PROSPECTUS_PENDING`, `LOCKUP_DAY0_UNKNOWN`, or `FIRST_EARNINGS_PENDING`.

---

## Approved wording

Use:

- **proposed / expected listing symbol SPCX**
- **anticipated listing on Nasdaq** (when citing S-1/A language)
- **pending Form 424B4 and first trading confirmation**

Avoid:

- “listed ticker SPCX”
- “listed equity SPCX”
- “publicly traded SPCX” (until post-listing)
- Chinese phrasing that implies **已上市** (already listed)

---

## Evidence anchor

Phase 1 SEC extraction and integrated audit:

- [workstreams/sec-evidence-phase1/01-offering-terms.md](../workstreams/sec-evidence-phase1/01-offering-terms.md)
- [workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md](../workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)

---

## When to update this page

1. **424B4 filed** — update final price, share count, and expected listing date from the pricing prospectus.
2. **First trade confirmed** — record exchange, date, and opening print; revise repository language from “proposed symbol” to “listed symbol” only after primary confirmation.
3. **Amendments / FWPs / 8-Ks** — material filing changes to symbol, exchange, offering communications, or retail-offer surfaces must be reflected here and in `plugin/metrics/registry.yaml` blockers where applicable.

Related: [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md) · [COMPLIANCE.md](./COMPLIANCE.md)
