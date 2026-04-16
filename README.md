# GraalPy + Micronaut + VADER Sentiment Analysis Demo

This demo project consists of the following:

- Micronaut 4.10.10 provides the web app.
- Java calls a tiny embedded GraalPy program during review analysis.
- GraalPy runs `vaderSentiment` over an uploaded product review file.
- The Maven project and app name are aligned around `graalpy-mn-vader-v1`.

## Run

```bash
sdk install java 25.0.2-graal
sdk use java 25.0.2-graal
```
```bash
./mvnw test
```
```bash
./mvnw mn:run
```

Open `http://localhost:8080`.

Use the sample data files in `samples/` to quickly test the upload flow during the demo.

## Native Image

This repo has also been validated locally with Micronaut native image packaging:

```bash
sdk use java 25.0.2-graal
```
```bash
./mvnw package -Dpackaging=native-image
```
```bash
./target/graalpy-mn-vader-v1
```

The native executable is created in the `target/` directory as `graalpy-mn-vader-v1`.

## Load Testing

Load-testing utilities live in the separate `benchmarks/` folder so they do not interfere with the application code.

```bash
benchmarks/run-jvm-benchmark.sh
```
```bash
benchmarks/run-native-benchmark.sh
```

Each run generates raw CSV/JSON files plus a simple HTML report with throughput, CPU, and memory charts.

## What It Does

1. Lets you upload a text-based product review file.
2. Decodes that file in Java and sends the plain review text into GraalPy.
3. Runs VADER sentiment analysis in Python.
4. Returns the scores and a simple positive/neutral/negative label.

## Key Files

- `src/main/java/graalpy/demo/GraalPySentimentService.java`
- `src/main/java/graalpy/demo/ReviewController.java`
- `src/main/resources/python/sentiment_app.py`
- `benchmarks/`

## Notes

- The first build needs network access so Maven can resolve dependencies and GraalPy can install the VADER wheel.
- The VADER dependency is pinned to `vaderSentiment==3.3.2` so the live demo stays reproducible.
- Native image is a supported build path for this demo, not just a stretch experiment.
- The benchmark harness uses only built-in/local tools already present on this machine: `python3`, `curl`, and `ps`.
