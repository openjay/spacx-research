# SBOM policy

**Scope:** SPDX intent, CycloneDX artifact for releases, and how to regenerate locally.

SPACX publishes a **CycloneDX JSON** Software Bill of Materials (`sbom.json`) alongside a **pip freeze lock snapshot** (`requirements-lock.txt`) for enterprise consumers who need reproducible dependency visibility. This is **not** a legal attestation; it is an engineering supply-chain artifact.

---

## SPDX intent

| Goal | Approach |
|------|----------|
| **License clarity** | [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) (direct deps) + [`docs/DEPENDENCY_LICENSES.md`](./DEPENDENCY_LICENSES.md) (transitive) |
| **Machine-readable inventory** | CycloneDX 1.5 JSON from `cyclonedx-py` (maps to SPDX identifiers where available) |
| **Reproducible install snapshot** | `requirements-lock.txt` from CI `pip freeze` after `pip install -e ".[dev]"` |

We do **not** currently ship a standalone SPDX 2.3 document. CycloneDX components include `licenses` fields suitable for SPDX ID crosswalk. If a downstream consumer requires SPDX-only format, convert with [spdx/tools-python](https://github.com/spdx/tools-python) or request a maintainer export at release time.

---

## Regeneration (local)

```bash
python -m venv .venv-sbom && source .venv-sbom/bin/activate
pip install -e ".[dev]"
pip freeze > requirements-lock.txt
pip install cyclonedx-bom
cyclonedx-py environment -o sbom.json --output-format json
```

Validate JSON:

```bash
python -c "import json; json.load(open('sbom.json'))"
```

---

## CI and releases

| Artifact | Source | When |
|----------|--------|------|
| `requirements-lock.txt` | `pip freeze` in CI `supply-chain` job | Every push/PR to `main` |
| `sbom.json` | `cyclonedx-py environment` in CI | Every push/PR to `main` |

Artifacts upload to the GitHub Actions run (`supply-chain` artifact). **Tagged releases** should attach both files plus SHA-256 checksums — see [`PUBLIC_LAUNCH_CHECKLIST.md`](./PUBLIC_LAUNCH_CHECKLIST.md).

Optional scheduled commit: a maintainer may open a PR to commit refreshed `requirements-lock.txt` on a weekly schedule; SBOM stays CI-generated until release attach step is automated.

---

## Related docs

- [`docs/DEPENDENCY_LICENSES.md`](./DEPENDENCY_LICENSES.md)
- [`docs/OPEN_SOURCE_READINESS.md`](./OPEN_SOURCE_READINESS.md)
- [`docs/PUBLIC_LAUNCH_CHECKLIST.md`](./PUBLIC_LAUNCH_CHECKLIST.md)
