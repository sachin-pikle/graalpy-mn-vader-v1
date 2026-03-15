# Purpose

Build a small, conference-friendly demo app for my GIDS 2026 session, "Practical Python AI in Java with GraalPy". The app must clearly show GraalPy embedded in Java, not just a generic AI workflow.

# Success Criteria

- The demo runs locally on my MacBook Pro M2
- I can show the full pipeline end to end with a provided sample file
- Each pipeline step has visible input, output, status, and logs
- The code stays small, readable, and easy to explain live
- The demo supports the core GraalPy-in-Java story from the session

# Project Defaults

- Language: Java 21 bytecode target for the demo Micronaut app
- Framework: Micronaut preferred; Spring Boot acceptable if it keeps the demo simpler
- If Micronaut is used, prefer a GraalVM and GraalPy 24.x baseline for the first version; do not assume GraalVM 25.x compatibility without verifying the exact Micronaut 4.10.x combination
- Default local runtime for demo, test, and live rehearsal: `sdk use java 23-graal`
- Avoid Java 25 for the first conference-ready build unless the exact Micronaut 4.10.x plus GraalPy combination has been re-verified end to end
- Build: Maven Wrapper required and use Maven for the first version; add Gradle Wrapper only later if it does not create significant extra maintenance
- Runtime: local-only execution on macOS Apple Silicon
- AI/data stack: GraalPy, MarkItDown, VADER sentiment, a small local Hugging Face model, and Plotly or Pygal for visualization
- UX goal: polished enough for a live audience, but still simple
- Code goal: minimal, modular, maintainable, and easy to narrate

# Version Guardrails

- Compile and package the app for Java 21 unless there is a specific reason to raise the bytecode level
- Use `23-graal` as the preferred SDKMAN runtime while validating the Micronaut + GraalPy demo locally
- Keep GraalPy tooling on an explicit 24.x version line for now instead of drifting to 25.x
- Pin Python dependencies to exact versions for reproducible demos; do not leave `vaderSentiment` as a floating range

# Reference Material

Use these sources as primary implementation references while shaping the first version of the demo:

- Python wheels for GraalPy: https://www.graalvm.org/python/wheels/
- GraalPy demo examples: https://github.com/graalvm/graal-languages-demos/tree/main/graalpy
- Micronaut GraalPy Maven guide: https://guides.micronaut.io/latest/micronaut-graalpy-maven-java.html

# Current Delivery Plan

Build the demo in small, verifiable phases instead of jumping straight to the full conference flow.

## Phase 1: Minimal Working Story

Start with the smallest end-to-end demo that still proves the session point:

1. A Micronaut 4.10.x app runs locally with Maven Wrapper.
2. Java calls a tiny embedded GraalPy program through a small, obvious integration layer.
3. The user uploads a text-based product review file.
4. GraalPy runs VADER sentiment analysis on the uploaded text.
5. The UI shows the uploaded review text and the resulting sentiment scores.

Do not add MarkItDown, local Hugging Face models, labeling, visualization, or multi-step orchestration until Phase 1 works reliably.
Treat reproducible local startup and version alignment as part of Phase 1, not cleanup work for later.

# Required Demo Flow

Implement the app as a visible step-by-step pipeline:

1. User uploads a sample product-review file.
2. MarkItDown extracts or converts the uploaded content into plain text.
3. VADER performs sentiment analysis.
4. A local Hugging Face model generates a summary.
5. A local Hugging Face model generates categories or labels.
6. The app renders a visual summary of the results.

For the current implementation, Phase 1 takes priority over the full pipeline above.
Only move beyond Phase 1 after the minimal upload-plus-VADER path is working end to end.

For every step:

- Show the step input and output in the UI
- Show a clear state such as ready, running, complete, or failed
- Let the user click a button to run the next step
- Write useful logs when the step starts, completes, or fails

# Required Deliverables

- A working local demo application
- A simple frontend that looks appealing to developers
- A proper `.gitignore`
- Three additional sample input files for the demo
- Sensible logging so the app does not appear idle for long periods
- A short README with setup, run steps, demo flow, and architecture notes

# Session Coverage

When practical, make sure the demo also supports these session points:

- Embed Python in Java with GraalPy
- Install and bundle Python packages from Maven or Gradle
- Call Python libraries from Java through a small, understandable integration layer
- Demonstrate local inference, data processing, and visualization
- Package the app as a single deployable JAR

Treat GraalVM Native Image as a stretch goal, not a blocker for the first working version.

# Working Rules

- Prefer one complete working demo over supporting every possible framework or build combination
- Avoid unnecessary abstraction, configuration, and extra dependencies
- Prefer local-only execution; avoid paid APIs and cloud dependencies
- Keep the project small enough to explain during a live session
- Keep the code modular: separate pipeline steps into small, easy-to-demo units with clear boundaries
- If two options are equally valid, choose the one with less code and less setup friction
- Do not hide important logic in generated files
- Make changes in a way that remains easy to inspect in local git history

# Definition Of Done

The work is complete when:

- The app runs locally with documented commands
- The audience can follow the pipeline step by step
- Logs make progress visible throughout the demo
- The Python-in-Java integration is easy to point to in code
- The repository remains small and maintainable

## Phase 1 Done

The current milestone is complete when:

- The app starts with `./mvnw mn:run`
- A user can upload a text review file in the browser
- Java sends that review into GraalPy with very little code
- VADER returns a clear positive, neutral, or negative result
- The code is simple enough to explain live in a couple of minutes
