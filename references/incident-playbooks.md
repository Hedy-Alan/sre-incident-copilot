# Incident Playbooks / 故障排查 Playbook

Use these playbooks as starting points. Keep each action evidence-driven and reversible.

## K8s Pod CrashLoopBackOff

Primary signals:
- Pod restart count, last termination reason, exit code
- Recent deploy, image, config, secret, env var, command changes
- Container logs before exit
- CPU/memory limits and OOMKilled events
- Readiness/liveness probe failures

Suggested checks:
```bash
kubectl get pod -n <namespace> <pod> -o wide
kubectl describe pod -n <namespace> <pod>
kubectl logs -n <namespace> <pod> --previous
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl rollout history deployment -n <namespace> <deployment>
```

Mitigation options:
- Roll back the latest deployment if failures correlate with release time.
- Temporarily increase memory limits only if OOMKilled is confirmed and capacity allows.
- Disable broken liveness probes only as a temporary measure with explicit expiry.

Recovery verification:
- Restart count stops increasing.
- Ready pods return to expected replica count.
- Service error rate and latency return to normal.

## Service 5xx Spike / 服务 5xx 激增

Primary signals:
- HTTP status distribution by route, upstream, pod, and ingress
- P95/P99 latency and saturation
- Recent deploy/config change
- Dependency errors, timeouts, connection pool exhaustion
- Traffic change or bad client behavior

Suggested checks:
```bash
kubectl get deploy,rs,pod -n <namespace> -l app=<service>
kubectl logs -n <namespace> deploy/<deployment> --since=30m
kubectl top pod -n <namespace>
kubectl describe ingress -n <namespace> <ingress>
```

Prometheus query examples:
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service, route)
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
sum(rate(container_cpu_usage_seconds_total{pod=~"<pod-prefix>.*"}[5m])) by (pod)
```

Mitigation options:
- Roll back the latest risky release.
- Scale replicas if saturation is confirmed and downstream dependencies can handle it.
- Reduce traffic to the faulty route or disable a risky feature flag.

## Prometheus Target Down

Primary signals:
- Target health, scrape error, last scrape time
- ServiceMonitor/PodMonitor selectors
- Endpoint and port names
- NetworkPolicy, DNS, TLS, auth, or service discovery changes

Suggested checks:
```bash
kubectl get servicemonitor,podmonitor -A
kubectl get endpoints -n <namespace> <service>
kubectl describe service -n <namespace> <service>
kubectl get networkpolicy -n <namespace>
```

Prometheus query examples:
```promql
up{job="<job-name>"}
scrape_duration_seconds{job="<job-name>"}
scrape_samples_scraped{job="<job-name>"}
```

Mitigation options:
- Fix selector or port-name mismatch.
- Restore metrics endpoint path or auth config.
- Treat app health separately from observability health if user traffic is unaffected.

## Node CPU / Memory / Disk Pressure

Primary signals:
- Node conditions: MemoryPressure, DiskPressure, PIDPressure
- Top pods by CPU/memory
- Evictions and scheduling failures
- Disk inode and container log growth

Suggested checks:
```bash
kubectl describe node <node>
kubectl top node
kubectl top pod -A --sort-by=cpu
kubectl top pod -A --sort-by=memory
kubectl get events -A --sort-by=.lastTimestamp
```

Mitigation options:
- Cordon and drain only after checking redundancy and disruption budget.
- Scale workloads away or reduce noisy workload traffic.
- Clean log pressure through approved platform procedures, not ad hoc deletion.

## Nginx Ingress Issues / 入口层异常

Primary signals:
- 4xx/5xx split at ingress versus application
- Upstream connect timeout, read timeout, reset, no live upstream
- Ingress rule, TLS secret, annotation, backend service changes
- Controller reload errors

Suggested checks:
```bash
kubectl describe ingress -n <namespace> <ingress>
kubectl get svc,endpoints -n <namespace> <service>
kubectl logs -n ingress-nginx deploy/ingress-nginx-controller --since=30m
```

Mitigation options:
- Roll back ingress annotation or routing changes.
- Restore backend endpoints or service selector.
- Temporarily route traffic to the last known healthy backend.

## MySQL or External Dependency Latency / 数据库或外部依赖延迟

Primary signals:
- Application timeout and connection pool metrics
- Database slow queries, locks, saturation, connection count
- External provider status and error distribution
- Retry storm or queue backlog

Suggested checks:
```bash
kubectl logs -n <namespace> deploy/<deployment> --since=30m
kubectl top pod -n <namespace>
```

Prometheus query examples:
```promql
histogram_quantile(0.95, sum(rate(db_query_duration_seconds_bucket[5m])) by (le, service))
sum(rate(db_errors_total[5m])) by (service, error)
sum(rate(http_client_requests_total{status=~"5..|timeout"}[5m])) by (service, target)
```

Mitigation options:
- Reduce traffic, disable expensive feature paths, or enable cached fallback.
- Increase timeout only when it reduces false failure and does not amplify saturation.
- Stop retry storms by lowering retry count or adding backoff.
