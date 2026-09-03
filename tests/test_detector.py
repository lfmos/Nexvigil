from detection_engine.detector import (
    detect_bruteforce,
    detect_success_after_failures,
)


def make_failed_event(second: int) -> dict:

    return {
        "timestamp": f"2026-09-03T15:00:{second:02d}+00:00",
        "event_type": "authentication",
        "action": "login",
        "result": "failed",
        "username": "analyst@nexvigil.local",
        "source_ip": "127.0.0.1",
    }


def test_detects_five_failed_logins():

    events = [
        make_failed_event(second)
        for second in range(5)
    ]

    alerts = detect_bruteforce(
        events,
        threshold=5,
        window_seconds=60,
    )

    assert len(alerts) == 1

    assert alerts[0]["severity"] == "high"

    assert (
        alerts[0]["mitre_attack"]["technique_id"]
        == "T1110"
    )


def test_alert_contains_target_user():

    events = [
        make_failed_event(second)
        for second in range(5)
    ]

    alerts = detect_bruteforce(events)

    assert alerts[0]["target_users"] == [
        "analyst@nexvigil.local"
    ]


def test_does_not_alert_below_threshold():

    events = [
        make_failed_event(second)
        for second in range(4)
    ]

    assert detect_bruteforce(events) == []


def test_detects_success_after_failures():

    events = [
        make_failed_event(second)
        for second in range(5)
    ]

    events.append(
        {
            "timestamp": "2026-09-03T15:00:06+00:00",
            "event_type": "authentication",
            "action": "login",
            "result": "success",
            "username": "analyst@nexvigil.local",
            "source_ip": "127.0.0.1",
        }
    )

    alerts = detect_success_after_failures(events)

    assert len(alerts) == 1

    alert = alerts[0]

    assert alert["severity"] == "critical"

    assert (
        alert["alert_type"]
        == "possible_account_compromise"
    )

    assert (
        alert["target_user"]
        == "analyst@nexvigil.local"
    )