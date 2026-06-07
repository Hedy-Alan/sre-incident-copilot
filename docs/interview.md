# Interview Guide / 面试展示指南

Use this page to present the project in 3-5 minutes.

## 3-Minute Pitch / 三分钟讲法

1. **Problem / 问题**
   - SRE incidents are stressful because impact, mitigation, evidence, and communication happen at the same time.
   - 运维故障最难的不是敲命令，而是在压力下保持判断顺序：先影响面、再止血、再定位。
2. **Solution / 方案**
   - This project turns incident response into reusable Codex skill workflows, playbooks, examples, and safe scripts.
   - 它不会直接操作生产，而是输出排障路径、建议命令、复盘草稿和改进项。
3. **Demo / 演示**
   - Run `python3 scripts/demo_incident.py`.
   - Show one example such as `examples/service-5xx-spike.md`.
   - Show the generated postmortem structure.
4. **Value / 价值**
   - Faster triage, clearer communication, safer mitigation, better postmortems.
   - 展示的是 SRE 方法论、K8s/Prometheus 实战理解和自动化沉淀能力。

## FAQ / 高频问题

### 1. 故障时你如何决定先止血还是先定位？

先看用户影响和 SLO 风险。如果影响正在扩大，优先选择可回滚、可验证、低风险的止血动作，例如回滚、限流、关闭风险功能或切换降级路径。根因分析继续进行，但不阻塞恢复。

### 2. 如何设计一个好告警？

好告警应该关联用户体验和 SLO，而不是只报机器状态。它要说明影响面、阈值、持续时间、建议 runbook，并尽量减少无行动价值的噪音。

### 3. 如何做告警降噪？

按告警是否需要立即人工动作分类。无行动价值的告警改为 dashboard 或 ticket；重复告警做聚合；阈值结合 burn rate、持续时间和业务重要性调整。

### 4. 如何做复盘？

复盘不找个人背锅，而是找系统改进点。结构包括影响、时间线、根因、促成因素、处置动作、恢复验证、预防项和 owner。

### 5. 为什么不让自动化脚本直接操作生产？

生产变更需要权限、上下文、审批和回滚策略。这个项目定位是安全辅助决策，输出建议和模板，避免把 AI 误判断直接变成生产动作。

## Resume Bullets / 简历项目描述

Choose and adapt these bullets with real numbers only:

- Built a bilingual SRE incident-response copilot that standardizes impact assessment, mitigation planning, Kubernetes troubleshooting, and postmortem drafting.
- Designed reusable runbooks for CrashLoopBackOff, service 5xx spikes, Prometheus target-down alerts, ingress failures, and node pressure scenarios.
- Created safe automation scripts that generate triage checklists and postmortem drafts without connecting to production systems.
- Improved incident communication quality by separating facts, hypotheses, next checks, mitigation options, and recovery signals.
- 沉淀 SRE 故障处理方法论，覆盖 SLO、错误预算、K8s 排障、Prometheus 查询、值班交接和复盘模板。

## STAR Placeholders / STAR 案例占位

### Case 1: MTTR Reduction

- Situation:
- Task:
- Action:
- Result:

### Case 2: Alert Noise Reduction

- Situation:
- Task:
- Action:
- Result:

### Case 3: Release Risk Control

- Situation:
- Task:
- Action:
- Result:
