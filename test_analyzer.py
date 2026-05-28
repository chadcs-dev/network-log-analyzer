from analyzer import analyze_events


def test_analyze_events_flags_repeated_failures():
    lines = [
        "2026-05-27T09:00:01 10.0.0.8 172.16.0.12 FAIL",
        "2026-05-27T09:00:02 10.0.0.8 172.16.0.12 FAIL",
        "2026-05-27T09:00:03 10.0.0.8 172.16.0.12 FAIL",
        "2026-05-27T09:00:04 10.0.0.2 172.16.0.10 OK",
    ]
    summary = analyze_events(lines)
    assert summary["total"] == 4
    assert summary["failures"] == 3
    assert "10.0.0.8" in summary["flagged"]
