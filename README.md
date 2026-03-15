# GraalPy + Micronaut VADER Demo

This project is the smallest useful starting point for the GIDS 2026 demo:

- Micronaut 4.10.x provides the web app.
- Java calls into a tiny embedded GraalPy program.
- GraalPy runs `vaderSentiment` over an uploaded product review file.

## Run

```bash
./mvnw test
./mvnw mn:run
```

Open `http://localhost:8080`.

## What It Does

1. Shows a hello message produced by GraalPy.
2. Lets you upload a text-based product review file.
3. Decodes that file and sends the review text into GraalPy.
4. Runs VADER sentiment analysis in Python.
5. Returns the scores and a simple positive/neutral/negative label.

## Key Files

- `src/main/java/gids/graalpy/demo/GraalPySentimentService.java`
- `src/main/java/gids/graalpy/demo/ReviewController.java`
- `src/main/resources/python/sentiment_app.py`

## Notes

- The first build needs network access so Maven can resolve dependencies and GraalPy can install the VADER wheel.
- This is intentionally small. MarkItDown, multi-step orchestration, summaries, labels, and charts can be added later after this path is stable.
