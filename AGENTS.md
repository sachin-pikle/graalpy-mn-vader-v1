# Purpose

Keep this repo aligned with the current sample: a very small Micronaut app that uses the direct GraalPy embedding API to run VADER sentiment analysis on an uploaded text file.

# Current Sample Snapshot

- Artifact and app name: `graalpy-mn-vader-v1`
- Version label: `v1`
- Framework: Micronaut 4.10.11
- Java target: 25
- Preferred local runtime: `sdk use java 25.0.2-graal`
- GraalPy runtime and embedding API: 25.0.2
- Python package: `vaderSentiment==3.3.2`
- UI shape: one static page with upload, preview, sentiment card, raw JSON, and a clear button
- Bundled sample inputs: five short text files under `samples/`

# Pattern To Preserve

1. Serve the UI from `src/main/resources/public`.
2. Accept a multipart upload at `/api/reviews/analyze`.
3. Validate missing or empty uploads in the controller.
4. Decode uploaded bytes to plain UTF-8 text in Java.
5. Load the Python script from `classpath:python/sentiment_app.py` and create a GraalPy context with `GraalPyResources`.
6. Keep the Python module under `src/main/resources/python/`.
7. Return a small JSON string from Python and map it into a Java record.
8. Render the preview, score, label, emoji, and raw JSON in the browser.
9. Keep a single clear action that resets both the file input and the visible output.
10. Keep the direct Java -> GraalPy script -> VADER path obvious in the code.

# Similar-Example Rules

- Prefer direct GraalPy embedding with `GraalPyResources.contextBuilder()` over the Micronaut `@GraalPyModule` pattern in this `v1` sample.
- Keep the Java-to-Python boundary simple: pass plain decoded text plus small scalar inputs such as the file name.
- Keep the Python side tiny and obvious. One module file and one exported function is ideal for this style of sample.
- Keep the script loaded from `classpath:python/sentiment_app.py` and evaluated from Java so the manual embedding path stays easy to explain.
- Keep the function lookup explicit through Python bindings and guard that the returned member is executable.
- Return JSON from Python and deserialize it into a small `@Serdeable` record on the Java side.
- Keep `pom.xml` lean. Keep explicit `org.graalvm.python:python`, `org.graalvm.python:python-embedding`, and the `graalpy-maven-plugin`.
- Keep the `maven-shade-plugin` executable JAR configuration in `pom.xml`. Preserve merged service resources and the `Multi-Release: true` manifest entry so GraalPy and Truffle initialize correctly in the shaded jar.
- Do not add `io.micronaut.graal-languages:micronaut-graalpy` unless the repo is intentionally migrating to the `v2` annotation-based approach.
- Do not add `org.graalvm.polyglot:python-community`.
- Keep the GraalPy runtime, embedding API, and Maven plugin aligned on the same version line unless they are intentionally upgraded together.
- Pin Python packages to exact versions for reproducible demos.
- Keep the UI minimal and back-of-room readable. Small visual cues like an emoji are fine when they improve a live demo.
- Keep sample content original, short, safe for a public conference setting, and easy to read aloud.
- Do not add benchmark, load-test, multi-step orchestration, or unrelated demo paths to this repo.

# Current Code Map

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
- `src/test/java/graalpy/demo/GraalPySentimentServiceTest.java`
- `src/test/java/graalpy/demo/ReviewControllerTest.java`
- `samples/`

# Run Commands

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

Native image:

```bash
sdk use java 25.0.2-graal
```

```bash
./mvnw package -Dpackaging=native-image
```

```bash
./target/graalpy-mn-vader-v1
```

Executable jar:

```bash
sdk use java 25.0.2-graal
```

```bash
./mvnw package
```

```bash
java -jar target/graalpy-mn-vader-v1-0.1.jar
```

Inspect executable jar in JD-GUI:

```bash
java -jar jd-gui-1.6.6.jar
```

When JD-GUI opens, open `target/graalpy-mn-vader-v1-0.1.jar`.

Look for these paths inside the jar:

- `python/sentiment_app.py`
- `org.graalvm.python.vfs/venv/`

See the bundled Python module, embedded GraalPy virtual filesystem, and installed Python packages packaged into the executable jar.

# Success Criteria

- The sample stays small enough to explain in a few minutes.
- The Java -> GraalPy script -> VADER story is obvious in the code.
- The browser upload flow remains the main proof path.
- The UI shows the decoded text, label, score, JSON, emoji, and clear reset behavior.
- The sample can also be packaged and run as an executable jar with `java -jar`.
- The packaged jar is easy to inspect live to show the embedded GraalPy environment and files.
- JVM and native-image paths both remain available.
- The tests continue to cover the service path and the upload endpoint.
- The repo remains narrowly focused on this one sample.

# References

- Python wheels for GraalPy: https://www.graalvm.org/python/wheels/
- GraalPy demo examples: https://github.com/graalvm/graal-languages-demos/tree/main/graalpy
- GraalPy embedding build tools: https://www.graalvm.org/latest/reference-manual/python/Embedding-Build-Tools/
