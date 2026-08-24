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
    """Detect repeated failed logins from the same source IP.

    This is intentionally simple for v0.1. Later versions should include
    deduplication, tuning, suppression and richer context.
    """
    failed_by_ip: dict[str, list[dict]] = defaultdict(list)

    for event in events:
        if (
            event.get("event_type") == "authentication"
            and event.get("action") == "login"
            and event.get("result") == "failed"
        ):
            failed_by_ip[str(event.get("source_ip", "unknown"))].append(event)

    alerts: list[dict] = []

    for source_ip, ip_events in failed_by_ip.items():
        ordered = sorted(ip_events, key=lambda e: parse_time(e["timestamp"]))

        for start in range(len(ordered)):
            first_time = parse_time(ordered[start]["timestamp"])
            window = []

            for current in ordered[start:]:
                current_time = parse_time(current["timestamp"])
                if (current_time - first_time).total_seconds() <= window_seconds:
                    window.append(current)
                else:
                    break

            if len(window) >= threshold:
                alerts.append(
                    {
                        "alert_type": "credential_bruteforce",
                        "severity": "high",
                        "source_ip": source_ip,
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
