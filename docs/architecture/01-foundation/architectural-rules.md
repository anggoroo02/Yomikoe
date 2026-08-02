# Architectural Rules & Design Principles

Version: 1.0

Status: Accepted

---

# 1. Purpose

This document defines the non-negotiable architectural rules of Yomikoe.

These rules exist to preserve long-term maintainability and architectural consistency.

---

# 2. Core Principles

Priority order:

1. Simplicity
2. Maintainability
3. Reliability
4. Extensibility
5. Performance

Performance optimizations shall never compromise architectural clarity without explicit architectural approval.

---

# 3. Dependency Rules

Dependencies always point inward.

Core modules must not depend on infrastructure implementations.

Business rules must not depend on external libraries.

---

# 4. Domain Rules

Domain models are immutable.

Domain models are technology-independent.

Domain models contain no I/O logic.

---

# 5. Module Rules

Each module has one responsibility.

Each domain concept has one owner.

Modules communicate only through documented Ports.

---

# 6. Extension Rules

Extensions implement Ports.

Extensions declare Capabilities.

Extensions must not access Core internals.

---

# 7. Error Handling Rules

Public operations produce a ProcessingOutcome.

Errors are propagated with context.

Errors are never silently ignored.

Warnings are not failures.

---

# 8. Data Transformation Rules

Every transformation has:

- one owner
- one input model
- one output model

Input models are never mutated.

---

# 9. Naming Rules

One concept.

One name.

No undocumented synonyms.

---

# 10. Forbidden Practices

The following are prohibited without architectural approval:

- Circular dependencies.
- Shared mutable domain state.
- Hidden global state.
- Undocumented public APIs.
- Business logic inside Infrastructure.
- Technology-specific code inside Domain.
- Catch-all "Utils" modules.
- Silent exception swallowing.

---

# 11. Evolution Rules

Architecture evolves through ADRs.

Breaking architectural changes require:

- documented motivation,
- impact analysis,
- migration strategy.

---

# 12. Stability

These rules are expected to remain stable throughout the lifetime of the project.