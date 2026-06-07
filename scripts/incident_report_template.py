#!/usr/bin/env python3
"""Generate a safe Markdown incident report draft from provided facts."""

from __future__ import annotations

import argparse
import datetime as dt


def split_items(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def bullet_list(items: list[str], placeholder: str) -> str:
    if not items:
        return f"- {placeholder}"
    return "\n".join(f"- {item}" for item in items)


def build_report(args: argparse.Namespace) -> str:
    timeline = bullet_list(split_items(args.timeline), "TODO: add timestamped incident events")
    actions = bullet_list(split_items(args.actions), "TODO: add mitigation and recovery actions")
    followups = bullet_list(split_items(args.followups), "TODO: add prevention or detection improvements")
    generated_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    root_cause = args.root_cause or "TODO: describe the confirmed root cause, or mark as unknown if still under investigation"

    return f"""# Incident Report / 故障复盘草稿

Generated at: {generated_at}

## Summary / 摘要
- Alert / 告警: {args.alert}
- Service / 服务: {args.service}
- Impact / 影响: {args.impact}
- Status / 状态: {args.status}

## Timeline / 时间线
{timeline}

## Root Cause / 根因
{root_cause}

## Actions Taken / 处置动作
{actions}

## Recovery Verification / 恢复验证
- TODO: verify error rate, latency, traffic, saturation, and user-facing behavior.

## Follow-up Items / 后续改进
{followups}

## Interview Notes / 面试讲述要点
- Explain how impact was confirmed before deep debugging.
- Explain why mitigation was reversible and how recovery was verified.
- Avoid sensitive company names, domains, IPs, cluster names, and customer details.
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a bilingual Markdown incident report draft. This script does not connect to production systems."
    )
    parser.add_argument("--alert", required=True, help="Alert name, for example: Service5xxSpike")
    parser.add_argument("--service", default="TODO: service name", help="Affected service")
    parser.add_argument("--impact", default="TODO: affected users or SLO risk", help="Impact summary")
    parser.add_argument("--status", default="Mitigated / 已止血", help="Current incident status")
    parser.add_argument("--timeline", default="", help="Semicolon-separated timeline events")
    parser.add_argument("--root-cause", default="", help="Confirmed or suspected root cause")
    parser.add_argument("--actions", default="", help="Semicolon-separated mitigation actions")
    parser.add_argument("--followups", default="", help="Semicolon-separated follow-up items")
    print(build_report(parser.parse_args()))


if __name__ == "__main__":
    main()
