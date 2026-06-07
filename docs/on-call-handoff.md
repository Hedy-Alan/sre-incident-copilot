# On-Call Handoff Template / 值班交接模板

Use this template to make reliability work auditable and easy to continue.

## Shift Summary / 值班摘要

- Time window:
- On-call engineer:
- Overall status: `<normal / degraded / active incident>`
- Open risks:

## Active Incidents / 进行中的故障

| Incident | Impact | Current Status | Owner | Next Action |
| --- | --- | --- | --- | --- |
| `<alert>` | `<user/SLO impact>` | `<investigating/mitigated/resolved>` | `<role>` | `<next check>` |

## Alerts Reviewed / 已处理告警

| Alert | Decision | Evidence | Follow-up |
| --- | --- | --- | --- |
| `<alert>` | `<paged/ticket/noise>` | `<metric/log/event>` | `<runbook/tuning>` |

## Deployments and Changes / 发布与变更

- Recent deploys:
- Config changes:
- Infra changes:
- Feature flags:

## Risk Register / 风险列表

- Capacity risk:
- Dependency risk:
- Observability gap:
- Known noisy alerts:

## Handoff Notes / 交接说明

- What changed during the shift?
- What should the next on-call watch first?
- Which dashboards or logs matter?
- What actions should not be taken without approval?

## Interview Notes / 面试讲述

- "I use handoff notes to reduce context loss between engineers."
- "A good handoff separates facts, hypotheses, and next actions."
- "On-call quality improves when repeated pain becomes runbook or alert improvements."
