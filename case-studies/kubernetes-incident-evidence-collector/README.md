# Case study: AI-assisted Kubernetes incident evidence collection

**Domain:** Site Reliability Engineering · Kubernetes · Incident Response · AI-assisted Development  
**Date:** October 2026  
**Status:** Reviewed prototype. Mock-based automated tests passed; live-cluster validation and impact measurement remain open.

[Versão em português](README_PT-BR.md) · [Source code](collector.py) · [Tests](tests/test_collector.py) · [Experiment report](docs/experiment.md)

## The operational problem

When an alert fires in a Kubernetes environment, an SRE must often run several commands and cross-reference warning events, Pod/container state, restart history, and Deployment rollout status. This process consumes attention during incident response and can be inconsistent across investigations.

**Goal:** Generate a consistent, structured, read-only evidence snapshot with one command, so responders can spend less effort gathering facts and more time validating hypotheses.

This collector **does not** predict failures, determine root cause, generate LLM summaries, or remediate workloads. It is an evidence collection building block for future RCA workflows.

## Experiment question

Can an AI coding assistant produce a useful first version of a Kubernetes incident evidence collector, and how much review is required to make it more appropriate for SRE use?

The project was developed as a seven-step experiment: identify a repetitive task, compare assistants, write a constrained prompt, generate code, review and refine it, document observations, and identify a measurable follow-up.

- **AI tool selected for the workflow:** GitHub Copilot in VS Code.
- **Tool that generated the documented initial implementation:** ChatGPT. Independent Copilot execution was not verified.
- **Human engineering review:** focused on diagnostic completeness, safe defaults, error handling, and test coverage.
- **Implementation:** Python 3.11+, kubectl JSON output, standard library, pytest.

## System design

~~~mermaid
flowchart LR
    A[Alert or investigation] --> B[Read-only Python CLI]
    B -->|kubectl get| E[Kubernetes Events]
    B -->|kubectl get| P[Pods and container status]
    B -->|kubectl get| D[Deployment status]
    E --> N[Normalize and filter]
    P --> N
    D --> N
    N --> S[Structured JSON report]
    S --> H[Engineer validates hypotheses]
    S -. future integration .-> R[Evidence-first RCA engine]
    R -. optional future layer .-> L[AI incident summaries]
~~~

The command uses an allowlist of three resource types and subprocess argument arrays, with no shell interpolation and no write operations against the cluster. An explicitly scoped Kubernetes identity must supply the RBAC restrictions.

## What was built

The initial version collected warning events, Pod/container status, restart counts and Deployment state. It emitted a JSON timeline and structured findings.

Review of this first version identified operational issues: Running Pods with unready containers could be missed, stalled or incomplete rollouts were not fully represented, prior OOMKills required separate attention, and unstructured event messages could disclose sensitive information.

The reviewed version improved these areas and introduced:
- Pod/container readiness findings and previous OOMKill visibility.
- Rollout-incomplete, controller-lag and progress-deadline diagnostics.
- Fixed resource allowlist, safe subprocess calls and categorized failure reporting.
- Event message suppression by default, with explicit opt-in.
- Atomic JSON writes and POSIX 0600 output permissions.
- Complete/partial/failed collection states so missing evidence is never silently treated as healthy.
- Explicit handling for events with unknown timestamps.

See the [code review](docs/day5-review.md), [experiment report](docs/experiment.md), and [reviewed implementation](collector.py). The unmodified initial source is retained in the original sprint archive, rather than published in this profile repository.

## Observed results

| Verification | Initial version | Reviewed version | What this shows |
| --- | ---: | ---: | --- |
| Automated tests passing | 11 | 19 | Mocked behavior, not live-cluster compatibility |
| Python syntax check | Not recorded here | Passed | Source compiles |
| Synthetic JSON validation | Not recorded here | Passed | Example report is parseable |
| Live Kubernetes integration | Not tested | Not tested | Pending |
| Time saved compared to manual commands | Not measured | Not measured | Pending |
| MTTR / incident accuracy | Not measured | Not measured | Cannot claim impact yet |

**Interpretation:** An increase from 11 to 19 passing tests is an expansion of tested scenarios, **not** evidence of 73% greater reliability or any MTTR reduction.

## Reproduce the local tests

From this directory:

~~~bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m compileall -q collector.py tests
python -m json.tool sample-report.json
~~~

For a namespace-scoped, **read-only** investigation on a deliberately configured test cluster:

~~~bash
python collector.py --namespace default --since-minutes 60 --output incident-evidence.json
~~~

Requires Python 3.11+, kubectl, and permission to list events, pods and deployments in the target namespace. Review the output before sharing; even when event messages are omitted, resource names and status metadata may be sensitive. POSIX file permissions do not automatically translate to Windows ACLs.

The [sample report](sample-report.json) is synthetic and should not be mistaken for evidence collected from production.

## Engineering lessons

**A passing initial test suite was insufficient.** The original scenarios missed readiness and rollout edge cases; review by someone familiar with SRE failure modes materially improved the specification.

**Safety is a functional requirement.** A diagnostics tool should preserve the boundary between observation and mutation, avoid automatic incident remediation, and minimize accidental data disclosure.

**Partial evidence should be visible.** An RBAC denial, timeout or API failure creates uncertainty. A blank result after a failed query cannot be presented as a healthy namespace.

**Evidence is not causality.** Events and timestamps help engineers build hypotheses; root cause still requires corroboration with metrics, traces, dependency state and service impact.

## Next experiment

Validate the reviewed collector in a disposable Kubernetes namespace using deliberately simulated readiness failures and failed Deployment rollouts. Compare its output with a manual kubectl checklist.

Record elapsed time, evidence completeness, false positives, RBAC/API compatibility and any sensitive fields in the resulting report. Only after those measurements should the collector be considered as a possible input adapter for a deterministic RCA engine.

## Artifacts

- [Reviewed CLI](collector.py)
- [Automated tests](tests/test_collector.py)
- [Synthetic output](sample-report.json)
- [Review decisions](docs/day5-review.md)
- [Detailed experiment log](docs/experiment.md)

This is a portfolio case study of an **AI-assisted software engineering experiment**, not a claim that the collector has already achieved production-grade reliability or that GitHub Copilot generated the original code.
