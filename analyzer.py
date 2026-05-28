from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path


def parse_log_line(line: str) -> dict[str, str] | None:
    parts = line.strip().split()
    if len(parts) != 4:
        return None
    timestamp, source_ip, destination_ip, status = parts
    return {
        "timestamp": timestamp,
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "status": status.upper(),
    }


def analyze_events(lines: list[str], failure_threshold: int = 3) -> dict:
    events = [event for line in lines if (event := parse_log_line(line))]
    failures = [event for event in events if event["status"] == "FAIL"]
    successes = [event for event in events if event["status"] == "OK"]
    failure_sources = Counter(event["source_ip"] for event in failures)
    flagged = [
        source for source, count in failure_sources.items()
        if count >= failure_threshold
    ]
    total = len(events)
    failure_rate = (len(failures) / total * 100) if total else 0.0
    return {
        "total": total,
        "successes": len(successes),
        "failures": len(failures),
        "failure_rate": failure_rate,
        "failure_sources": failure_sources,
        "flagged": flagged,
    }


def format_summary(summary: dict) -> str:
    lines = [
        "Network Log Summary",
        f"Total events: {summary['total']}",
        f"Successful connections: {summary['successes']}",
        f"Failed connections: {summary['failures']}",
        f"Failure rate: {summary['failure_rate']:.2f}%",
        "",
        "Top failure sources:",
    ]
    if summary["failure_sources"]:
        for source, count in summary["failure_sources"].most_common(5):
            lines.append(f"- {source}: {count} failures")
    else:
        lines.append("- None")

    lines.extend(["", "Flagged sources:"])
    if summary["flagged"]:
        for source in summary["flagged"]:
            lines.append(f"- {source} exceeded repeated failure threshold")
    else:
        lines.append("- None")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze simple network logs.")
    parser.add_argument("path", help="Path to a whitespace-delimited log file.")
    parser.add_argument("--threshold", type=int, default=3)
    args = parser.parse_args()

    lines = Path(args.path).read_text().splitlines()
    summary = analyze_events(lines, failure_threshold=args.threshold)
    print(format_summary(summary))


if __name__ == "__main__":
    main()
