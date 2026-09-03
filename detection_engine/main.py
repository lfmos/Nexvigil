from __future__ import annotations

import json
import time
from pathlib import Path

from detection_engine.detector import (
    detect_bruteforce,
    detect_success_after_failures,
)


ROOT = Path(__file__).resolve().parents[1]

EVENT_FILE = ROOT / "logs" / "security_events.jsonl"

ALERT_DIR = ROOT / "alerts"
ALERT_FILE = ALERT_DIR / "security_alerts.jsonl"

ALERT_DIR.mkdir(parents=True, exist_ok=True)


def load_events() -> list[dict]:

    if not EVENT_FILE.exists():
        return []

    events: list[dict] = []

    with EVENT_FILE.open("r", encoding="utf-8") as handle:

        for line in handle:

            line = line.strip()

            if not line:
                continue

            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return events


def append_alert(alert: dict) -> None:

    with ALERT_FILE.open("a", encoding="utf-8") as handle:

        handle.write(
            json.dumps(
                alert,
                ensure_ascii=False,
            )
            + "\n"
        )


def create_fingerprint(alert: dict) -> str:

    if alert["alert_type"] == "credential_bruteforce":

        users = ",".join(alert.get("target_users", []))

        return (
            f"{alert['alert_type']}|"
            f"{alert['source_ip']}|"
            f"{users}|"
            f"{alert['first_seen']}"
        )

    return (
        f"{alert['alert_type']}|"
        f"{alert['source_ip']}|"
        f"{alert.get('target_user')}|"
        f"{alert.get('success_time')}"
    )


def main() -> None:

    print("[NexVigil] Detection Engine v0.1.1")
    print(f"[NexVigil] Watching: {EVENT_FILE}")

    seen_fingerprints: set[str] = set()

    try:

        while True:

            events = load_events()

            alerts = []

            alerts.extend(
                detect_bruteforce(events)
            )

            alerts.extend(
                detect_success_after_failures(events)
            )

            for alert in alerts:

                fingerprint = create_fingerprint(alert)

                if fingerprint in seen_fingerprints:
                    continue

                seen_fingerprints.add(fingerprint)

                append_alert(alert)

                if alert["severity"] == "critical":

                    print(
                        "[ALERT] CRITICAL | "
                        "Possible Account Compromise | "
                        f"user={alert['target_user']} | "
                        f"source={alert['source_ip']} | "
                        f"failures={alert['failed_attempts_before_success']}"
                    )

                else:

                    print(
                        "[ALERT] HIGH | "
                        "T1110 Brute Force | "
                        f"source={alert['source_ip']} | "
                        f"users={','.join(alert['target_users'])} | "
                        f"attempts={alert['failed_attempts']}"
                    )

            time.sleep(2)

    except KeyboardInterrupt:

        print("\n[NexVigil] Detection Engine stopped.")


if __name__ == "__main__":
    main()