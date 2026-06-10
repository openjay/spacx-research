# Engineering End-to-End Retrospective — SPACX-Research v0.1.0

**Audit date:** 2026-06-10 · **Track:** ENG (engineering & infrastructure quality)
**Scope:** full git history (40 commits, 2026-06-04 → 2026-06-05), `plugin/`, `runtime/`, `scripts/`, `tests/`, CI, architecture coherence
**Repo:** https://github.com/openjay/spacx-research · tag `v0.1.0` at `7cb5f1a`

---

## 1. Timeline of major milestones

| Date | Commit | Milestone |
|------|--------|-----------|
| 2026-06-04 | `e1e4a6e` | Phase 1 SEC evidence base + audit Tracks A–D published |
| 2026-06-04 | `7e68e2f` | Rebrand to SPACX platform; Phase 1 SEC workstream relocated |
| 2026-06-04 | `edb8c3e` | Eight-agent roles + 24/7 scheduler spec (`plugin/agents/`, `scheduler.yaml`) |
| 2026-06-04 | `ed04125` | Plugin V0 intelligence stack (api, schemas, metrics, models) |
| 2026-06-04 | `4fc492d` | Web3/RWA pre-layer plugin stubs (`plugin/rwa/`) |
| 2026-06-04 | `652d474` | CFA policy, listing status, OSS prep docs |
| 2026-06-04 | `72a29e8` | Runtime V0: worker, EDGAR poll, persistence, health, action packets |
| 2026-06-04 | `5c61e86` | Audit remediation: schema contracts, tests, CI |
| 2026-06-05 | `09ea9a8` | CFA valuation layer: SOTP, price anchors, implied multiples, reverse DCF |
| 2026-06-05 | `d9474ba` | AI-native P0/P1 batch: FWP watch, valuation schema alignment, runtime fixes |
| 2026-06-05 | `3514b1e` | FWP evidence packet + source cache |
| 2026-06-05 | `b270485` | CI SEC feed sync gate for listing status |
| 2026-06-05 | `d8f2850` | MetricSnapshot export + research freshness |
| 2026-06-05 | `a212488` | OSS release-grade gap infrastructure + launch checklist |
| 2026-06-05 | `5be75e1` | Trademark audit, terminology policy, affiliation disclaimers |
| 2026-06-05 | `5082299` | SPACX-Research rename; repo `spacx-research` |
| 2026-06-05 | `160dfa5` | Final launch-gated patches, gitleaks allowlist, brand tests |
| 2026-06-05 | `ebc5f65` → `7cb5f1a` | Public OSS flip; `v0.1.0` tagged at `7cb5f1a` |

**History observation:** 15 of 40 commits (37.5%) are `GITHUB.md` HEAD-pointer churn (`docs: update/point/pin GITHUB.md HEAD`), including self-referential fix-the-fix sequences. The entire project spans ~2 days of wall-clock time.

## 2. Verification results (run 2026-06-10, local Python 3.14.3)

| Check | Command | Result |
|-------|---------|--------|
| Test suite | `pytest -q` | **PASS** — 65 tests, 0 failures (tests/, plugin/tests/, runtime/tests/) |
| Byte-compile | `python -m compileall -q plugin runtime scripts tests` | **PASS** (exit 0) |
| Health gate | `python -m runtime.health` | **PASS** — `ready: true`, `sec_cache_ok: true`, `schema_contract_ok: true`; blockers correctly raised (424B4 pending, lockup day-0 unknown, first earnings pending) |
| Valuation export | `python -m plugin.valuation.export_snapshots --out /tmp/snap.json` | **PASS** — valid JSON dict, 6 top-level keys |
| Tag signature | `git tag -v v0.1.0` | **UNSIGNED** — annotated tag only, no GPG/SSH signature |

Note: local toolchain is Python 3.14.3; CI pins 3.11 only. Everything passes on both, but only 3.11 is continuously verified.

## 3. Strengths (genuinely solid)

1. **Schema-first contracts.** 13 JSON Schemas in `plugin/schemas/` are the single source of truth; `plugin/contracts/` is a real Draft 2020-12 validator (not a stub) with an end-to-end `contract_probe_ok()` probe exercised by tests and `runtime/health.py`. API outputs are validated against schemas in CI.
2. **Honest stub labeling.** Stub code self-identifies (`MONITOR_PHASE = "v0_stub"`, `mode: "prior_stub"`, `ModelPhase.V0`, docstrings naming Phase 2/3 replacements). The codebase rarely pretends to be more than it is.
3. **Clean, consistent Python.** ~5,500 lines, fully type-annotated (`from __future__ import annotations`, modern `X | None` unions), dataclasses, stdlib-first (only `jsonschema` + `PyYAML` runtime deps), small focused modules (largest file 338 lines). Compiles clean on 3.11 and 3.14.
4. **Working runtime kernel.** `runtime/worker.py --once/--loop` → `edgar_poll` (real SEC submissions API with fair-access User-Agent) → SQLite + JSONL persistence with idempotent `init_db`, upserted EDGAR state, audit receipts, and typed action packets. `runtime/health.py` gates on cache, schema contract, and blocker flags.
5. **Supply-chain-aware CI for a 2-day-old project.** gitleaks secret scan, SBOM (CycloneDX), pip lock snapshot, dependency license drift check, and a live SEC feed-vs-docs sync gate that degrades gracefully when the User-Agent secret is absent.
6. **Compliance-as-architecture.** Compliance levels 0–6 with hard V0 = level-2 ceiling (proposals only, no orders) encoded in code paths (`observation_only: true`, `nap_from_blockers`), not just docs.

## 4. Gap register

Severity: **P0** = undermines the product's stated purpose or correctness; **P1** = quality/operational risk; **P2** = hygiene.

| # | Sev | Gap | Evidence |
|---|-----|-----|----------|
| G1 | **P0** | **Runtime is not deployed anywhere.** `worker.py --loop` exists but there is no daemon, cron, systemd/launchd unit, container, or hosted scheduler. The "24/7 world model" in ARCHITECTURE.md runs zero hours per day; scheduler tiers T0–T4 in `plugin/scheduler.yaml` are documentation, not wiring. | `runtime/worker.py`; no Dockerfile/unit files; only workflow is `ci.yml` |
| G2 | **P0** | **Models and chain monitors are stub-math with no real data feeds.** Factor exposure returns hardcoded prior betas (`AI_GROWTH=0.85`, `MKT=1.10`); chain monitors return placeholder rows (`notes="V0 stub — no RPC"`); market/macro lanes have no ingest. Outputs are schema-valid and could be mistaken for live research by downstream agents. | `plugin/models/factor_exposure.py:108-118`, `plugin/rwa/chain_state_monitor.py`, all 5 tiers except `sec_1h` are no-op dispatch in `worker.run_tier` |
| G3 | **P0** | **Persistence unproven at scale.** Single-file SQLite + append-only JSONL with no retention, rotation, vacuuming, concurrency strategy (loop + ad-hoc CLI invocations share one DB file), backup, or migration story. `runtime/data/` is gitignored and machine-local — a disk loss erases the entire audit trail the architecture calls "chain of custody". | `runtime/persistence.py`, `.gitignore` |
| G4 | **P1** | **No lint or type-check in CI.** No ruff/flake8, no mypy/pyright — despite the codebase being fully type-annotated (the annotations are never machine-checked). | `.github/workflows/ci.yml` jobs: secret-scan, test, supply-chain, sec-feed-sync only |
| G5 | **P1** | **No coverage measurement and clear coverage holes.** No `pytest-cov`/coverage gate. Untested modules: `runtime/worker.py`, `runtime/persistence.py`, `runtime/health.py`, `plugin/api/risk.py` (125 lines, only probed indirectly), `plugin/api/thesis.py`, `plugin/valuation/freshness.py` partially. Models have smoke tests only. | `tests/`, `plugin/tests/`, `runtime/tests/` import graph |
| G6 | **P1** | **Single Python version in CI (3.11), no matrix.** Local development runs 3.14.3; `pyproject.toml` claims `>=3.11`. The supported range is asserted but not tested. | `ci.yml:31`, `pyproject.toml` |
| G7 | **P1** | **No integration test of `runtime/edgar_poll` against live EDGAR in CI.** The `sec-feed-sync` job only checks docs/LISTING_STATUS.md drift via `scripts/check_sec_feed_sync.py`, and silently skips when the `SPACX_SEC_USER_AGENT` secret is unset. The actual runtime ingest path (`poll_edgar` → persistence → packets) is never exercised end-to-end anywhere. | `ci.yml:93-109`, `scripts/check_sec_feed_sync.py:33-34` |
| G8 | **P1** | **Release engineering is manual and unsigned.** `v0.1.0` tag has no GPG/SSH signature; release artifacts (`RELEASE_NOTES_v0.1.0.md`, `SHA256SUMS`, `sbom.json`, `requirements-lock.txt`) live in an untracked local `dist/` directory; no release workflow, no GitHub Release automation, no provenance/attestation. | `git tag -v v0.1.0`; `git status` shows `?? dist/` |
| G9 | **P1** | **ARCHITECTURE.md repository map is incomplete.** It omits `runtime/` (the entire execution layer), `plugin/rwa/`, `plugin/contracts/`, `scripts/`, and `tests/`. The layer-stack and lane descriptions are accurate, but a newcomer following the map misses ~40% of the code. | `docs/ARCHITECTURE.md:145-157` |
| G10 | **P2** | **Local directory name `spacx` vs remote `spacx-research`.** Post-rename drift; also a stale legacy `spacx.egg-info/` sits beside `spacx_research.egg-info/` on disk (gitignored but confusing). | `/Users/jay/code/spacx`, `origin` URL |
| G11 | **P2** | **GITHUB.md HEAD-pointer commit churn.** 15/40 commits exist only to update a self-referential commit hash in `GITHUB.md`, twice requiring fix-the-fix commits. The mechanism fights git itself. | `git log --oneline` |
| G12 | **P2** | **CI license jobs are contradictory and discard output.** One step diffs `docs/DEPENDENCY_LICENSES.md` for drift, the next regenerates it in the workspace and throws it away (no commit/artifact); both are `continue-on-error`, so drift never actually gates. | `ci.yml:42-61` |

**Gap counts: P0 × 3 · P1 × 6 · P2 × 3 (12 total)**

### Stub inventory (stub vs production)

| Component | Status |
|-----------|--------|
| `plugin/schemas/` + `plugin/contracts/` | **Production-grade** (validated in CI) |
| `runtime/edgar_poll.py`, `fwp_ingest.py` | **Real** (live SEC API) but not deployed or integration-tested in CI |
| `runtime/persistence.py`, `health.py`, `packets.py`, `worker.py` | **Real** but unscheduled (G1) and lightly tested (G5) |
| `plugin/metrics/threshold_engine.py` | **Real** engine, baselines static JSON |
| `plugin/valuation/*` | **Real** calculators over static YAML anchors (no live prices) |
| `plugin/models/*` (8 models) | **Stub math** — interfaces + V0 placeholder computation, no data feeds (G2) |
| `plugin/rwa/*` (5 modules) | **Explicit stubs** — no RPC/indexer (G2) |
| `plugin/api/*` | **Pass-through stubs** returning schema-valid defaults |
| `plugin/agents/*` (9 roles) | **Spec-only** — YAML + README, no executable agent code |
| Scheduler tiers T0–T4 | **Spec-only** — worker no-ops all tiers except `sec_1h` |

## 5. Next-iteration recommendations (prioritized)

1. **Deploy the runtime (G1).** Pick the cheapest real option — a scheduled GitHub Action invoking `python -m runtime.worker --once` hourly, or a `launchd`/systemd unit — and commit the unit/workflow. The 24/7 thesis needs at least 24/1.
2. **Add ruff + mypy to CI (G4).** The codebase is already annotation-complete; this is a one-day change with permanent payoff. Gate on both.
3. **Add coverage with a floor (G5).** `pytest --cov=plugin --cov=runtime --cov-fail-under=70`, then write the missing `worker`/`persistence`/`api.risk` tests (mock the EDGAR fetch; temp-dir the SQLite path — the `db_path` injection points already exist).
4. **Add a live-EDGAR integration job (G7).** A scheduled (not per-PR) workflow running `poll_edgar` end-to-end against the real submissions API with the secret User-Agent, asserting persistence rows and packet emission; alert on failure instead of skipping silently.
5. **Automate and sign releases (G8).** A `release.yml` triggered on tags: build sdist/wheel, generate SBOM + SHA256SUMS, attach to a GitHub Release, enable artifact attestation; sign tags (`git tag -s`) or adopt gitsig/SSH signing.
6. **Mark stub outputs at the data level (G2).** Every stub-mode payload should carry a machine-readable `data_quality: "stub"`/`mode` field that the risk gate refuses to act on — today only humans reading `notes` strings can tell.
7. **Harden persistence (G3).** Enable WAL mode, add a retention/rotation policy for JSONL, document the single-writer assumption, and add a scheduled off-machine backup (even a private gist/bucket) for the audit trail.
8. **Test the supported Python range (G6).** Matrix CI over 3.11/3.12/3.13/3.14 (fast: total deps are two packages).
9. **Replace GITHUB.md HEAD-pinning (G11).** Delete the hash-pinning ritual; use tags/releases as public reference points. This removes ~37% of future commit noise.
10. **Sync ARCHITECTURE.md map + repo naming (G9, G10).** Add `runtime/`, `rwa/`, `contracts/`, `scripts/`, `tests/` to the repository map; rename the local checkout to `spacx-research` and delete the stale `spacx.egg-info/`; fix the license CI job to either gate or regenerate-and-commit, not both half-heartedly (G12).

---

*Generated by Audit Track ENG. Verification commands are reproducible from repo root with `pip install -e ".[dev]"`.*
