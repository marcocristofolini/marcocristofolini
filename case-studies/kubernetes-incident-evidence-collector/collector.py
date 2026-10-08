#!/usr/bin/env python3
"""Read-only Kubernetes incident evidence collection CLI (Python 3.11+)."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

UTC = timezone.utc
NS_RE = re.compile(r"^[a-z0-9](?:[-a-z0-9]*[a-z0-9])?$")
UNHEALTHY_REASONS = {
    "CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull", "CreateContainerConfigError",
    "CreateContainerError", "RunContainerError", "InvalidImageName", "OOMKilled",
    "Error", "ContainerCannotRun", "PodInitializing", "Failed",
}
ALLOWED_RESOURCES = frozenset({"events", "pods", "deployments"})


def utc_now() -> datetime:
    return datetime.now(UTC)


def parse_k8s_time(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(UTC)
    except (ValueError, TypeError):
        return None


def iso_utc(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def require_namespace(value: str) -> str:
    if len(value) > 63 or not NS_RE.fullmatch(value):
        raise argparse.ArgumentTypeError("namespace must be a valid Kubernetes DNS label")
    return value


def positive_minutes(value: str) -> int:
    try:
        minutes = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if minutes < 1 or minutes > 10080:
        raise argparse.ArgumentTypeError("must be between 1 and 10080")
    return minutes


def kubectl_get(resource: str, namespace: str, context: str | None, timeout: int) -> list[dict[str, Any]]:
    """Retrieve namespaced resources; never use a shell or a write operation."""
    if resource not in ALLOWED_RESOURCES:
        raise ValueError(f"Unsupported Kubernetes resource: {resource}")
    argv = ["kubectl"]
    if context:
        if context.startswith("-"):
            raise ValueError("Kubernetes context must not begin with '-'")
        argv += ["--context", context]
    argv += ["--namespace", namespace, "get", resource, "-o", "json", f"--request-timeout={timeout}s"]
    try:
        result = subprocess.run(argv, capture_output=True, text=True, check=False, timeout=timeout + 5)
    except FileNotFoundError as exc:
        raise RuntimeError("kubectl executable not found") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"kubectl get {resource} timed out") from exc
    except OSError as exc:
        raise RuntimeError(f"kubectl get {resource} could not start") from exc
    if result.returncode != 0:
        # Avoid storing raw kubectl output that could expose environment details.
        detail = result.stderr.lower()
        if "forbidden" in detail or "permission" in detail or "unauthorized" in detail:
            category = "RBAC or authentication denied"
        elif "connection refused" in detail or "unable to connect" in detail:
            category = "Kubernetes API unreachable"
        else:
            category = f"kubectl exited with status {result.returncode}"
        raise RuntimeError(f"{resource}: {category}")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{resource}: invalid Kubernetes JSON response") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise RuntimeError(f"{resource}: unexpected Kubernetes List response")
    return payload["items"]


def collect_events(items: list[dict[str, Any]], since: datetime,
                   include_event_messages: bool = False) -> list[dict[str, Any]]:
    out = []
    for item in items:
        if item.get("type") != "Warning":
            continue
        series = item.get("series") or {}
        stamp = (
            series.get("lastObservedTime") or item.get("lastTimestamp")
            or item.get("eventTime") or item.get("firstTimestamp")
            or (item.get("metadata") or {}).get("creationTimestamp")
        )
        parsed = parse_k8s_time(stamp)
        if parsed is not None and parsed < since:
            continue
        obj = item.get("regarding") or item.get("involvedObject") or {}
        out.append({
            "timestamp": iso_utc(parsed) if parsed else None,
            "timestamp_unknown": parsed is None,
            "reason": item.get("reason") or "Unknown",
            # Event messages can contain URLs, tokens or private data.
            "message": str(item.get("note") or item.get("message") or "")[:1000]
            if include_event_messages else None,
            "resource": {"kind": obj.get("kind"), "name": obj.get("name")},
            "count": series.get("count") or item.get("count") or 1,
        })
    return sorted(out, key=lambda e: (
        e["timestamp"] or "", e["resource"]["kind"] or "",
        e["resource"]["name"] or "", e["reason"]
    ))


def inspect_pods(items: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pods = []
    findings = []
    for pod in items:
        metadata = pod.get("metadata") or {}
        status = pod.get("status") or {}
        phase = status.get("phase") or "Unknown"
        name = metadata.get("name") or "unknown"
        containers = []
        for state in ("initContainerStatuses", "containerStatuses", "ephemeralContainerStatuses"):
            for c in status.get(state) or []:
                waiting = (c.get("state") or {}).get("waiting") or {}
                terminated = (c.get("state") or {}).get("terminated") or {}
                last_terminated = (c.get("lastState") or {}).get("terminated") or {}
                reason = waiting.get("reason") or terminated.get("reason")
                prior_reason = last_terminated.get("reason")
                container = {
                    "name": c.get("name"), "ready": c.get("ready", False),
                    "restarts": c.get("restartCount") or 0,
                    "current_reason": reason,
                    "last_termination_reason": prior_reason,
                }
                containers.append(container)
                if reason in UNHEALTHY_REASONS:
                    findings.append({"kind": "container_issue", "resource": name,
                                     "detail": f"{c.get('name')}: {reason}"})
                if prior_reason == "OOMKilled":
                    findings.append({"kind": "previous_oomkill", "resource": name,
                                     "detail": f"{c.get('name')}: OOMKilled"})
                if reason not in UNHEALTHY_REASONS and prior_reason != "OOMKilled" and container["restarts"] > 0:
                    findings.append({"kind": "container_restarts", "resource": name,
                                     "detail": f"{c.get('name')}: {container['restarts']} restarts"})
                if state == "containerStatuses" and phase == "Running" and c.get("ready") is False:
                    findings.append({"kind": "container_not_ready", "resource": name,
                                     "detail": f"{c.get('name')}: container is not ready"})
        readiness = next((c for c in status.get("conditions") or [] if c.get("type") == "Ready"), None)
        if phase == "Running" and readiness and readiness.get("status") == "False":
            findings.append({"kind": "pod_not_ready", "resource": name,
                             "detail": str(readiness.get("reason") or "Ready condition is False")})
        if phase not in ("Running", "Succeeded"):
            findings.append({"kind": "pod_phase", "resource": name, "detail": phase})
        pods.append({"name": name, "phase": phase, "containers": sorted(containers, key=lambda c: c["name"] or "")})
    return sorted(pods, key=lambda p: p["name"]), findings


def inspect_deployments(items: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    deployments = []
    findings = []
    for deployment in items:
        meta = deployment.get("metadata") or {}
        spec = deployment.get("spec") or {}
        status = deployment.get("status") or {}
        desired = spec.get("replicas", 1)
        available = status.get("availableReplicas") or 0
        ready = status.get("readyReplicas") or 0
        updated = status.get("updatedReplicas") or 0
        name = meta.get("name") or "unknown"
        conditions = [
            {"type": c.get("type"), "status": c.get("status"),
             "reason": c.get("reason"), "last_transition": c.get("lastTransitionTime")}
            for c in status.get("conditions") or []
        ]
        deployments.append({
            "name": name, "desired": desired, "available": available,
            "ready": ready, "updated": updated,
            "generation": meta.get("generation"), "observed_generation": status.get("observedGeneration"),
            "revision": (meta.get("annotations") or {}).get("deployment.kubernetes.io/revision"),
            "conditions": sorted(conditions, key=lambda c: c["type"] or ""),
        })
        if available < desired or ready < desired:
            findings.append({"kind": "deployment_unavailable", "resource": name,
                             "detail": f"available={available}, ready={ready}, desired={desired}"})
        if updated < desired:
            findings.append({"kind": "deployment_rollout_incomplete", "resource": name,
                             "detail": f"updated={updated}, desired={desired}"})
        if (isinstance(meta.get("generation"), int) and
                isinstance(status.get("observedGeneration"), int) and
                status["observedGeneration"] < meta["generation"]):
            findings.append({"kind": "deployment_controller_lag", "resource": name,
                             "detail": f"observed={status['observedGeneration']}, desired_generation={meta['generation']}"})
        if any(c.get("type") == "Progressing" and c.get("status") == "False" and
               c.get("reason") == "ProgressDeadlineExceeded" for c in status.get("conditions") or []):
            findings.append({"kind": "deployment_rollout_stalled", "resource": name,
                             "detail": "ProgressDeadlineExceeded"})
    return sorted(deployments, key=lambda d: d["name"]), findings


def build_report(namespace: str, context: str | None, since_minutes: int, timeout: int = 15,
                 now: datetime | None = None, include_event_messages: bool = False) -> dict[str, Any]:
    now = now or utc_now()
    since = now - timedelta(minutes=since_minutes)
    report: dict[str, Any] = {
        "schema_version": "1.1", "collected_at": iso_utc(now), "namespace": namespace,
        "context": context, "since_minutes": since_minutes,
        "event_messages_included": include_event_messages,
        "collection_status": "complete", "errors": [],
        "events": [], "pods": [], "deployments": [], "findings": [], "timeline": [],
    }
    for resource in ("events", "pods", "deployments"):
        try:
            items = kubectl_get(resource, namespace, context, timeout)
            if resource == "events":
                report["events"] = collect_events(items, since, include_event_messages)
            elif resource == "pods":
                report["pods"], new_findings = inspect_pods(items)
                report["findings"].extend(new_findings)
            else:
                report["deployments"], new_findings = inspect_deployments(items)
                report["findings"].extend(new_findings)
        except (RuntimeError, ValueError) as exc:
            report["errors"].append({"resource": resource, "error": str(exc)})
    report["collection_status"] = (
        "failed" if len(report["errors"]) == 3 else
        "partial" if report["errors"] else "complete"
    )
    report["findings"].sort(key=lambda f: (f["kind"], f["resource"], f["detail"]))
    report["timeline"] = [
        {"timestamp": e["timestamp"], "event": e["reason"], "resource": e["resource"]}
        for e in report["events"]
    ]
    return report


def write_report_securely(destination: Path, report: dict[str, Any]) -> None:
    """Atomically replace output with a private file (mode 0600 on POSIX)."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix=".incident-evidence-", suffix=".tmp", delete=False,
        ) as handle:
            temporary = handle.name
            os.chmod(temporary, 0o600)
            json.dump(report, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, destination)
    finally:
        if temporary is not None and os.path.exists(temporary):
            os.unlink(temporary)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect read-only Kubernetes incident evidence")
    parser.add_argument("--namespace", required=True, type=require_namespace)
    parser.add_argument("--context", help="Optional kubectl context")
    parser.add_argument("--since-minutes", type=positive_minutes, default=60)
    parser.add_argument("--output", type=Path, required=True, help="Destination JSON file")
    parser.add_argument("--include-event-messages", action="store_true",
                        help="Include event messages, which may contain sensitive information")
    args = parser.parse_args(argv)
    if args.context and args.context.startswith("-"):
        parser.error("--context cannot begin with '-'")
    report = build_report(
        args.namespace, args.context, args.since_minutes,
        include_event_messages=args.include_event_messages
    )
    try:
        write_report_securely(args.output, report)
    except OSError as exc:
        print(f"Unable to write output: {exc}", file=sys.stderr)
        return 1
    print(f"Report saved: {args.output} (status={report['collection_status']})")
    return 0 if report["collection_status"] == "complete" else 2


if __name__ == "__main__":
    sys.exit(main())
