# Engineering Standards

Version: 1.0

Status: Accepted

---

# 1. Purpose

This document defines engineering standards for implementing Yomikoe.

The objective is to ensure every implementation remains aligned with the project's architecture.

---

# 2. Design Philosophy

Implementation follows architecture.

Architecture never follows implementation.

When implementation pressure conflicts with architectural rules, architectural review is required.

---

# 3. SOLID

The project follows SOLID principles whenever practical.

Priority is given to:

- Single Responsibility
- Dependency Inversion

Other principles are applied when they improve maintainability.

SOLID is a guideline, not a goal by itself.

---

# 4. Composition

Prefer composition over inheritance.

Inheritance should only be introduced when it models a true "is-a" relationship.

---

# 5. Dependency Injection

Dependencies shall be provided from the outside.

Modules should not construct their own collaborators whenever practical.

---

# 6. Public APIs

Public APIs must remain:

- small
- documented
- stable

Breaking changes require architectural review.

---

# 7. Domain Integrity

Domain models:

- contain no I/O
- contain no framework dependencies
- remain immutable
- represent business concepts only

---

# 8. Side Effects

Side effects should be isolated.

Business logic should remain deterministic whenever possible.

---

# 9. Configuration

Configuration shall be injected.

Global mutable configuration is prohibited.

---

# 10. Logging

Logging is an infrastructure concern.

Business logic must not depend on logging behavior.

---

# 11. Error Handling

Operations return ProcessingOutcome.

Exceptions are reserved for unexpected implementation failures.

Expected failures are represented explicitly.

---

# 12. Documentation

Every public component shall have:

- purpose
- responsibilities
- usage notes

Architecture documentation has priority over implementation comments.

---

# 13. Testing

Code shall be testable by design.

Implementation that cannot be tested usually indicates architectural issues.

---

# 14. Simplicity

Prefer the simplest implementation that satisfies the architectural requirements.

Avoid speculative abstraction.

---

# 15. Stability

Engineering standards evolve conservatively.

Changes require architectural review.