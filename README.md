# Demo: Sentiment Analysis with VADER, GraalPy and Micronaut

<small>version: v1</small>

This repo is a small Micronaut sample that accepts an uploaded text file, sends the decoded text from Java into GraalPy, runs VADER sentiment scoring, and shows the result in a simple browser UI.

This sample uses the direct GraalPy embedding API through `GraalPyResources.contextBuilder()` rather than Micronaut's injected `@GraalPyModule` pattern.

## Current Sample

- Micronaut 4.10.11
- Java 25 bytecode
- Preferred local runtime: `sdk use java 25.0.2-graal`
- GraalPy runtime and embedding API on 25.0.2
- GraalVM DAP tool on 25.0.2 for embedded Python debugging
- Python dependency pinned to `vaderSentiment==3.3.2`
- One static page with upload, preview, sentiment card, raw JSON, and a clear button

## Demo Flow

1. Upload a text-based review file from the browser.
2. Micronaut receives the multipart upload at `/api/reviews/analyze`.
3. Java decodes the upload bytes to UTF-8 text.
4. `GraalPyContext` creates the GraalPy context with `GraalPyResources`.
5. `GraalPySentimentService` evaluates `sentiment_app.py` from the embedded resource path and calls `analyze_review_json`.
6. Java deserializes that JSON into `ReviewAnalysisView`.
7. The UI shows the review text, sentiment label, compound score, raw JSON, and an emoji.
8. Clear resets both the file input and the visible output.

## Key Files

- `pom.xml`
- `src/main/java/graalpy/demo/Application.java`
- `src/main/java/graalpy/demo/ReviewController.java`
- `src/main/java/graalpy/demo/GraalPyContext.java`
- `src/main/java/graalpy/demo/GraalPySentimentService.java`
- `src/main/java/graalpy/demo/ReviewAnalysisView.java`
- `src/main/resources/application.properties`
- `src/main/resources/org.graalvm.python.vfs/src/sentiment_app.py`
- `src/main/resources/public/index.html`
- `src/main/resources/public/app.js`
- `src/main/resources/public/styles.css`
- `.vscode/launch.json`

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

## Debug Embedded Python

The app includes `org.graalvm.tools:dap-tool`, but DAP is off by default so the upload flow runs normally without waiting for a debugger.

### DAP Off

Keep this setting in `src/main/resources/application.properties`:

```properties
graalpy.dap.enabled=false
```

```bash
./mvnw mn:run
```

Open `http://localhost:8080`, select one of the files under `samples/`, and submit it. The result should render immediately.

### DAP On

Change `src/main/resources/application.properties` to:

```properties
graalpy.dap.enabled=true
```

Set a breakpoint in `src/main/resources/org.graalvm.python.vfs/src/sentiment_app.py`, for example inside `analyze_review_json`.

Start the app:

```bash
./mvnw mn:run
```

Open `http://localhost:8080`, select a sample text file, and submit it. The request will wait when the GraalPy context starts. In VS Code, run the `GraalPy: Attach embedded` launch configuration to attach to `localhost:4711`. Once attached, the debugger can stop at breakpoints in `sentiment_app.py`.

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

## Inspect The Jar In JD-GUI

```bash
java -jar jd-gui-1.6.6.jar
```

When JD-GUI opens, open `target/graalpy-mn-vader-v1-0.1.jar`.

Look for these paths inside the jar:

- `org.graalvm.python.vfs/src/sentiment_app.py`
- `org.graalvm.python.vfs/venv/`

See the bundled Python module, embedded GraalPy virtual filesystem, and installed Python packages packaged into the executable jar.

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

## Sample Inputs

- `samples/book-practical-ai-positive.txt`
- `samples/movie-starlight-harbor-negative.txt`
- `samples/product-coffee-grinder-positive.txt`
- `samples/product-robot-vacuum-negative.txt`
- `samples/product-wireless-headphones-positive.txt`

## Main Differences From v2

- This repo is the simpler manual-embedding variant; `v2` is the Micronaut annotation-based GraalPy variant.
- `v1` uses direct GraalPy embedding with `GraalPyResources` plus explicit `org.graalvm.python:python` and `org.graalvm.python:python-embedding`; `v2` uses `io.micronaut.graal-languages:micronaut-graalpy` and an injected `@GraalPyModule` interface.
- `v1` runs on Micronaut 4.10.11, Java 25 bytecode, `sdk use java 25.0.2-graal`, and GraalPy 25.0.2; `v2` runs on Micronaut 4.10.10, Java 21 bytecode, `sdk use java 23-graal`, and GraalPy 24.2.1.
- `v1` keeps the Python script at `src/main/resources/org.graalvm.python.vfs/src/sentiment_app.py`; `v2` keeps it under `src/main/resources/org.graalvm.python.vfs/src/sentiment_app.py`.
- `v1` manually evaluates the script and reads the function from Python bindings; `v2` calls the Python function through the injected `SentimentModule` and keeps `src/main/resources/META-INF/native-image/proxy-config.json` aligned with that interface.

## Appendix

### VM Arguments

```
export MAVEN_OPTS="--enable-native-access=ALL-UNNAMED -Dsun.misc.unsafe.memory.access=allow"
```