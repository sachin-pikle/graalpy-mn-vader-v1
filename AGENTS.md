# Purpose

Build a small, conference-friendly demo app for my GIDS 2026 session, "Practical Python AI in Java with GraalPy". The app must clearly show GraalPy embedded in Java, not just a generic AI workflow.

# Success Criteria

- The demo runs locally on my MacBook Pro M2
- I can show the full pipeline end to end with a provided sample file
- Each pipeline step has visible input, output, status, and logs
- The code stays small, readable, and easy to explain live
- The demo supports the core GraalPy-in-Java story from the session

# Project Defaults

- Language: Java 25
- Framework: Micronaut preferred; Spring Boot acceptable if it keeps the demo simpler
- If Micronaut is used, prefer a GraalVM and GraalPy 24.x baseline for the first version; do not assume GraalVM 25.x compatibility without verifying the exact Micronaut 4.10.x combination
- Build: Maven Wrapper required and use Maven for the first version; add Gradle Wrapper only later if it does not create significant extra maintenance
- Runtime: local-only execution on macOS Apple Silicon
- AI/data stack: GraalPy, MarkItDown, VADER sentiment, a small local Hugging Face model, and Plotly or Pygal for visualization
- UX goal: polished enough for a live audience, but still simple
- Code goal: minimal, modular, maintainable, and easy to narrate

# Required Demo Flow

Implement the app as a visible step-by-step pipeline:

1. User uploads a sample product-review file.
2. MarkItDown extracts or converts the uploaded content into plain text.
3. VADER performs sentiment analysis.
4. A local Hugging Face model generates a summary.
5. A local Hugging Face model generates categories or labels.
6. The app renders a visual summary of the results.

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
