# Code review: AI-generated Kubernetes incident collector

**Review date:** 2026-10-08  
**Scope:** Python CLI collecting Kubernetes Events, Pods and Deployments  
**Status:** Reviewed prototype; mock-based tests only

## Baseline and review scope

The initial AI-generated version passed 11 tests, but passing tests did not establish completeness for real SRE incident scenarios. The original source was retained in the sprint artifact archive; the public case study provides the reviewed implementation and expanded test suite.

## Findings and refinements

| Initial finding | Operational risk | Refinement |
| --- | --- | --- |
| Pods in Running state with unready containers might not produce a finding | Readiness probe failures remain invisible | Added container_not_ready and pod_not_ready |
| Replica availability was emphasized over rollout state | Stalled rollout or lagging controller overlooked | Added ProgressDeadlineExceeded, observedGeneration and updatedReplicas checks |
| Previous OOMKilled state could be obscured by current container state | Historical evidence lost | Separate previous_oomkill finding |
| Event messages always captured | Potential exposure of sensitive data | Message omitted by default; explicit opt-in |
| JSON written directly to the output path | Truncated file on write failure; broad default permissions | Atomic replacement and POSIX 0600 |
| Resource query helper accepted arbitrary resource names | Unintentional expansion to undesired data | Fixed read-only resource allowlist |
| Untimed events lacked a clear marker | Unwarranted confidence in event recency | timestamp_unknown |
| API errors could be confused with healthy/empty results | False reassurance during an incident | complete / partial / failed status with errors |

## Review decisions

- The collector only runs kubectl **get** for three allowlisted resources. It never invokes a mutation.
- This is not an automatic RCA classifier or autonomous remediation system.
- A timestamped warning event is an observed signal, not proof of causality.
- Results are incomplete whenever RBAC or API calls fail; the JSON reports this explicitly.
- Event messages are excluded by default, but names and metadata in reports still require access controls.
- The schema was revised to version 1.1. Downstream consumers must confirm compatibility.

## Verification

Run from the case study directory:

~~~bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m compileall -q collector.py tests
python -m json.tool sample-report.json
~~~

The expanded test suite has **19 passing mocked tests**, covering read-only execution, ordering/time filtering, container state, restarts, OOMKills, readiness, rollout issues, event message opt-in, RBAC, timeouts, unknown timestamps, namespace input validation, file permissions, and partial failures.

**Limitations:** no test has yet verified end-to-end behavior against a running Kubernetes cluster. No actual incident investigation time, diagnosis accuracy or MTTR improvement was measured.

## Next controlled validation

1. Set up a disposable namespace with a service account limited to list permissions for events, pods and deployments.
2. Trigger a deliberate readiness failure and a failed Deployment rollout.
3. Compare CLI results with manual kubectl commands and investigate missed or spurious findings.
4. Measure execution time and evidence completeness and inspect the resulting file for sensitive metadata.
5. Only after collecting these measurements, evaluate ingestion into an evidence-first RCA workflow.
