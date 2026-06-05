# GitHub remote

| Field | Value |
|-------|-------|
| **URL** | https://github.com/openjay/spacx-research |
| **Visibility** | Private *(flip to public only after [`docs/PUBLIC_LAUNCH_CHECKLIST.md`](docs/PUBLIC_LAUNCH_CHECKLIST.md) P0 sign-off)* |
| **Account** | openjay (personal) |
| **Branch** | `main` |
| **Description** | SPACX-Research — proposed symbol SPCX research platform; SEC evidence, AI-native analysis, trading workflows (pre-listing) |

**HEAD (`main`):** see latest commit on `main` after push.

```bash
git clone git@github.com:openjay/spacx-research.git
# or
git clone https://github.com/openjay/spacx-research.git
```

## Public launch readiness

Before changing visibility to **public**:

1. Complete P0 items in [`docs/PUBLIC_LAUNCH_CHECKLIST.md`](docs/PUBLIC_LAUNCH_CHECKLIST.md) (counsel, secret scan green, compliance gates).
2. Confirm CI green including [`gitleaks`](../.gitleaks.toml) on `main`.
3. Attach `sbom.json` and `requirements-lock.txt` to the first signed release tag — see [`docs/SBOM_POLICY.md`](docs/SBOM_POLICY.md).

**Rename history:** `spacex-ipo-research` → `spacx` (2026-06-04) → **`spacx-research`** (2026-06-05, SPACX-Research suffix adoption).

**Contributing:** no special account required once public — fork and PR per [`CONTRIBUTING.md`](CONTRIBUTING.md).
