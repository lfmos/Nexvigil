from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Iterable


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def detect_bruteforce(
    events: Iterable[dict],
    threshold: int = 5,
    window_seconds: int = 60,
) -> list[dict]:

    failed_by_ip: dict[str, list[dict]] = defaultdict(list)

    for event in events:
        if (
            event.get("event_type") == "authentication"
            and event.get("action") == "login"
            and event.get("result") == "failed"
        ):
            source_ip = str(event.get("source_ip", "unknown"))
            failed_by_ip[source_ip].append(event)

    alerts: list[dict] = []

    for source_ip, ip_events in failed_by_ip.items():

        ordered = sorted(
            ip_events,
            key=lambda event: parse_time(event["timestamp"]),
        )

        for start in range(len(ordered)):

            first_time = parse_time(ordered[start]["timestamp"])
            window: list[dict] = []

            for current in ordered[start:]:

                current_time = parse_time(current["timestamp"])

                elapsed = (current_time - first_time).total_seconds()

                if elapsed <= window_seconds:
                    window.append(current)
                else:
                    break

            if len(window) >= threshold:

                target_users = sorted(
                    {
                        str(event.get("username", "unknown"))
                        for event in window
                    }
                )

                alerts.append(
                    {
                        "alert_type": "credential_bruteforce",
                        "severity": "high",
                        "source_ip": source_ip,
                        "target_users": target_users,
                        "failed_attempts": len(window),
                        "window_seconds": window_seconds,
                        "first_seen": window[0]["timestamp"],
                        "last_seen": window[-1]["timestamp"],
                        "mitre_attack": {
                            "technique_id": "T1110",
                            "technique": "Brute Force",
                        },
                    }
                )

                break

    return alerts


def detect_success_after_failures(
    events: Iterable[dict],
    threshold: int = 5,
    window_seconds: int = 60,
) -> list[dict]:

    events_by_identity: dict[tuple[str, str], list[dict]] = defaultdict(list)

    for event in events:

        if (
            event.get("event_type") != "authentication"
            or event.get("action") != "login"
        ):
            continue

        source_ip = str(event.get("source_ip", "unknown"))
        username = str(event.get("username", "unknown"))

        events_by_identity[(source_ip, username)].append(event)

    alerts: list[dict] = []

    for (source_ip, username), identity_events in events_by_identity.items():

        ordered = sorted(
            identity_events,
            key=lambda event: parse_time(event["timestamp"]),
        )

        failures: list[dict] = []

        for event in ordered:

            if event.get("result") == "failed":
                failures.append(event)
                continue

            if event.get("result") != "success":
                continue

            success_time = parse_time(event["timestamp"])

            recent_failures = [
                failure
                for failure in failures
                if 0
                <= (
                    success_time - parse_time(failure["timestamp"])
                ).total_seconds()
                <= window_seconds
            ]

            if len(recent_failures) >= threshold:

                alerts.append(
                    {
                        "alert_type": "possible_account_compromise",
                        "severity": "critical",
                        "source_ip": source_ip,
                        "target_user": username,
                        "failed_attempts_before_success": len(recent_failures),
                        "window_seconds": window_seconds,
                        "first_seen": recent_failures[0]["timestamp"],
                        "success_time": event["timestamp"],
                        "mitre_attack": {
                            "technique_id": "T1110",
                            "technique": "Brute Force",
                        },
                    }
                )

                break

    return alerts