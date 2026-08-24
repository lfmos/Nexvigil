from detection_engine.detector import detect_bruteforce


def test_detects_five_failed_logins_in_window():
    events = [
        {
            "timestamp": f"2026-08-20T19:00:{second:02d}+00:00",
            "event_type": "authentication",
            "action": "login",
            "result": "failed",
            "username": "analyst@nexvigil.local",
            "source_ip": "127.0.0.1",
        }
        for second in range(5)
    ]

    alerts = detect_bruteforce(events, threshold=5, window_seconds=60)

    assert len(alerts) == 1
    assert alerts[0]["mitre_attack"]["technique_id"] == "T1110"


def test_does_not_alert_below_threshold():
    events = [
        {
            "timestamp": f"2026-08-20T19:00:{second:02d}+00:00",
            "event_type": "authentication",
            "action": "login",
            "result": "failed",
            "username": "analyst@nexvigil.local",
            "source_ip": "127.0.0.1",
        }
        for second in range(4)
    ]

    assert detect_bruteforce(events, threshold=5, window_seconds=60) == []
