## Community Guidelines

Before contributing, please read:

- CONTRIBUTING.md — Development workflow and contribution guidelines.
- CODE_OF_CONDUCT.md — Community standards and expected behavior.
- SECURITY.md — Responsible vulnerability disclosure process.

# Contributing to Yomikoe

First of all, thank you for considering contributing to **Yomikoe**.

Whether you're fixing a typo, reporting a bug, improving documentation, or implementing a new feature, every contribution helps make the project better for everyone.

This document explains how we collaborate and the principles that guide development.

---

# 1. Welcome

Yomikoe is a community-driven project built around simplicity, transparency, and maintainability.

We welcome contributors of all experience levels. You don't need to be an expert to make meaningful contributions—improving documentation, fixing bugs, writing tests, or reviewing pull requests are all valuable ways to help.

If you're unsure where to start, maybe look for issues labeled:

* `good first issue`
* `help wanted`
* `enchancement`

---

# 2. Project Philosophy

The following principles guide every design and implementation decision in Yomikoe.

## Offline First

Yomikoe should work without requiring internet access whenever possible.

Online services should always be optional rather than mandatory.

---

## Free & Open Source

The project is developed in the open.

We prefer open standards, transparent development, and permissive collaboration.

---

## Modular Architecture

Components should have clear responsibilities and well-defined interfaces.

Backends, pipelines, and infrastructure should be replaceable without affecting the rest of the system.

---

## Well Documented

Code is only complete when it is understandable.

New features should include appropriate documentation, examples, or comments where necessary.

---

## Beginner Friendly

We value readable code over clever code.

New contributors should be able to understand the project structure without needing extensive internal knowledge.

---

## Replaceable Components

Avoid tightly coupling implementations.

Whenever practical, design systems so components can be swapped with minimal changes.

---

## Explicit over Magic

Prefer code that is obvious and predictable.

Avoid hidden behavior, unnecessary abstractions, and implicit side effects.

---

# 3. Development Setup

1. Fork the repository.
2. Clone your fork.
3. Create a virtual environment.
4. Install project dependencies.
5. Install development dependencies.
6. Run the test suite before making changes.
7. Run the formatter and linter before opening a Pull Request.

Refer to the project documentation for the latest installation instructions.

---

# 4. Development Workflow

We use a simple feature-based workflow.

```text
Issue
   ↓
Feature Branch
   ↓
Implementation
   ↓
Pull Request
   ↓
Review
   ↓
Merge
```

Recommended process:

1. Open or choose an existing issue.
2. Create a feature branch from the default branch.
3. Implement the change.
4. Keep commits focused and meaningful.
5. Run tests and linting.
6. Open a Pull Request.
7. Address review feedback.
8. Merge after approval.

---

# 5. Coding Guidelines

Keep the codebase consistent and easy to maintain.

## Python Version

* Use **Python 3.14+**.

## Type Hints

* Use type hints for all public APIs.
* Prefer explicit types over `Any` whenever practical.

## Formatting & Linting

* Use **Ruff** for formatting and linting.
* Ensure all checks pass before submitting a Pull Request.

## Functions

* Prefer small functions with a single responsibility.
* Keep implementations easy to read.

## Architecture

Separate concerns clearly:

* Domain
* Pipeline
* Infrastructure

Avoid mixing responsibilities between layers.

## Dependencies

Avoid introducing new dependencies unless they provide clear long-term value.

Whenever possible, prefer the standard library or existing project utilities.

---

# 6. Pull Request Guidelines

Before opening a Pull Request, please ensure:

* The change solves a specific problem.
* The code follows the project's style.
* Linting passes.
* Tests pass.
* Documentation is updated when necessary.
* The Pull Request description explains **what changed** and **why**.

Small, focused Pull Requests are much easier to review than large ones.

---

# 7. Commit Convention

Use clear, descriptive commit messages following the Conventional Commit style adopted by the project.

Examples:

```text
feat(cli): export SRT file

feat(engine): integrate Faster-Whisper backend

fix(audio): handle empty audio stream

refactor(audio): introduce AudioMetadata TypedDict

docs(readme): update installation guide

test(engine): improve transcription coverage

chore(ci): update GitHub Actions
```

Recommended commit types:

* `feat`
* `fix`
* `refactor`
* `docs`
* `test`
* `chore`
* `perf`
* `build`
* `ci`

Keep each commit focused on a single logical change.

---

# 8. Reporting Bugs

When reporting a bug, please include:

* A clear description of the problem
* Steps to reproduce
* Expected behavior
* Actual behavior
* Operating system
* Python version
* Relevant logs or error messages
* Screenshots if applicable

The more information you provide, the easier it is to investigate.

---

# 9. Suggesting Features

Feature requests are always welcome.

When proposing a feature, consider explaining:

* The problem you're trying to solve
* Why the feature is useful
* Possible implementation ideas (optional)
* Alternatives you've considered

Not every proposal will be accepted, but all thoughtful suggestions are appreciated and will be discussed openly.

---

# Thank You

Thank you for helping improve Yomikoe.

Every contribution—whether code, documentation, bug reports, testing, or feedback—helps make the project more reliable, maintainable, and accessible to everyone.
