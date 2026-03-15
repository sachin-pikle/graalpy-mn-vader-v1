# Purpose

State what this repository exists to build, automate, or support in one or two sentences.

# Success Criteria

- Describe the most important user-visible outcome
- Describe the main technical outcome
- Describe one maintainability or quality bar

# Project Defaults

- Primary language: [language and version]
- Primary framework: [framework]
- Build or package tool: [tool]
- Runtime target: [local machine, cloud, container, platform]
- Supported environments: [for example macOS, Linux, CI]
- Primary dependencies or integrations: [short list]
- UX or product goal: [simple, polished, internal-only, etc.]
- Code goal: [minimal, highly extensible, performance-oriented, etc.]

# Required Flow

List the core user or system flow in ordered steps:

1. [Step one]
2. [Step two]
3. [Step three]

For each step, specify any expectations that always apply:

- What input should be shown or accepted
- What output should be produced or displayed
- Whether the step is automatic or user-triggered
- What progress, logging, or error handling should be visible

# Required Deliverables

- [Main application, script, or service]
- [README or runbook]
- [Tests, fixtures, or sample data]
- [Config, gitignore, Dockerfile, deployment file, etc.]

# Repo Working Rules

- Prefer [main priority such as simplicity, speed, correctness, or low cost]
- Avoid [unwanted complexity or classes of dependency]
- If there is a tradeoff, choose [default decision rule]
- Keep changes easy to review and easy to explain
- Do not move critical logic into generated artifacts

# Build And Run

Document the commands an agent should keep working:

- Setup: `[command]`
- Run locally: `[command]`
- Test: `[command]`
- Lint or format: `[command]`

If a command does not exist yet, create it and document it in the README.

# Quality Bar

- Logging should be visible enough that long-running work does not look stalled
- Errors should be surfaced clearly to the user or operator
- Keep code paths small and understandable unless complexity is required
- Add tests for the most important behavior when practical

# Optional Constraints

Use this section only when it matters:

- Performance limits
- Security or privacy requirements
- Offline-only or local-only requirements
- Packaging or deployment requirements
- Demo or presentation constraints

# Definition Of Done

The work is complete when:

- [Primary flow works end to end]
- [Docs are updated]
- [Key tests pass]
- [Important constraints are satisfied]
- [The result is maintainable enough for the intended audience]
