# Launch self-attestation (public OSS flip)

**Effective date (public visibility):** 2026-06-05  
**Maintainer:** openjay (personal GitHub account)  
**Repository:** [openjay/spacx-research](https://github.com/openjay/spacx-research)

---

## Not legal advice

This document records **maintainer self-attestation and engineering gates** for flipping the repository from private to **public** under the MIT license. It is **not** legal counsel, trademark clearance, or investment compliance sign-off. Readers should not treat waived items below as substitute for professional advice.

---

## Project intent

- **Purpose:** Personal AI research and education around publicly filed SEC evidence, structured audits, and an open research scaffold (plugin V0, valuation layer).
- **Non-commercial:** Maintainer attests this OSS release is for research/education, not a commercial product launch or solicitation.
- **License:** [MIT](../LICENSE) — see repository root.
- **Disclaimers:** [COMPLIANCE.md](./COMPLIANCE.md) · [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md) · [BRAND_USAGE_POLICY.md](./BRAND_USAGE_POLICY.md) · [TRADEMARK_BRAND_AUDIT.md](./TRADEMARK_BRAND_AUDIT.md) · [LISTING_STATUS.md](./LISTING_STATUS.md)

**Proposed / expected listing symbol SPCX** is documented as research context only until Form 424B4 and first trading confirmation. **Not investment advice.**

---

## P0 waivers (maintainer attestation)

| Gate | Original requirement | Decision | Rationale (maintainer) |
|------|----------------------|----------|-------------------------|
| **P0-1** | Trademark counsel sign-off | **Waived — self-attested** | Engineering audit complete in [TRADEMARK_BRAND_AUDIT.md](./TRADEMARK_BRAND_AUDIT.md). Maintainer accepts residual brand confusion risk for **`spacx-research`** slug and **`SPACX-Research`** display name; no claim of affiliation with Space Exploration Technologies Corp. (SpaceX). |
| **P0-4** | CFA / distribution compliance review | **Waived — self-attested** | Default deployment remains **compliance level 2–3** per [COMPLIANCE.md](./COMPLIANCE.md). External distribution is **research-only**, governed by [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md); no level ≥4 external distribution without separate review. |

Waivers were **explicitly authorized** by the maintainer for this public flip; risks are acknowledged in the audit and policy docs linked above.

---

## P0 verification (not waived)

| Gate | Status | Evidence |
|------|--------|----------|
| **P0-2** Secret scan on `main` | **Verified** | CI job `secret-scan` (gitleaks) **success** on `main` at commit `160dfa5` (run `27002547086`, 2026-06-05). Gitleaks not installed locally; CI used as source of truth. |
| **P0-3** No committed secrets | **Verified** | Local pattern grep (API keys, private keys) on tracked tree — no matches. `SPACX_SEC_USER_AGENT` documented for GitHub Actions secrets only. |
| **P0-5** Listing status language | **Done** | [LISTING_STATUS.md](./LISTING_STATUS.md) |
| **P0-6** SECURITY.md triage | **Done** | [SECURITY.md](../SECURITY.md) |

---

## Release

- **Tag:** `v0.1.0` — first public research scaffold release (SEC evidence Phase 1, plugin V0, valuation layer, test suite).
- **Checklist:** [PUBLIC_LAUNCH_CHECKLIST.md](./PUBLIC_LAUNCH_CHECKLIST.md)

---

## 中文

**生效日期（公开可见）：** 2026-06-05  
**维护者：** openjay（个人 GitHub 账户）  
**仓库：** [openjay/spacx-research](https://github.com/openjay/spacx-research)

### 非法律意见

本文档记录维护者在 MIT 开源许可下将仓库由**私有**转为**公开**时的**自我声明与工程门禁**，**不构成**法律顾问意见、商标确权或投资合规审批。

### 项目意图

- **用途：** 基于公开 SEC 申报材料的 AI 研究与教育、结构化审计及开放研究脚手架（插件 V0、估值层）。
- **非商业：** 维护者声明本次开源发布用于研究/教育，非商业产品发布或招揽。
- **许可：** [MIT](../LICENSE)
- **免责声明：** 见 [COMPLIANCE.md](./COMPLIANCE.md)、[CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md)、[BRAND_USAGE_POLICY.md](./BRAND_USAGE_POLICY.md)、[TRADEMARK_BRAND_AUDIT.md](./TRADEMARK_BRAND_AUDIT.md)、[LISTING_STATUS.md](./LISTING_STATUS.md)

**拟上市/预期代码 SPCX** 仅作研究语境，待 Form 424B4 与首笔交易确认。**不构成投资建议。**

### P0 豁免（维护者自证）

| 门禁 | 原要求 | 决定 | 说明 |
|------|--------|------|------|
| **P0-1** | 商标律师签批 | **豁免 — 自证** | [TRADEMARK_BRAND_AUDIT.md](./TRADEMARK_BRAND_AUDIT.md) 工程审计已完成；维护者接受 **`spacx-research`** 与 **`SPACX-Research`** 的残余混淆风险；**与 SpaceX 无关联**。 |
| **P0-4** | CFA/分发合规审查 | **豁免 — 自证** | 默认 **合规等级 2–3**（[COMPLIANCE.md](./COMPLIANCE.md)）；外部分发为**仅研究**，受 [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md) 约束。 |

### P0 验证（未豁免）

- **P0-2：** CI `secret-scan`（gitleaks）在 `main` 上通过（2026-06-05）。
- **P0-3：** 本地密钥模式扫描无命中；`SPACX_SEC_USER_AGENT` 仅用于 GitHub Secrets。

### 发布

- **标签：** `v0.1.0`  
- **清单：** [PUBLIC_LAUNCH_CHECKLIST.md](./PUBLIC_LAUNCH_CHECKLIST.md)
