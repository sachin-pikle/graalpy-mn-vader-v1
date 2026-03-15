# GraalPy + Micronaut + VADER Sentiment Analysis Demo

This demo project consists of the following:

- Micronaut 4.10.9 provides the web app.
- Java calls a tiny embedded GraalPy program during review analysis.
- GraalPy runs `vaderSentiment` over an uploaded product review file.
- The Maven project and app name are aligned around `graalpy-mn-vader-v1`.

## Run

```bash
sdk use java 23-graal
./mvnw test
./mvnw mn:run
```

Open `http://localhost:8080`.

The project compiles for Java 21 bytecode, pins the Micronaut platform to 4.10.9, and is currently validated locally with the `23-graal` runtime.

## Native Image

This repo has also been validated locally with Micronaut native image packaging:

```bash
sdk use java 23-graal
./mvnw package -Dpackaging=native-image
./target/micronautguide
```

The native executable is created in the `target/` directory as `micronautguide`.

## What It Does

1. Lets you upload a text-based product review file.
2. Decodes that file in Java and sends the plain review text into GraalPy.
3. Runs VADER sentiment analysis in Python.
4. Returns the scores and a simple positive/neutral/negative label.

## Key Files

- `src/main/java/gids/graalpy/demo/GraalPySentimentService.java`
- `src/main/java/gids/graalpy/demo/ReviewController.java`
- `src/main/resources/python/sentiment_app.py`

## Notes

- The first build needs network access so Maven can resolve dependencies and GraalPy can install the VADER wheel.
- The VADER dependency is pinned to `vaderSentiment==3.3.2` so the live demo stays reproducible.
- Native image is a supported build path for this demo, not just a stretch experiment.
