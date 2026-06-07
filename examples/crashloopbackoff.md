# Example: CrashLoopBackOff / Pod 重启

This is an anonymized practice scenario. It does not describe a real company, cluster, or customer.

## Alert / 告警

- Alert: `KubePodCrashLooping`
- Service: `order-worker`
- Symptom: new pods restart repeatedly after a deployment
- Impact: background order processing delay; user-facing checkout still available
- SLO risk: queue processing freshness may breach within 30 minutes

## Triage / 排查路径

1. Confirm blast radius:
   - namespace, deployment, affected replicas, restart count
   - queue backlog and processing latency
2. Stabilize:
   - pause rollout or roll back if restarts correlate with release time
   - keep old healthy replicas serving if possible
3. Collect evidence:
   - `kubectl describe pod` for termination reason and events
   - `kubectl logs --previous` for the last crash
   - Prometheus restart rate, pod readiness, CPU/memory, queue lag
4. Isolate:
   - image or command issue
   - missing env/config/secret
   - OOMKilled from memory limit
   - failing startup dependency

## Suggested Checks / 建议检查

```bash
kubectl get pod -n <namespace> -l app=order-worker -o wide
kubectl describe pod -n <namespace> <pod>
kubectl logs -n <namespace> <pod> --previous
kubectl rollout history deployment -n <namespace> order-worker
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

Prometheus examples:

```promql
sum(rate(kube_pod_container_status_restarts_total{pod=~"order-worker.*"}[5m])) by (pod)
kube_pod_container_status_last_terminated_reason{pod=~"order-worker.*"}
sum(container_memory_working_set_bytes{pod=~"order-worker.*"}) by (pod)
```

## Mitigation / 止血

- Roll back to the last healthy deployment when crash start time matches release time.
- If OOMKilled is confirmed, temporarily increase memory only after checking node capacity.
- If a config/secret is missing, restore the last known valid config and restart only affected pods.

## Recovery Verification / 恢复验证

- Restart count stops increasing.
- Ready replicas match desired replicas.
- Queue lag decreases.
- Error rate and latency return to baseline.

## Postmortem Notes / 复盘要点

- Add pre-deploy config validation.
- Add canary release for worker deployment.
- Add alert routing that separates user-facing impact from background-processing risk.
