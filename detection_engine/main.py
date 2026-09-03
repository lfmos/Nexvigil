from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from detection_engine.detector import (
    detect_bruteforce,
    detect_success_after_failures,
)
from detection_engine.state import (
    load_state,
    prune_recent_events,
    save_state,
)


ROOT = Path(__file__).resolve().parents[1]

EVENT_FILE = ROOT / "logs" / "security_events.jsonl"

ALERT_DIR = ROOT / "alerts"
ALERT_FILE = ALERT_DIR / "security_alerts.jsonl"

STATE_DIR = ROOT / "state"
STATE_FILE = STATE_DIR / "detection_state.json"

ALERT_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)


def read_new_events(
    event_file: Path,
    offset: int,
) -> tuple[list[dict], int]:
    if not event_file.exists():
        return [], 0

    file_size = event_file.stat().st_size

    # O arquivo foi truncado ou recriado.
    if offset > file_size:
        offset = 0

    events: list[dict] = []

    with event_file.open("rb") as handle:
        handle.seek(offset)

        while True:
            raw_line = handle.readline()

            if not raw_line:
                break

            try:
                line = raw_line.decode("utf-8").strip()
            except UnicodeDecodeError:
                continue

            if not line:
                continue

            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

        new_offset = handle.tell()

    return events, new_offset


def append_alert(alert: dict) -> None:
    with ALERT_FILE.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                alert,
                ensure_ascii=False,
            )
            + "\n"
        )


def compute_alert_id(alert: dict) -> str:
    if alert["alert_type"] == "credential_bruteforce":
        identity = "|".join(
            [
                alert["alert_type"],
                alert["source_ip"],
                ",".join(alert.get("target_users", [])),
                alert["first_seen"],
            ]
        )

    else:
        identity = "|".join(
            [
                alert["alert_type"],
                alert["source_ip"],
                str(alert.get("target_user", "")),
                str(alert.get("success_time", "")),
            ]
        )

    digest = hashlib.sha256(
        identity.encode("utf-8")
    ).hexdigest()[:16]

    return f"NV-ALT-{digest.upper()}"


def main() -> None:
    print("[NexVigil] Detection Engine v0.1.2")
    print(f"[NexVigil] Watching: {EVENT_FILE}")
    print(f"[NexVigil] State: {STATE_FILE}")

    state = load_state(STATE_FILE)

    try:
        while True:
            new_events, new_offset = read_new_events(
                EVENT_FILE,
                state["file_offset"],
            )

            if not new_events:
                time.sleep(2)
                continue

            correlation_events = (
                state["recent_events"]
                + new_events
            )

            correlation_events = prune_recent_events(
                correlation_events,
                retention_seconds=120,
            )

            alerts: list[dict] = []

            alerts.extend(
                detect_bruteforce(correlation_events)
            )

            alerts.extend(
                detect_success_after_failures(
                    correlation_events
                )
            )

            emitted_alert_ids = set(
                state["emitted_alert_ids"]
            )

            for alert in alerts:
                alert_id = compute_alert_id(alert)

                if alert_id in emitted_alert_ids:
                    continue

                alert["alert_id"] = alert_id

                append_alert(alert)

                emitted_alert_ids.add(alert_id)

                if alert["severity"] == "critical":
                    print(
                        "[ALERT] CRITICAL | "
                        f"{alert_id} | "
                        "Possible Account Compromise | "
                        f"user={alert['target_user']} | "
                        f"source={alert['source_ip']} | "
                        f"failures="
                        f"{alert['failed_attempts_before_success']}"
                    )

                else:
                    print(
                        "[ALERT] HIGH | "
                        f"{alert_id} | "
                        "T1110 Brute Force | "
                        f"source={alert['source_ip']} | "
                        f"users="
                        f"{','.join(alert['target_users'])} | "
                        f"attempts="
                        f"{alert['failed_attempts']}"
                    )

            state = {
                "version": 1,
                "file_offset": new_offset,
                "recent_events": correlation_events,
                "emitted_alert_ids": sorted(
                    emitted_alert_ids
                ),
            }

            save_state(
                STATE_FILE,
                state,
            )

            time.sleep(2)

    except KeyboardInterrupt:
        print(
            "\n[NexVigil] Detection Engine stopped safely."
        )


if __name__ == "__main__":
    main()