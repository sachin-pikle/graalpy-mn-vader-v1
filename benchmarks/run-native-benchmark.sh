#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUTPUT_DIR="${OUTPUT_DIR:-$ROOT/benchmarks/results/native-$STAMP}"
SAMPLE_FILE="${SAMPLE_FILE:-$ROOT/samples/sample-review.txt}"
CONCURRENCY="${CONCURRENCY:-4}"
DURATION="${DURATION:-20}"
APP_PORT="${APP_PORT:-8091}"
URL="${URL:-http://127.0.0.1:$APP_PORT/api/reviews/analyze}"
APP_LOG="$OUTPUT_DIR/app.log"
BINARY="$ROOT/target/graalpy-mn-vader-v1"

if [[ ! -x "$BINARY" ]]; then
  echo "Native binary not found at $BINARY" >&2
  echo "Build it first with ./mvnw package -Dpackaging=native-image" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

cd "$ROOT"
MICRONAUT_SERVER_PORT="$APP_PORT" "$BINARY" > "$APP_LOG" 2>&1 &
APP_PID=$!
cleanup() {
  kill "$APP_PID" 2>/dev/null || true
}
trap cleanup EXIT

for _ in $(seq 1 90); do
  if curl -sf "http://127.0.0.1:$APP_PORT/" > /dev/null; then
    break
  fi
  sleep 1
done

python3 "$ROOT/benchmarks/run_benchmark.py" \
  --url "$URL" \
  --sample-file "$SAMPLE_FILE" \
  --concurrency "$CONCURRENCY" \
  --duration "$DURATION" \
  --pid "$APP_PID" \
  --output-dir "$OUTPUT_DIR"

python3 "$ROOT/benchmarks/render_report.py" --input-dir "$OUTPUT_DIR"

echo "Native benchmark report: $OUTPUT_DIR/report.html"
