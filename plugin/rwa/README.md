# Web3 / RWA pre-layer (V0)

**Compliance:** level **2** (monitor + proposals; no execution). **Execution wallet:** Phase **W4** gated. No wallet keys or live chain RPC in V0.

Integrates with platform schemas [`EvidencePacket.json`](../schemas/EvidencePacket.json) and [`AuditReceipt.json`](../schemas/AuditReceipt.json) via `evidence_hash.py`.

## Module map

| Module | Role | Schema / output |
|--------|------|-----------------|
| [`chain_state_monitor.py`](chain_state_monitor.py) | Stub monitors: stablecoin supply, tokenized treasury AUM, RWA transfers, bridge flows, oracle deviation | [`ChainStateSnapshot.json`](../schemas/ChainStateSnapshot.json) |
| [`rwa_risk_scoring.py`](rwa_risk_scoring.py) | Multi-axis 0–100 scores + explain flags; **Beyond TVL** principle | [`RWARiskScore.json`](../schemas/RWARiskScore.json) |
| [`settlement_abstraction.py`](settlement_abstraction.py) | `SettlementProfile` — trading hours, settlement, redemption, transfer rules, custodian, legal claim | [`SettlementProfile.json`](../schemas/SettlementProfile.json) |
| [`evidence_hash.py`](evidence_hash.py) | SHA-256 seals for evidence packet, metric snapshot, thesis, risk proposal; optional chain anchor placeholder | `EvidencePacket.hash`, `AuditReceipt` hashes |
| [`policy_wallet.py`](policy_wallet.py) | `ExecutionPolicy` whitelist + guards; `propose_onchain_action()` → **BLOCKED** in V0 | [`ExecutionPolicy.json`](../schemas/ExecutionPolicy.json) |

## Capability

Manifest: `rwa_prelayer_v0: monitor_only` — see [`../manifest.yaml`](../manifest.yaml).

## Agent

[`OnchainRWAAgent`](../agents/OnchainRWAAgent/README.md) schedules chain capture and hash manifests; **no trading**.

## Quick start

```bash
cd /path/to/spacx
PYTHONPATH=. python -c "
from plugin.rwa import capture_chain_state, run_rwa_risk_scoring, propose_onchain_action
print(capture_chain_state().to_dict())
print(run_rwa_risk_scoring().to_dict())
print(propose_onchain_action({'asset':'USDC','chain_id':'ethereum'}))
"
```

## Phase roadmap

| Phase | Pre-layer |
|-------|-----------|
| V0 (now) | Interfaces + stubs + schemas |
| W2 | Live RWA monitors (redemption, custody, oracle) |
| W4 | Policy-bound execution wallet (human gate) |

See [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) and [`docs/MODELS.md`](../../docs/MODELS.md).
