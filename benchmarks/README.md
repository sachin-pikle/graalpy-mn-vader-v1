# Load Testing

This folder keeps the load-testing utilities separate from the main demo application.

## What It Uses

- `python3`
- `curl`
- `ps`
- `lsof`

No application code changes are required to run the benchmark.

## Quick Start

JVM app:

```bash
benchmarks/run-jvm-benchmark.sh
```

Native image:

```bash
./mvnw package -Dpackaging=native-image
benchmarks/run-native-benchmark.sh
```

## Optional Tuning

```bash
APP_PORT=8092 CONCURRENCY=8 DURATION=30 benchmarks/run-jvm-benchmark.sh
APP_PORT=8092 CONCURRENCY=8 DURATION=30 benchmarks/run-native-benchmark.sh
```

## Outputs

Each run creates a timestamped folder under `benchmarks/results/` with:

- `summary.json`
- `requests.csv`
- `process.csv`
- `report.md`
- `report.html`
- `app.log`

## Notes

- The benchmark targets `POST /api/reviews/analyze` with multipart file upload.
- The default sample file is `samples/product-coffee-grinder-positive.txt`.
- The wrapper scripts use port `8091` by default so they do not interfere with a normal demo app running on `8080`.
- CPU and memory are sampled from the app process once per second.
- The HTML report includes throughput, CPU, and RSS charts generated without extra Python packages.
