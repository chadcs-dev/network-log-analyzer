# Network Log Analyzer CLI

Small Python command-line tool for scanning network event logs and summarizing
connection health, error rates, and suspicious repeated failures.

## What it demonstrates

- Python file parsing
- Dictionaries and counters
- Basic anomaly detection logic
- Clean command-line output
- Simple testable functions

## Run

```bash
python3 analyzer.py sample_logs.txt
```

## Example Output

```text
Network Log Summary
Total events: 12
Successful connections: 7
Failed connections: 5
Failure rate: 41.67%

Top failure sources:
- 10.0.0.8: 3 failures
- 10.0.0.4: 2 failures

Flagged sources:
- 10.0.0.8 exceeded repeated failure threshold
```
