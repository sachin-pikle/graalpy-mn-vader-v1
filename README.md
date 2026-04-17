# GraalPy + Micronaut + VADER Sentiment Demo

<small>version: v1</small>

This repo is a small Micronaut sample that accepts an uploaded text file, sends the decoded text from Java into GraalPy, runs VADER sentiment scoring, and shows the result in a simple browser UI.

This sample uses the direct GraalPy embedding API through `GraalPyResources.contextBuilder()` rather than Micronaut's injected `@GraalPyModule` pattern.

## Current Sample

- Micronaut 4.10.11
- Java 25 bytecode
- Preferred local runtime: `sdk use java 25.0.2-graal`
- GraalPy runtime and embedding API on 25.0.2
- Python dependency pinned to `vaderSentiment==3.3.2`
- One static page with upload, preview, sentiment card, raw JSON, and a clear button
- Five bundled sample input files under `samples/`

## Demo Flow

1. Upload a text-based review file from the browser.
2. Micronaut receives the multipart upload at `/api/reviews/analyze`.
3. Java decodes the upload bytes to UTF-8 text.
4. `GraalPySentimentService` creates a GraalPy context with `GraalPyResources`.
5. GraalPy runs `sentiment_app.py` and returns a JSON string.
6. Java deserializes that JSON into `ReviewAnalysisView`.
7. The UI shows the review text, sentiment label, compound score, raw JSON, and an emoji.
8. Clear resets both the file input and the visible output.

## Key Files

- `pom.xml`
- `src/main/java/graalpy/demo/Application.java`
- `src/main/java/graalpy/demo/ReviewController.java`
- `src/main/java/graalpy/demo/GraalPySentimentService.java`
- `src/main/java/graalpy/demo/ReviewAnalysisView.java`
- `src/main/resources/application.properties`
- `src/main/resources/python/sentiment_app.py`
- `src/main/resources/public/index.html`
- `src/main/resources/public/app.js`
- `src/main/resources/public/styles.css`

## Run Locally

```bash
sdk install java 25.0.2-graal
```

```bash
sdk use java 25.0.2-graal
```

```bash
./mvnw test
```

```bash
./mvnw mn:run
```

Open `http://localhost:8080`.

The first build needs network access so Maven and GraalPy can resolve dependencies and install the pinned VADER package.

## Native Image

```bash
sdk use java 25.0.2-graal
```

```bash
./mvnw package -Dpackaging=native-image
```

```bash
./target/graalpy-mn-vader-v1
```

## Executable Jar

```bash
sdk use java 25.0.2-graal
```

```bash
./mvnw package
```

```bash
java -jar target/graalpy-mn-vader-v1-0.1.jar
```

## Sample Inputs

- `samples/book-practical-ai-positive.txt`
- `samples/movie-starlight-harbor-negative.txt`
- `samples/product-coffee-grinder-positive.txt`
- `samples/product-robot-vacuum-negative.txt`
- `samples/product-wireless-headphones-positive.txt`

## Main Differences From v2

- `v1` uses direct GraalPy embedding with `GraalPyResources` plus explicit `org.graalvm.python:python` and `org.graalvm.python:python-embedding`; `v2` uses `io.micronaut.graal-languages:micronaut-graalpy` and an injected `@GraalPyModule` interface.
- `v1` runs on Micronaut 4.10.11, Java 25, and GraalPy 25.0.2; `v2` stays on Micronaut 4.10.10, Java 21, and GraalPy 24.2.1.
- `v1` keeps the Python script at `src/main/resources/python/sentiment_app.py`; `v2` keeps it under `src/main/resources/org.graalvm.python.vfs/src/sentiment_app.py`.
- `v1` calls the Python function by manually evaluating the script and reading bindings from the context; `v2` calls an injected `SentimentModule` interface method.
- `v1` does not need `src/main/resources/META-INF/native-image/proxy-config.json`; `v2` includes it because the annotation-based module path needs proxy metadata for native image.
- `v1` currently ships five sample files; `v2` documents two bundled sample inputs.

## Notes

- The VADER dependency is pinned to `vaderSentiment==3.3.2` so the live demo stays reproducible.
- Native image is a supported build path for this demo, not just a stretch experiment.
- This repo is the simpler manual-embedding variant; `v2` is the Micronaut annotation-based GraalPy variant.
