# Interview Showcase / 面试展示指南

Use this reference when presenting the skill as an SRE/ops portfolio artifact.

## Positioning / 作品定位

This skill demonstrates that the candidate can turn operations experience into reusable, safe, AI-assisted runbooks. It is not a script that blindly operates production. It is a structured incident copilot that helps an engineer reason, communicate, and verify under pressure.

中文表达：
这个 skill 展示的是我把运维经验沉淀成标准化流程的能力：先确认影响面，再止血，再基于指标、日志、事件分层定位，最后形成复盘和改进项。它不会直接操作生产，而是帮助 SRE 在高压故障中保持判断清晰。

## What It Demonstrates / 能力展示

- Incident command mindset: impact first, mitigation first, evidence before conclusion.
- Kubernetes troubleshooting: pods, deployments, events, ingress, nodes, resources.
- Observability: Prometheus metrics, logs, events, golden signals, recovery checks.
- Risk control: reversible changes, rollback criteria, validation signals.
- Communication: bilingual summaries, postmortem drafts, interview-ready STAR stories.

## Demo Flow / 面试演示方式

1. Show the `SKILL.md` workflow and explain why the order matters.
2. Run a checklist script for a common issue such as `CrashLoopBackOff`.
3. Generate a postmortem draft from anonymized incident facts.
4. Explain what is deliberately not automated: destructive commands, production access, secret handling.
5. Connect the artifact to real work habits: runbooks, SLO thinking, incident review, continuous improvement.

## STAR Story Placeholder / 匿名真实案例占位

Do not invent details. Fill this with anonymized facts only.

```markdown
### Situation
某业务在 <time window> 出现 <symptom>，影响 <user scope / SLO risk>。

### Task
我负责 <incident role>，目标是在 <time target> 内止血，并定位主要原因。

### Action
- 先确认影响面：<metrics/logs/events used>
- 采取止血动作：<rollback/scale/bypass/feature flag>
- 分层定位：<ingress/service/pod/node/dependency>
- 恢复验证：<golden signals and user-facing checks>

### Result
<recovery time> 内恢复，错误率从 <before> 降到 <after>，后续补充 <prevention action>。
```

## Strong Interview Phrases / 可直接使用的话术

- "I treat incident response as a sequence: impact, stabilization, evidence, isolation, mitigation, verification, and learning."
- "我不会让自动化脚本直接碰生产变更；我更看重可回滚、可验证、可审计的辅助决策。"
- "This skill is designed to show how I standardize troubleshooting, not to replace human judgment."
- "一次好的故障处理，不只是恢复服务，还要留下下一次更快恢复的机制。"
