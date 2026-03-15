#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import pathlib
from collections import Counter


def load_summary(input_dir: pathlib.Path) -> dict[str, object]:
    return json.loads((input_dir / "summary.json").read_text(encoding="utf-8"))


def load_requests(input_dir: pathlib.Path) -> list[dict[str, str]]:
    with (input_dir / "requests.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_process_samples(input_dir: pathlib.Path) -> list[dict[str, str]]:
    with (input_dir / "process.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def throughput_series(requests: list[dict[str, str]]) -> list[tuple[float, float]]:
    if not requests:
        return []
    start = float(requests[0]["completed_at"])
    counts: Counter[int] = Counter()
    for row in requests:
        bucket = int(float(row["completed_at"]) - start)
        counts[bucket] += 1
    return [(float(second), float(counts.get(second, 0))) for second in range(max(counts) + 1)]


def float_series(rows: list[dict[str, str]], x_key: str, y_key: str) -> list[tuple[float, float]]:
    series: list[tuple[float, float]] = []
    for row in rows:
        try:
            series.append((float(row[x_key]), float(row[y_key])))
        except (KeyError, ValueError):
            continue
    return series


def svg_line_chart(series: list[tuple[float, float]], title: str, stroke: str) -> str:
    width = 860
    height = 260
    left = 56
    right = 16
    top = 28
    bottom = 36
    if not series:
        return f"<svg width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\" xmlns=\"http://www.w3.org/2000/svg\"><text x=\"24\" y=\"36\" font-size=\"18\" fill=\"#13202b\">{title}</text><text x=\"24\" y=\"140\" font-size=\"14\" fill=\"#5f6f7d\">No data</text></svg>"
    xs = [point[0] for point in series]
    ys = [point[1] for point in series]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(0.0, min(ys))
    max_y = max(ys)
    if math.isclose(max_x, min_x):
        max_x = min_x + 1.0
    if math.isclose(max_y, min_y):
        max_y = min_y + 1.0

    def map_x(value: float) -> float:
        return left + (value - min_x) / (max_x - min_x) * (width - left - right)

    def map_y(value: float) -> float:
        return height - bottom - (value - min_y) / (max_y - min_y) * (height - top - bottom)

    points = " ".join(f"{map_x(x):.2f},{map_y(y):.2f}" for x, y in series)
    grid = []
    for index in range(5):
        y_value = min_y + (max_y - min_y) * index / 4.0
        y = map_y(y_value)
        grid.append(f'<line x1="{left}" y1="{y:.2f}" x2="{width - right}" y2="{y:.2f}" stroke="#d9d3c8" stroke-width="1"/>')
        grid.append(f'<text x="10" y="{y + 4:.2f}" font-size="12" fill="#5f6f7d">{y_value:.1f}</text>')

    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <text x="24" y="24" font-size="18" font-weight="700" fill="#13202b">{title}</text>
  {''.join(grid)}
  <line x1="{left}" y1="{height - bottom}" x2="{width - right}" y2="{height - bottom}" stroke="#13202b" stroke-width="1.5"/>
  <line x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}" stroke="#13202b" stroke-width="1.5"/>
  <polyline fill="none" stroke="{stroke}" stroke-width="3" points="{points}"/>
</svg>'''


def write_report(input_dir: pathlib.Path, summary: dict[str, object], requests: list[dict[str, str]], process_rows: list[dict[str, str]]) -> None:
    throughput = throughput_series(requests)
    cpu_series = float_series(process_rows, "elapsed_s", "cpu_percent")
    rss_series = float_series(process_rows, "elapsed_s", "rss_mb")

    summary_table = f"""| Metric | Value |
| --- | --- |
| URL | `{summary['url']}` |
| Sample | `{summary['sample_file']}` |
| Concurrency | {summary['concurrency']} |
| Requested duration (s) | {summary['duration_requested_s']} |
| Actual duration (s) | {summary['duration_actual_s']} |
| Total requests | {summary['requests_total']} |
| Successful requests | {summary['requests_ok']} |
| Error requests | {summary['requests_error']} |
| Throughput (req/s) | {summary['throughput_rps']} |
| Avg latency (ms) | {summary['latency_avg_ms']} |
| P50 latency (ms) | {summary['latency_p50_ms']} |
| P95 latency (ms) | {summary['latency_p95_ms']} |
| P99 latency (ms) | {summary['latency_p99_ms']} |
| Peak CPU (%) | {summary['cpu_peak_percent']} |
| Peak RSS (MB) | {summary['rss_peak_mb']} |
"""

    (input_dir / "report.md").write_text(
        "# Load Test Report\n\n"
        + summary_table
        + "\nGenerated files:\n\n"
        + "- `summary.json`\n"
        + "- `requests.csv`\n"
        + "- `process.csv`\n"
        + "- `report.html`\n",
        encoding="utf-8",
    )

    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Load Test Report</title>
  <style>
    body {{ font-family: "Avenir Next", "Segoe UI", sans-serif; margin: 0; padding: 32px; background: #f2ede3; color: #13202b; }}
    main {{ max-width: 980px; margin: 0 auto; }}
    .card {{ background: rgba(255,255,255,0.88); border: 1px solid rgba(19,32,43,0.12); border-radius: 20px; padding: 24px; margin-bottom: 20px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    td, th {{ padding: 10px 12px; border-bottom: 1px solid rgba(19,32,43,0.10); text-align: left; }}
    h1, h2 {{ margin-top: 0; }}
  </style>
</head>
<body>
  <main>
    <section class="card">
      <h1>Load Test Report</h1>
      <table>
        <tbody>
          <tr><th>URL</th><td><code>{summary['url']}</code></td></tr>
          <tr><th>Sample</th><td><code>{summary['sample_file']}</code></td></tr>
          <tr><th>Concurrency</th><td>{summary['concurrency']}</td></tr>
          <tr><th>Requested duration (s)</th><td>{summary['duration_requested_s']}</td></tr>
          <tr><th>Actual duration (s)</th><td>{summary['duration_actual_s']}</td></tr>
          <tr><th>Total requests</th><td>{summary['requests_total']}</td></tr>
          <tr><th>Successful requests</th><td>{summary['requests_ok']}</td></tr>
          <tr><th>Error requests</th><td>{summary['requests_error']}</td></tr>
          <tr><th>Throughput (req/s)</th><td>{summary['throughput_rps']}</td></tr>
          <tr><th>Avg latency (ms)</th><td>{summary['latency_avg_ms']}</td></tr>
          <tr><th>P50 latency (ms)</th><td>{summary['latency_p50_ms']}</td></tr>
          <tr><th>P95 latency (ms)</th><td>{summary['latency_p95_ms']}</td></tr>
          <tr><th>P99 latency (ms)</th><td>{summary['latency_p99_ms']}</td></tr>
          <tr><th>Peak CPU (%)</th><td>{summary['cpu_peak_percent']}</td></tr>
          <tr><th>Peak RSS (MB)</th><td>{summary['rss_peak_mb']}</td></tr>
        </tbody>
      </table>
    </section>
    <section class="card">
      <h2>Throughput Over Time</h2>
      {svg_line_chart(throughput, 'Requests per second', '#c85b2b')}
    </section>
    <section class="card">
      <h2>Process CPU Over Time</h2>
      {svg_line_chart(cpu_series, 'CPU %', '#2f7e79')}
    </section>
    <section class="card">
      <h2>Process RSS Over Time</h2>
      {svg_line_chart(rss_series, 'RSS MB', '#b44134')}
    </section>
  </main>
</body>
</html>
'''
    (input_dir / "report.html").write_text(html, encoding="utf-8")


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Render a simple HTML and Markdown report from benchmark CSV/JSON files.")
    parser.add_argument("--input-dir", required=True)
    args = parser.parse_args()

    input_dir = pathlib.Path(args.input_dir).resolve()
    summary = load_summary(input_dir)
    requests = load_requests(input_dir)
    process_rows = load_process_samples(input_dir)
    write_report(input_dir, summary, requests, process_rows)
    print(f"Report written to {input_dir / 'report.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
