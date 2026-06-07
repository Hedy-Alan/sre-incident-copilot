# SRE Incident Copilot

`sre-incident-copilot` is a bilingual Codex skill for SRE and operations incident response.
It helps triage Kubernetes, Linux, and Prometheus incidents, draft safe mitigation plans,
and generate interview-ready postmortem material.

## What it shows

- Structured incident response: impact, stabilization, evidence, isolation, mitigation, verification, learning
- Kubernetes troubleshooting: pods, deployments, events, ingress, nodes, and resource pressure
- Observability thinking: Prometheus metrics, logs, events, golden signals, and recovery checks
- Safe automation: helper scripts print templates and checklists only; they do not connect to production systems
- Interview value: bilingual SRE portfolio material with STAR placeholders for anonymized real cases

## Install

Copy this folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R sre-incident-copilot ~/.codex/skills/
```

Then invoke it with:

```text
Use $sre-incident-copilot to triage a Kubernetes or Prometheus incident and draft a concise postmortem.
```

## Validate

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py ./sre-incident-copilot
```

## Safety

This skill does not include real company names, domains, IP addresses, cluster names, customer data, or production secrets.
The scripts are intentionally read-only template generators.
