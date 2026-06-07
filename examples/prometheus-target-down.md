# Example: Prometheus Target Down / 监控目标不可达

This is an anonymized practice scenario. It does not describe a real company, cluster, or customer.

## Alert / 告警

- Alert: `PrometheusTargetDown`
- Job: `payment-api`
- Symptom: Prometheus cannot scrape the metrics endpoint
- Impact: observability gap; user traffic impact not yet confirmed
- SLO risk: delayed detection if service degrades while target is down

## Triage / 排查路径

1. Confirm whether user traffic is affected:
   - request success rate, latency, traffic volume
   - health endpoint and synthetic checks
2. Check scrape failure:
   - target labels, scrape error, last scrape timestamp
   - service discovery and endpoint status
3. Isolate:
   - ServiceMonitor/PodMonitor selector mismatch
   - endpoint port name mismatch
   - metrics path changed
   - NetworkPolicy, TLS, or auth issue

## Suggested Checks / 建议检查

```bash
kubectl get servicemonitor,podmonitor -A
kubectl get svc,endpoints -n <namespace> payment-api
kubectl describe service -n <namespace> payment-api
kubectl get networkpolicy -n <namespace>
```

Prometheus examples:

```promql
up{job="payment-api"}
scrape_duration_seconds{job="payment-api"}
scrape_samples_scraped{job="payment-api"}
```

## Mitigation / 止血

- Restore metrics endpoint path or port name.
- Fix ServiceMonitor selector mismatch.
- Communicate clearly if user traffic is healthy but monitoring is degraded.

## Recovery Verification / 恢复验证

- `up{job="payment-api"} == 1`
- scrape samples return to baseline
- alert resolves
- user-facing health checks remain normal

## Postmortem Notes / 复盘要点

- Add CI validation for metrics endpoint path and service port name.
- Add alert annotation that distinguishes service-down from target-down.
- Add dashboard panel for scrape health by job.
