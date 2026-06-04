# Data provenance

**Not legal advice.** This notice describes how SPACX handles third-party data in the repository.

Related: [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md) · [LISTING_STATUS.md](./LISTING_STATUS.md)

---

## SEC EDGAR HTML cache

| Item | Detail |
|------|--------|
| **Location** | `workstreams/sec-evidence-phase1/s1*.htm` (and future filing caches) |
| **Source** | U.S. Securities and Exchange Commission EDGAR public filings |
| **Purpose** | Reproducible evidence extraction and audit replay |
| **Modification** | Do not edit cached HTML except to add a new filing snapshot from EDGAR |

### Redistribution notice

Cached SEC documents are **copies of publicly available government filings**. Redistribution of these files (e.g., in a fork, mirror, or export bundle) may implicate:

- SEC and issuer **copyright and fair-use** considerations
- Your obligation to **not misrepresent** edited or partial copies as official filings

**SPACX policy:** Treat cached HTML as **research evidence attachments**, not a republishing service. When sharing externally, prefer **EDGAR accession links** plus local SHA-256 verification rather than bulk redistribution.

---

## SHA-256 verification

Ingest and seal paths record content hashes:

1. Compute SHA-256 of the cached file bytes.
2. Store hash in `SourceRecord` / `EvidencePacket` metadata (`plugin/schemas/`).
3. On mismatch, halt thesis updates and open `hash_mismatch_investigation`.

Example (local check):

```bash
shasum -a 256 workstreams/sec-evidence-phase1/s1a2-main.htm
```

Agent sealing: `evidence.seal_evidence()` via `plugin/api/evidence.py`.

---

## Derived tables and registry

Markdown tables under `workstreams/` and entries in `plugin/metrics/registry.yaml` are **derived works** from SEC sources. They must:

- Cite filing form, date, and section
- Mark **424B4-pending** fields as TBD
- Not upgrade **proposed symbol SPCX** to listed status without [LISTING_STATUS.md](./LISTING_STATUS.md) update

---

## Third-party and chain data (pre-layer)

On-chain and RWA lane data (`plugin/rwa/`, OnchainRWAAgent) is **Grade B/C** unless tied to a primary filing claim. See [RWA_WEB3_STRATEGY.md](./RWA_WEB3_STRATEGY.md).

---

## Disclaimer

This document does **not** constitute legal advice on copyright, securities law, or data licensing. Consult qualified counsel before commercial redistribution or subscriber-facing research products.
