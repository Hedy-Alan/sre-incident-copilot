#!/usr/bin/env python3
"""Print safe Kubernetes/Prometheus triage checklists."""

from __future__ import annotations

import argparse
import textwrap


CHECKLISTS: dict[str, str] = {
    "crashloopbackoff": """\
        # CrashLoopBackOff Triage / Pod 重启排查

        ## Confirm / 确认
        - Identify namespace, deployment, pod, restart count, and last exit code.
        - Compare first restart time with deploy/config/secret changes.

        ## Suggested Commands / 建议命令
        kubectl get pod -n <namespace> <pod> -o wide
        kubectl describe pod -n <namespace> <pod>
        kubectl logs -n <namespace> <pod> --previous
        kubectl get events -n <namespace> --sort-by=.lastTimestamp
        kubectl rollout history deployment -n <namespace> <deployment>

        ## Signals / 关注信号
        - K8s events: OOMKilled, probe failures, image pull errors, config mount failures.
        - Logs: panic, missing env, failed migrations, dependency connection errors.
        - Resources: CPU/memory requests and limits; check whether memory limit caused OOM.
        - Prometheus: restart rate, pod readiness, request error rate, latency.

        ## Mitigation / 止血
        - Roll back if correlated with a release.
        - Increase resources only if OOM is confirmed and capacity allows.
        - Fix probe/config only after confirming the failure mode.
        """,
    "target_down": """\
        # Prometheus Target Down Triage / 监控目标不可达排查

        ## Confirm / 确认
        - Determine whether user traffic is impacted or only observability is impacted.
        - Check target labels, scrape error, last scrape time, and job name.

        ## Suggested Commands / 建议命令
        kubectl get servicemonitor,podmonitor -A
        kubectl get endpoints -n <namespace> <service>
        kubectl describe service -n <namespace> <service>
        kubectl get networkpolicy -n <namespace>

        ## Prometheus Checks / Prometheus 查询
        up{job="<job-name>"}
        scrape_duration_seconds{job="<job-name>"}
        scrape_samples_scraped{job="<job-name>"}

        ## Signals / 关注信号
        - ServiceMonitor or PodMonitor selector mismatch.
        - Endpoint port name mismatch.
        - Metrics path, TLS, auth, DNS, or NetworkPolicy changes.
        - K8s events for the monitored pods and service endpoints.

        ## Mitigation / 止血
        - Restore selectors, endpoint port names, or metrics path.
        - Separate monitoring recovery from service recovery in communication.
        """,
    "5xx": """\
        # Service 5xx Spike Triage / 服务 5xx 激增排查

        ## Confirm / 确认
        - Split ingress 5xx from application 5xx.
        - Identify affected route, version, pod, dependency, and time window.

        ## Suggested Commands / 建议命令
        kubectl get deploy,rs,pod -n <namespace> -l app=<service>
        kubectl logs -n <namespace> deploy/<deployment> --since=30m
        kubectl top pod -n <namespace>
        kubectl describe ingress -n <namespace> <ingress>

        ## Prometheus Checks / Prometheus 查询
        sum(rate(http_requests_total{status=~"5.."}[5m])) by (service, route)
        histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

        ## Signals / 关注信号
        - Recent deploy or config change.
        - Pod CPU/memory saturation and restarts.
        - Dependency timeout, connection pool exhaustion, retry storm.
        - K8s events and ingress controller logs.

        ## Mitigation / 止血
        - Roll back risky release.
        - Scale only when saturation is confirmed and dependencies can absorb traffic.
        - Disable risky route or feature flag if blast radius is narrow.
        """,
}

ALIASES = {
    "crashloop": "crashloopbackoff",
    "pod_crash": "crashloopbackoff",
    "prometheus_target_down": "target_down",
    "targetdown": "target_down",
    "service_5xx": "5xx",
    "http_5xx": "5xx",
}


def normalize(issue: str) -> str:
    key = issue.strip().lower().replace("-", "_").replace(" ", "_")
    return ALIASES.get(key, key)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print a safe triage checklist. This script only prints suggested checks; it does not run kubectl."
    )
    parser.add_argument("issue", help="Issue type: CrashLoopBackOff, target_down, or 5xx")
    args = parser.parse_args()
    key = normalize(args.issue)
    if key not in CHECKLISTS:
        supported = ", ".join(sorted(CHECKLISTS))
        raise SystemExit(f"Unsupported issue type: {args.issue}. Supported: {supported}")
    print(textwrap.dedent(CHECKLISTS[key]).strip())


if __name__ == "__main__":
    main()
