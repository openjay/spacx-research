# Security policy

## Supported versions

| Version | Supported |
|---------|-----------|
| `main` branch | Yes |
| Tagged releases | Yes, latest tag only |
| Older tags | Best effort |

## Reporting a vulnerability

**Do not** open a public GitHub issue for security-sensitive reports.

1. Email the repository owner via the contact method on the [openjay/spacx-research](https://github.com/openjay/spacx-research) GitHub profile, or use GitHub **Private vulnerability reporting** if enabled.
2. Include: description, reproduction steps, affected paths, and potential impact.
3. Allow reasonable time for triage before public disclosure.

We will acknowledge receipt and coordinate a fix on `main` when appropriate.

## Scope notes

- This repository contains **research tooling**, not production trading or custody systems.
- Cached SEC HTML and evidence hashes are integrity-sensitive — report tampering or missing provenance.
- Agent API stubs (V0) are not hardened for public internet exposure; do not deploy without authentication and network controls.

## Safe harbor

Good-faith security research that follows this policy will not be pursued as hostile action. Do not test against systems or accounts you do not own or lack permission to test.
