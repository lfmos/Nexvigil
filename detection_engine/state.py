from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

from detection_engine.detector import parse_time


DEFAULT_STATE = {
    "version": 1,
    "file_offset": 0,
    "recent_events": [],
    "emitted_alert_ids": [],
}


def load_state(state_file: Path) -> dict:
    if not state_file.exists():
        return DEFAULT_STATE.copy()

    try:
        with state_file.open("r", encoding="utf-8") as handle:
            state = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_STATE.copy()

    return {
        "version": state.get("version", 1),
        "file_offset": int(state.get("file_offset", 0)),
        "recent_events": state.get("recent_events", []),
        "emitted_alert_ids": state.get("emitted_alert_ids", []),
    }


def save_state(state_file: Path, state: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = state_file.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as handle:
        json.dump(
            state,
            handle,
            ensure_ascii=False,
            indent=2,
        )

    temporary_file.replace(state_file)


def prune_recent_events(
    events: list[dict],
    retention_seconds: int = 120,
) -> list[dict]:
    if not events:
        return []

    valid_events = [
        event
        for event in events
        if event.get("timestamp")
    ]

    if not valid_events:
        return []

    ordered = sorted(
        valid_events,
        key=lambda event: parse_time(event["timestamp"]),
    )

    newest_time = parse_time(ordered[-1]["timestamp"])
    cutoff = newest_time - timedelta(seconds=retention_seconds)

    return [
        event
        for event in ordered
        if parse_time(event["timestamp"]) >= cutoff
    ]