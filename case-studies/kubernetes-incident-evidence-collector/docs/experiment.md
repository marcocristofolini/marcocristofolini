# First AI Code Generation Experiment for SRE

**Day 6 deliverable | 2026-10-08**  
**Project:** Kubernetes Incident Evidence Collector  
**Status:** Initial generation and refinement completed; mocked tests passed; live-cluster validation pending.

> **Public portfolio note:** This document records the original seven-day sprint. References to baseline/collector_day4.py describe the separately archived sprint artifact; the public case folder currently publishes the reviewed collector and expanded test suite.

## 1. SRE task and problem statement

During Kubernetes incidents, SREs repeatedly run `kubectl` commands to investigate Warning events, unhealthy Pods, container restarts, and Deployment rollout status. Manually retrieving and consolidating these signals is repetitive and increases the risk of inconsistent evidence collection during high-pressure incident response.

**Selected task:** Create a read-only Python command-line tool that collects a consistent incident-evidence snapshot from one Kubernetes namespace and exports structured JSON for later analysis. The output can eventually be used as input for an evidence-first, deterministic RCA engine. This collector itself does **not** determine root cause, predict incidents, or perform remediation.

## 2. AI coding tool and environment

- **Tool selected in Day 2:** GitHub Copilot for Visual Studio Code.
- **Tool that actually produced the Day 4 source in this documented interaction:** ChatGPT (AI-assisted code generation). GitHub Copilot execution and its original output have not been independently verified. To document a Copilot-specific experiment, the Day 3 prompt should also be run in Copilot and that unmodified output retained.
- **Implementation:** Python 3.11+, standard library (`argparse`, `subprocess`, `json`, etc.), `kubectl` CLI.
- **Test framework:** pytest, with mocked `kubectl` responses.
- **Target environment:** Kubernetes, accessed through a preconfigured read-only Kubernetes identity with namespace-scoped `list` privileges for `events`, `pods`, and `deployments`.

## 3. Initial prompt (Day 3)

The generation prompt requested a production-oriented, **read-only** Python CLI named *Kubernetes Incident Evidence Collector* with the following requirements:

> Act as a Senior Site Reliability Engineer and Python developer experienced in Kubernetes, incident response, and observability. Build a production-oriented, read-only Python 3.11+ CLI called Kubernetes Incident Evidence Collector. Use `argparse`, `subprocess` calls to `kubectl get ... -o json` (never a shell), the Python standard library and pytest for tests. For one user-selected namespace, collect Warning events with timestamps and affected resources; detect unhealthy Pods, container failures and restart counts; inspect Deployment readiness, availability and rollout metadata; assemble a chronological event timeline; and export a structured JSON report. Expose `--namespace`, optional `--context`, `--since-minutes`, and `--output`. Treat API errors, RBAC denials and timeouts explicitly. Never modify resources, retrieve Secrets or expose credentials. Use UTC timestamps. Supply the CLI, unit tests with mocked `kubectl` responses, a README, sample JSON and usage instructions. Success means a one-command read-only collection that yields valid JSON and can be compared with the equivalent manual workflow.

This paragraph preserves the initial prompt's technical intent; the longer Day 3 submission contains the original full-length formulation.

## 4. First generated code (Day 4)

**Saved artifact:** `baseline/collector_day4.py` (snapshot included in the Day 5 project; original Day 4 project also includes `collector.py`).

The first version:

- Called `kubectl` to retrieve Events, Pods and Deployments for a namespace.
- Extracted Warning events, container state/restart information and Deployment status.
- Built a chronological event list and wrote a JSON report.
- Included basic exception handling and pytest tests with mocked Kubernetes responses.

**Initial verification:** 11/11 automated tests passed. This verifies the scripted scenarios, not live cluster compatibility or production readiness.

## 5. Code review and manual refinements (Day 5)

**Saved artifact:** `collector.py` in the reviewed project; `docs/day5-review.md` documents the review. The following changes were introduced after reviewing the generated source:

| Review finding | Refinement |
| --- | --- |
| A Pod could be running but not ready | Detect unready containers and Pod readiness failures |
| Rollout failures were not fully surfaced | Detect stalled Deployment rollouts, lagging controller generation and incomplete updated replicas |
| A prior out-of-memory failure could be lost | Track previous `OOMKilled` status separately from current failures |
| Warning event messages could include sensitive text | Omit unstructured event messages by default; require explicit opt-in |
| JSON output could be partial or broadly accessible | Use atomic writes and `0600` file permissions on POSIX |
| Generalized resource queries could permit unsafe expansion | Restrict collection to an explicit resource allowlist |
| Some events lack reliable timestamps | Flag unknown timestamps rather than present them as confidently recent |

**Revised verification:** 19/19 automated tests passed. Python compilation and JSON syntax validation also passed. The revised JSON schema identifies itself as version `1.1`.

## 6. Observations and lessons learned

1. **AI accelerated creation of an initial implementation**, but it did not eliminate the need for SRE review. The first passing test suite missed operational edge cases that were identified in the manual review.
2. **Tests provide scoped evidence.** Passing 11 and then 19 mocked tests establishes behavior for those cases, not reliability in real clusters.
3. **Secure defaults matter for diagnostic tools.** Kubernetes event messages and resource metadata can disclose sensitive operational data; exported reports need access controls and human review before sharing.
4. **Completeness must be explicit.** A partial result caused by RBAC or API failures cannot be interpreted as proof that a namespace is healthy.
5. **Evidence collection is not RCA.** A chronological timeline and a set of findings are useful inputs for investigation, but causal conclusions and incident summaries require further validation and potentially a separate AI layer.

## 7. Outcomes and measurements

| Metric | Baseline / observed value | Interpretation |
| --- | --- | --- |
| Automated tests in initial version | 11 passed | Mocked responses only |
| Automated tests after review | 19 passed | Eight additional passing tests; not a measured accuracy increase |
| Syntax and sample JSON validation | Passed | Local structural checks |
| Read-only design | `kubectl get` for an allowlisted set of resources | Implementation design; actual RBAC must be verified |
| Time saved versus manual collection | Not measured | Benchmark pending |
| Root-cause accuracy | Not measured | Collector does not identify root cause |
| Time to first actionable diagnosis / MTTR | Not measured | Requires incident-based evaluation |
| Live Kubernetes testing | Not performed | Pending controlled-cluster validation |

## 8. Next steps

1. Run the collector in a disposable test namespace using a least-privilege service account; verify `list` permissions for the three resource types.
2. Compare output against manual `kubectl` collection for a controlled failed rollout and readiness-probe scenario.
3. Measure collection time in both approaches and log completeness, missed findings, and false positives.
4. Review reports for sensitive information and verify file permissions on the intended operating system (Windows ACLs differ from POSIX `0600`).
5. If the training requires GitHub Copilot specifically, run the original Day 3 prompt in Copilot, save its untouched output, and compare that result with the implementation documented here.

## 9. Evidence / artifacts

- **Day 4 initial source:** `baseline/collector_day4.py`
- **Day 5 refined source:** `collector.py`
- **Code review:** `docs/day5-review.md`
- **Tests:** `tests/test_collector.py`
- **Synthetic report:** `sample-report.json`
- **Project usage guide:** `README.md`

**Reproduce local verification:**

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m compileall -q collector.py tests
python -m json.tool sample-report.json > /dev/null
```

Run tests from the Day 5 project root. The sample JSON is synthetic and should not be described as a captured production incident.