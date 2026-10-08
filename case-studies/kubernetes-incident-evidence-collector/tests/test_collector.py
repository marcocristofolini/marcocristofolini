import json
import os
import subprocess
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from collector import (
    build_report, collect_events, inspect_deployments, inspect_pods, kubectl_get, main,
    require_namespace,
)

NOW = datetime(2026, 10, 8, 12, 0, tzinfo=timezone.utc)


def test_kubectl_read_only_argv():
    with patch("collector.subprocess.run", return_value=subprocess.CompletedProcess([], 0, '{"items": []}', '')) as run:
        assert kubectl_get("pods", "production", "demo", 15) == []
    argv = run.call_args.args[0]
    assert argv == ["kubectl", "--context", "demo", "--namespace", "production", "get", "pods", "-o", "json", "--request-timeout=15s"]
    assert run.call_args.kwargs.get("shell", False) is False


def test_warning_event_time_filter_and_order():
    events = [
        {"type": "Warning", "reason": "Old", "lastTimestamp": "2026-10-08T09:00:00Z"},
        {"type": "Normal", "reason": "Ignored", "lastTimestamp": "2026-10-08T11:59:00Z"},
        {"type": "Warning", "reason": "BackOff", "lastTimestamp": "2026-10-08T11:58:00Z", "involvedObject": {"kind": "Pod", "name": "a"}},
        {"type": "Warning", "reason": "Failed", "eventTime": "2026-10-08T11:57:00Z"},
    ]
    result = collect_events(events, datetime(2026, 10, 8, 11, 30, tzinfo=timezone.utc))
    assert [e["reason"] for e in result] == ["Failed", "BackOff"]


def test_pod_health_and_restart_detection():
    pod = {"metadata": {"name": "api"}, "status": {"phase": "Running", "containerStatuses": [
        {"name": "app", "restartCount": 4, "ready": False, "state": {"waiting": {"reason": "CrashLoopBackOff"}}}
    ]}}
    pods, findings = inspect_pods([pod])
    assert pods[0]["containers"][0]["restarts"] == 4
    assert any(f["kind"] == "container_issue" for f in findings)


def test_previous_oomkill_detected():
    pod = {"metadata": {"name": "worker"}, "status": {"phase": "Running", "containerStatuses": [
        {"name": "job", "restartCount": 1, "state": {"running": {}}, "lastState": {"terminated": {"reason": "OOMKilled"}}}
    ]}}
    _, findings = inspect_pods([pod])
    assert findings[0]["kind"] == "previous_oomkill"
    assert findings[0]["detail"] == "job: OOMKilled"


def test_failed_deployment_status():
    deployments, findings = inspect_deployments([{"metadata": {"name": "api"}, "spec": {"replicas": 3}, "status": {"availableReplicas": 1}}])
    assert deployments[0]["desired"] == 3
    assert findings[0]["kind"] == "deployment_unavailable"


def test_rbac_error_is_categorized():
    proc = subprocess.CompletedProcess([], 1, "", 'Error: pods is forbidden: User cannot list resource "pods"')
    with patch("collector.subprocess.run", return_value=proc):
        with pytest.raises(RuntimeError, match="RBAC"):
            kubectl_get("pods", "production", None, 5)


def test_timeout_is_categorized():
    with patch("collector.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="kubectl", timeout=20)):
        with pytest.raises(RuntimeError, match="timed out"):
            kubectl_get("pods", "production", None, 15)


def test_partial_report_does_not_call_absence_healthy():
    def fake_get(kind, namespace, context, timeout):
        if kind == "pods":
            raise RuntimeError("RBAC or authentication denied")
        return []
    with patch("collector.kubectl_get", side_effect=fake_get):
        report = build_report("production", None, 60, now=NOW)
    assert report["collection_status"] == "partial"
    assert report["errors"][0]["resource"] == "pods"


def test_cli_generates_json_and_exit_success(tmp_path):
    path = tmp_path / "evidence.json"
    with patch("collector.kubectl_get", return_value=[]):
        result = main(["--namespace", "production", "--output", str(path)])
    assert result == 0
    report = json.loads(path.read_text())
    assert report["schema_version"] == "1.1"
    assert report["collection_status"] == "complete"


def test_reject_invalid_namespace():
    import argparse
    with pytest.raises(argparse.ArgumentTypeError):
        require_namespace("-bad")


def test_never_serializes_full_secret_env_values():
    pod = {"metadata": {"name": "api"}, "spec": {"containers": [{"env": [{"value": "SENSITIVE_VALUE"}]}]}, "status": {"phase": "Running"}}
    pods, _ = inspect_pods([pod])
    assert "SENSITIVE_VALUE" not in json.dumps(pods)


def test_running_unready_container_and_pod_are_identified():
    pod = {"metadata": {"name": "checkout"}, "status": {
        "phase": "Running",
        "containerStatuses": [{"name": "app", "ready": False, "restartCount": 0,
                               "state": {"running": {}}}],
        "conditions": [{"type": "Ready", "status": "False", "reason": "ContainersNotReady"}],
    }}
    _, findings = inspect_pods([pod])
    assert {finding["kind"] for finding in findings} == {"pod_not_ready", "container_not_ready"}


def test_rollout_stalled_and_controller_lag_are_identified():
    deployment = {"metadata": {"name": "payments", "generation": 8},
                  "spec": {"replicas": 2},
                  "status": {"updatedReplicas": 1, "readyReplicas": 2, "availableReplicas": 2,
                             "observedGeneration": 7,
                             "conditions": [{"type": "Progressing", "status": "False",
                                             "reason": "ProgressDeadlineExceeded"}]}}
    _, findings = inspect_deployments([deployment])
    assert {finding["kind"] for finding in findings} == {
        "deployment_rollout_incomplete", "deployment_controller_lag", "deployment_rollout_stalled"
    }


def test_event_messages_redacted_by_default_and_opt_in():
    events = [{"type": "Warning", "reason": "Failed", "message": "token=SECRET_VALUE",
               "lastTimestamp": "2026-10-08T11:59:00Z"}]
    since = datetime(2026, 10, 8, 11, 30, tzinfo=timezone.utc)
    assert collect_events(events, since)[0]["message"] is None
    assert collect_events(events, since, include_event_messages=True)[0]["message"] == "token=SECRET_VALUE"


def test_event_without_timestamp_is_marked_unknown():
    result = collect_events([{"type": "Warning", "reason": "UnknownTime"}], NOW)
    assert result[0]["timestamp"] is None
    assert result[0]["timestamp_unknown"] is True


def test_kubectl_resource_allowlist():
    with pytest.raises(ValueError, match="Unsupported Kubernetes resource"):
        kubectl_get("secrets", "production", None, 5)


def test_existing_report_replaced_with_private_file(tmp_path):
    output = tmp_path / "report.json"
    output.write_text("old report", encoding="utf-8")
    with patch("collector.kubectl_get", return_value=[]):
        assert main(["--namespace", "production", "--output", str(output)]) == 0
    assert json.loads(output.read_text())["schema_version"] == "1.1"
    if os.name == "posix":
        assert os.stat(output).st_mode & 0o077 == 0


def test_partial_output_remains_distinguishable_from_healthy(tmp_path):
    def fake_get(resource, namespace, context, timeout):
        if resource == "events":
            raise RuntimeError("events: RBAC or authentication denied")
        return []
    output = tmp_path / "report.json"
    with patch("collector.kubectl_get", side_effect=fake_get):
        assert main(["--namespace", "production", "--output", str(output)]) == 2
    report = json.loads(output.read_text())
    assert report["collection_status"] == "partial"
    assert report["errors"][0]["resource"] == "events"


def test_current_failure_and_previous_oomkill_both_reported():
    pod = {"metadata": {"name": "api"}, "status": {"phase": "Running", "containerStatuses": [
        {"name": "app", "ready": False, "restartCount": 2,
         "state": {"waiting": {"reason": "CrashLoopBackOff"}},
         "lastState": {"terminated": {"reason": "OOMKilled"}}}
    ]}}
    _, findings = inspect_pods([pod])
    assert "container_issue" in {f["kind"] for f in findings}
    assert "previous_oomkill" in {f["kind"] for f in findings}
