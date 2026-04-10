#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import pathlib
import statistics
import subprocess
import threading
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict


@dataclass
class RequestResult:
    started_at: float
    completed_at: float
    latency_ms: float
    status_code: int
    ok: bool
    response_bytes: int
    error: str


@dataclass
class ProcessSample:
    timestamp: float
    elapsed_s: float
    rss_mb: float
    cpu_percent: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small local benchmark against the review upload endpoint.")
    parser.add_argument("--url", default="http://127.0.0.1:8080/api/reviews/analyze")
    parser.add_argument("--sample-file", default="samples/product-coffee-grinder-positive.txt")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--duration", type=int, default=20, help="Benchmark duration in seconds.")
    parser.add_argument("--timeout", type=float, default=15.0, help="Per-request timeout in seconds.")
    parser.add_argument("--pid", type=int, default=0, help="Application PID for CPU/RSS sampling.")
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def build_multipart_request(sample_file: pathlib.Path) -> tuple[bytes, dict[str, str]]:
    file_bytes = sample_file.read_bytes()
    boundary = f"----graalpy-bench-{uuid.uuid4().hex}"
    head = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{sample_file.name}\"\r\n"
        f"Content-Type: text/plain\r\n\r\n"
    ).encode("utf-8")
    tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = head + file_bytes + tail
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
    }
    return body, headers


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = (len(ordered) - 1) * pct
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (index - lower)


def sample_process(pid: int, samples: list[ProcessSample], stop_event: threading.Event, started_at: float) -> None:
    while not stop_event.is_set():
        completed = subprocess.run(
            ["ps", "-o", "rss=,%cpu=", "-p", str(pid)],
            check=False,
            capture_output=True,
            text=True,
        )
        line = completed.stdout.strip()
        if not line:
            break
        try:
            rss_kb_text, cpu_text = line.split()
            now = time.time()
            samples.append(
                ProcessSample(
                    timestamp=now,
                    elapsed_s=now - started_at,
                    rss_mb=float(rss_kb_text) / 1024.0,
                    cpu_percent=float(cpu_text),
                )
            )
        except ValueError:
            pass
        stop_event.wait(1.0)


def worker(url: str, body: bytes, headers: dict[str, str], deadline: float, timeout: float, results: list[RequestResult], lock: threading.Lock) -> None:
    while time.perf_counter() < deadline:
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        started_wall = time.time()
        started_perf = time.perf_counter()
        status_code = 0
        ok = False
        response_bytes = 0
        error = ""
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = response.read()
                status_code = response.getcode()
                ok = 200 <= status_code < 300
                response_bytes = len(payload)
        except urllib.error.HTTPError as exc:
            payload = exc.read()
            status_code = exc.code
            response_bytes = len(payload)
            error = f"HTTP {exc.code}"
        except Exception as exc:  # noqa: BLE001
            error = str(exc)
        completed_wall = time.time()
        latency_ms = (time.perf_counter() - started_perf) * 1000.0
        with lock:
            results.append(
                RequestResult(
                    started_at=started_wall,
                    completed_at=completed_wall,
                    latency_ms=latency_ms,
                    status_code=status_code,
                    ok=ok,
                    response_bytes=response_bytes,
                    error=error,
                )
            )


def write_requests_csv(path: pathlib.Path, results: list[RequestResult]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["started_at", "completed_at", "latency_ms", "status_code", "ok", "response_bytes", "error"])
        for result in results:
            writer.writerow([
                f"{result.started_at:.6f}",
                f"{result.completed_at:.6f}",
                f"{result.latency_ms:.3f}",
                result.status_code,
                str(result.ok).lower(),
                result.response_bytes,
                result.error,
            ])


def write_process_csv(path: pathlib.Path, samples: list[ProcessSample]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["timestamp", "elapsed_s", "rss_mb", "cpu_percent"])
        for sample in samples:
            writer.writerow([
                f"{sample.timestamp:.6f}",
                f"{sample.elapsed_s:.3f}",
                f"{sample.rss_mb:.3f}",
                f"{sample.cpu_percent:.3f}",
            ])


def build_summary(args: argparse.Namespace, results: list[RequestResult], samples: list[ProcessSample]) -> dict[str, object]:
    latencies = [result.latency_ms for result in results]
    successes = sum(1 for result in results if result.ok)
    errors = len(results) - successes
    started = min((result.started_at for result in results), default=time.time())
    completed = max((result.completed_at for result in results), default=started)
    duration_s = max(completed - started, 0.001)
    summary = {
        "url": args.url,
        "sample_file": args.sample_file,
        "concurrency": args.concurrency,
        "duration_requested_s": args.duration,
        "duration_actual_s": round(duration_s, 3),
        "requests_total": len(results),
        "requests_ok": successes,
        "requests_error": errors,
        "throughput_rps": round(len(results) / duration_s, 3),
        "latency_avg_ms": round(statistics.fmean(latencies), 3) if latencies else 0.0,
        "latency_p50_ms": round(percentile(latencies, 0.50), 3),
        "latency_p95_ms": round(percentile(latencies, 0.95), 3),
        "latency_p99_ms": round(percentile(latencies, 0.99), 3),
        "cpu_peak_percent": round(max((sample.cpu_percent for sample in samples), default=0.0), 3),
        "rss_peak_mb": round(max((sample.rss_mb for sample in samples), default=0.0), 3),
    }
    return summary


def main() -> int:
    args = parse_args()
    output_dir = pathlib.Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    sample_file = pathlib.Path(args.sample_file)
    if not sample_file.exists():
        raise SystemExit(f"Sample file not found: {sample_file}")

    body, headers = build_multipart_request(sample_file)
    results: list[RequestResult] = []
    samples: list[ProcessSample] = []
    lock = threading.Lock()
    stop_event = threading.Event()
    started_at = time.time()

    sampler = None
    if args.pid > 0:
        sampler = threading.Thread(
            target=sample_process,
            args=(args.pid, samples, stop_event, started_at),
            daemon=True,
        )
        sampler.start()

    deadline = time.perf_counter() + args.duration
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        for _ in range(args.concurrency):
            executor.submit(worker, args.url, body, headers, deadline, args.timeout, results, lock)

    stop_event.set()
    if sampler is not None:
        sampler.join(timeout=2.0)

    results.sort(key=lambda item: item.completed_at)
    summary = build_summary(args, results, samples)

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_requests_csv(output_dir / "requests.csv", results)
    write_process_csv(output_dir / "process.csv", samples)

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
