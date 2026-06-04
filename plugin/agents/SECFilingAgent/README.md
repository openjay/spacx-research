# SECFilingAgent

**EN — Responsibilities**

- Poll EDGAR for registrant CIK `0001181412` (Space Exploration Technologies Corp).
- Flag **P0** when Form **424B4** appears (Phase 1 blocked item per [integrated audit opinion](../../../workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)).
- Diff new S-1/A vs cached `s1a2-main.htm`; extract offering math (shares × price, greenshoe, net proceeds).
- Emit structured filing events only from SEC primary documents — no media price targets.

**中文 — 职责摘要**

- 监控 EDGAR 申报（S-1/A、424B4、8-K 等），424B4 出现时触发 **P0** 告警。
- 与 Phase 1 缓存 HTML 做差异对比，更新发行条款与未验证项（B-007、B-008 等）。
- 数字仅来源于 SEC 主文件，不替代 EvidenceAuditor 的 A/B/C/D 评级。

**Schedule:** hourly (`0 * * * *`); 15m accelerated poll when 424B4 watch is active.
