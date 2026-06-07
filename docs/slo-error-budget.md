# SLO and Error Budget Template / SLO 与错误预算模板

Use this document to show SRE thinking beyond "fixing servers". Keep targets realistic and tied to user experience.

## Service / 服务

- Service name: `<anonymized-service>`
- User journey: `<login / checkout / search / background processing>`
- Criticality: `<high / medium / low>`
- Owners: `<team or role, anonymized>`

## SLI / 服务水平指标

Choose indicators users can feel:

| Category | SLI | Example Query |
| --- | --- | --- |
| Availability | successful requests / total requests | `sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))` |
| Latency | P95 or P99 request duration | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` |
| Freshness | processing delay for async jobs | `max(queue_oldest_message_age_seconds)` |
| Saturation | CPU, memory, connection pool, queue depth | service-specific |

## SLO / 目标

Example:

- Availability: 99.9% successful checkout requests over 30 days
- Latency: 95% of checkout requests complete under 500 ms over 30 days
- Freshness: 99% of background jobs processed within 5 minutes

## Error Budget / 错误预算

- Window: 30 days
- Budget: `1 - SLO`
- Burn-rate alerts:
  - Fast burn: page immediately when budget is burning quickly
  - Slow burn: ticket or daytime alert when risk is accumulating

## Alert Quality / 告警质量

A good alert should answer:

- What user journey is at risk?
- Is the incident ongoing?
- What signal crossed what threshold?
- Which runbook should the on-call use?
- What is the suggested first check?

## Release Policy / 发布策略

When error budget is healthy:

- Normal release cadence
- Canary and rollback checks still required

When error budget is burning:

- Freeze risky changes
- Prioritize reliability fixes
- Require explicit owner approval for non-urgent releases

## Interview Notes / 面试讲述

- "I connect alerts to user-visible SLIs, not only infrastructure symptoms."
- "Error budget is a product and engineering tradeoff, not just an ops metric."
- "When budget burns, I prefer reversible mitigations and stronger release gates."
