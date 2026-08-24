from __future__ import annotations

import json
import time
from pathlib import Path

from detection_engine.detector import detect_bruteforce

ROOT = Path(__file__).resolve().parents[1]
EVENT_FILE = ROOT / "logs" / "security_events.jsonl"
ALERT_DIR = ROOT / "alerts"
ALERT_FILE = ALERT_DIR / "security_alerts.jsonl"
ALERT_DIR.mkdir(parents=True, exist_ok=True)


def load_events() -> list[dict]:
    if not EVENT_FILE.exists():
        return []

    events = []
    with EVENT_FILE.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                # In v0.1 malformed lines are ignored.
                continue
    return events


def append_alert(alert: dict) -> None:
    with ALERT_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(alert, ensure_ascii=False) + "\n")


def main() -> None:
    print("[NexVigil] Detection Engine v0.1")
    print(f"[NexVigil] Watching: {EVENT_FILE}")

    seen_fingerprints: set[tuple] = set()

    try:
        while True:
            events = load_events()
            alerts = detect_bruteforce(events)

            for alert in alerts:
                fingerprint = (
                    alert["alert_type"],
                    alert["source_ip"],
                    alert["first_seen"],
                    alert["last_seen"],
                )
                if fingerprint not in seen_fingerprints:
                    seen_fingerprints.add(fingerprint)
                    append_alert(alert)
                    print(
                        "[ALERT] HIGH | T1110 Brute Force | "
                        f"source={alert['source_ip']} | "
                        f"attempts={alert['failed_attempts']}"
                    )

            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[NexVigil] Detection Engine stopped.")


if __name__ == "__main__":
    main()
