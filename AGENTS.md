# Purpose

Keep this repo aligned with the current conference demo: a very small Micronaut app that embeds GraalPy and runs VADER sentiment analysis on an uploaded text file.

# Current App

- Project name: `graalpy-mn-vader-v1`
- Framework: Micronaut 4.10.9
- Java target: 21
- Preferred local runtime: `sdk use java 23-graal`
- Python runtime line: GraalPy 24.x tooling
- Micronaut platform parent is pinned to 4.10.9
- Python package: `vaderSentiment==3.3.2`

# Demo Flow

1. User uploads a text-based review or article file.
2. Java reads the file as plain text.
3. Java calls a tiny embedded GraalPy script.
4. GraalPy runs VADER sentiment scoring.
5. The UI shows the uploaded text, the sentiment label and scores, the raw JSON response, and a small sentiment emoji.
6. A single clear button resets both the file input and the visible output.

# What Is In Scope

- One polished, explainable end-to-end path
- Micronaut + GraalPy integration that is easy to point to live
- Minimal Java code and minimal Python code
- Five or more clean sample files for stage use
- Simple local execution on macOS Apple Silicon

# What Is Out Of Scope For This Version

- MarkItDown
- Hugging Face local models
- Summaries or labels beyond VADER sentiment
- Charts or multi-step orchestration
- GraalVM Native Image
- GraalPy 25.x migration

# Dependency Rules

- Keep `io.micronaut.graal-languages:micronaut-graalpy`
- Keep `org.graalvm.python:python-embedding` explicit because the app uses the embedding API directly
- Do not add `org.graalvm.polyglot:python-community`
- Do not move to GraalPy 25.x unless the runtime and dependency stack are upgraded together
- Pin Python packages to exact versions for demo reproducibility

# Code Rules

- Prefer the smallest working implementation over abstraction
- Pass plain decoded text from Java into GraalPy
- Keep the GraalPy bridge obvious and easy to explain
- Remove duplicate demo-only paths when the main upload flow already proves the point
- Keep `pom.xml` lean and avoid unused starter-generated options
- Small visual cues such as sentiment emoji are fine when they improve live readability with minimal code
- If an emoji is used in the sentiment card, size it for back-of-room readability
- Keep sample content original, short, readable aloud, and safe for a public conference setting

# Key Files

- `pom.xml`
- `src/main/java/gids/graalpy/demo/GraalPySentimentService.java`
- `src/main/java/gids/graalpy/demo/ReviewController.java`
- `src/main/resources/python/sentiment_app.py`
- `src/main/resources/public/index.html`
- `src/main/resources/public/styles.css`
- `src/main/resources/public/app.js`
- `samples/`

# Run Commands

```bash
sdk use java 23-graal
./mvnw test
./mvnw mn:run
```

# Success Criteria

- The app runs locally from Maven Wrapper
- The audience can follow the Java -> GraalPy -> VADER story quickly
- The code is small enough to explain in a few minutes
- The browser flow works with the bundled sample files
- The repo stays small and maintainable

# References

- Python wheels for GraalPy: https://www.graalvm.org/python/wheels/
- GraalPy demo examples: https://github.com/graalvm/graal-languages-demos/tree/main/graalpy
- Micronaut GraalPy Maven guide: https://guides.micronaut.io/latest/micronaut-graalpy-maven-java.html
