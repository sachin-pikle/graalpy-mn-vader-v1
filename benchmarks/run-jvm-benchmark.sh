#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUTPUT_DIR="${OUTPUT_DIR:-$ROOT/benchmarks/results/jvm-$STAMP}"
SAMPLE_FILE="${SAMPLE_FILE:-$ROOT/samples/product-coffee-grinder-positive.txt}"
CONCURRENCY="${CONCURRENCY:-4}"
DURATION="${DURATION:-20}"
APP_PORT="${APP_PORT:-8091}"
URL="${URL:-http://127.0.0.1:$APP_PORT/api/reviews/analyze}"
APP_LOG="$OUTPUT_DIR/app.log"

mkdir -p "$OUTPUT_DIR"

cd "$ROOT"
MICRONAUT_SERVER_PORT="$APP_PORT" ./mvnw -q mn:run > "$APP_LOG" 2>&1 &
LAUNCH_PID=$!
cleanup() {
  kill "$LAUNCH_PID" 2>/dev/null || true
}
trap cleanup EXIT

for _ in $(seq 1 90); do
  if curl -sf "http://127.0.0.1:$APP_PORT/" > /dev/null; then
    break
  fi
  sleep 1
done

APP_PID="$(lsof -ti tcp:"$APP_PORT" -sTCP:LISTEN | head -n 1 || true)"
if [[ -z "$APP_PID" ]]; then
  echo "Unable to find JVM application PID on port $APP_PORT." >&2
  exit 1
fi

python3 "$ROOT/benchmarks/run_benchmark.py" \
  --url "$URL" \
  --sample-file "$SAMPLE_FILE" \
  --concurrency "$CONCURRENCY" \
  --duration "$DURATION" \
  --pid "$APP_PID" \
  --output-dir "$OUTPUT_DIR"

python3 "$ROOT/benchmarks/render_report.py" --input-dir "$OUTPUT_DIR"

echo "JVM benchmark report: $OUTPUT_DIR/report.html"
