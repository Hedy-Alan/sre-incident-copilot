# Example: Service 5xx Spike / 服务 5xx 激增

This is an anonymized practice scenario. It does not describe a real company, cluster, or customer.

## Alert / 告警

- Alert: `Service5xxSpike`
- Service: `checkout-api`
- Symptom: 5xx rate rises after a new release
- Impact: some checkout requests fail
- SLO risk: availability burn rate is high for the checkout path

## Triage / 排查路径

1. Confirm impact:
   - affected route, status code, region, service version
   - error budget burn and user-facing failure rate
2. Stabilize:
   - roll back latest release if error rate aligns with deployment
   - reduce traffic to risky route or disable risky feature flag
3. Collect evidence:
   - ingress 5xx versus application 5xx
   - pod restarts and saturation
   - dependency timeout or connection pool errors
4. Isolate:
   - ingress/backend mismatch
   - application regression
   - dependency latency
   - retry storm or saturation

## Suggested Checks / 建议检查

```bash
kubectl get deploy,rs,pod -n <namespace> -l app=checkout-api
kubectl logs -n <namespace> deploy/checkout-api --since=30m
kubectl top pod -n <namespace>
kubectl describe ingress -n <namespace> <ingress>
```

Prometheus examples:

```promql
sum(rate(http_requests_total{service="checkout-api",status=~"5.."}[5m])) by (route)
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="checkout-api"}[5m])) by (le, route))
sum(rate(http_client_requests_total{service="checkout-api",status=~"5..|timeout"}[5m])) by (target)
```

## Mitigation / 止血

- Roll back the latest deployment if the regression is release-correlated.
- Disable the suspected feature flag if blast radius is narrow.
- Scale only when saturation is confirmed and dependencies can absorb load.

## Recovery Verification / 恢复验证

- 5xx rate returns below alert threshold.
- P95/P99 latency returns to baseline.
- Synthetic checkout probe succeeds.
- Error budget burn rate drops.

## Postmortem Notes / 复盘要点

- Add canary analysis for checkout route.
- Add dependency timeout tests in CI.
- Add runbook link to the alert annotation.
