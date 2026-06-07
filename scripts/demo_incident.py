#!/usr/bin/env python3
"""Run a local, no-cluster SRE incident demo."""

from __future__ import annotations

import textwrap


def main() -> None:
    print(
        textwrap.dedent(
            """\
            # Demo: Service5xxSpike / 3-minute SRE walkthrough

            ## 1. Alert / 告警输入
            - Alert: Service5xxSpike
            - Service: checkout-api
            - Symptom: 5xx rate increased after latest deployment
            - Impact: checkout failures; availability SLO at risk

            ## 2. Impact First / 先确认影响面
            - Check affected routes, status codes, traffic volume, and error-budget burn.
            - Split ingress-generated 5xx from application-generated 5xx.

            ## 3. Stabilize First / 先止血
            - If deployment time matches error start time, roll back the latest release.
            - If only one feature path is affected, disable the feature flag or route.
            - Avoid scaling blindly until dependency saturation is checked.

            ## 4. Evidence / 指标、日志、事件
            Suggested PromQL:
            sum(rate(http_requests_total{service="checkout-api",status=~"5.."}[5m])) by (route)
            histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="checkout-api"}[5m])) by (le, route))

            Suggested Kubernetes checks:
            kubectl get deploy,rs,pod -n <namespace> -l app=checkout-api
            kubectl logs -n <namespace> deploy/checkout-api --since=30m
            kubectl get events -n <namespace> --sort-by=.lastTimestamp

            ## 5. Recovery Verification / 恢复验证
            - 5xx rate returns below alert threshold.
            - P95/P99 latency returns to baseline.
            - Synthetic checkout probe succeeds.
            - Error-budget burn rate drops.

            ## 6. Postmortem Follow-ups / 复盘改进
            - Add canary analysis for checkout route.
            - Add dependency timeout regression test.
            - Link runbook in alert annotations.
            """
        )
    )


if __name__ == "__main__":
    main()
