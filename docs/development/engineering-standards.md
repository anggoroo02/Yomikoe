# Engineering Standards

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines engineering standards for implementing Yomikoe.

The objective is to keep implementation aligned with the accepted architecture
while avoiding unnecessary complexity.

---

# 2. Design Philosophy

Implementation follows architecture.

When implementation pressure conflicts with an accepted architectural rule,
the conflict should be resolved through architectural review rather than by
silently weakening the architecture.

The MVP should remain as simple as possible while satisfying its requirements.

---

# 3. SOLID

The project follows SOLID principles whenever practical.

Priority is given to:

- Single Responsibility
- Dependency Inversion

Other principles should be applied when they improve maintainability.

SOLID is a guideline, not a goal by itself.

---

# 4. Composition

Prefer composition over inheritance.

Inheritance should only be introduced when it represents a clear and useful
"is-a" relationship.

---

# 5. Dependency Injection

Dependencies should be provided from the outside when practical.

Modules should avoid unnecessarily constructing their own collaborators.

Dependency injection should not introduce abstraction that is not justified by
the current architecture.

---

# 6. Public APIs

Public APIs should remain:

- small
- documented
- stable

Breaking changes to established public contracts require appropriate review.

MVP implementations are not required to expose future architectural
interfaces before they are needed.

---

# 7. Domain Integrity

Domain models should:

- contain no I/O
- contain no framework-specific behavior
- represent business concepts
- avoid unnecessary mutation

Domain models should remain independent from infrastructure concerns.

---

# 8. Side Effects

Side effects should be isolated from domain logic.

Business logic should remain deterministic whenever practical.

Filesystem, process, external library, and environment interaction should remain
at appropriate technical boundaries.

---

# 9. Configuration

Configuration should be provided through explicit dependencies or application
boundaries.

Global mutable configuration should be avoided.

---

# 10. Logging

Logging is an infrastructure concern.

Business logic should not depend on logging implementation details.

Logging may record diagnostic information without changing the semantic meaning
of an operation or error.

---

# 11. Error Handling

The current MVP primarily uses exceptions and module-specific exception
classes to represent failures.

Expected failure behavior should remain explicit and meaningful.

`PipelineResult` represents the result of the current MVP processing workflow.

`ProcessingOutcome` belongs to the target architecture and is not required as an
explicit MVP model.

Exceptions should preserve useful error context and should not be silently
swallowed.

---

# 12. Documentation

Public components should document, when applicable:

- purpose
- responsibilities
- public behavior
- usage notes

Architecture documentation has priority over redundant implementation comments.

---

# 13. Testing

Code should be testable by design.

Tests should focus on observable behavior and stable contracts rather than
implementation details.

A component that is unnecessarily difficult to test may indicate excessive
coupling or unclear responsibility.

---

# 14. Simplicity

Prefer the simplest implementation that satisfies the current requirements and
architectural constraints.

Avoid speculative abstraction.

Future architecture should not be implemented merely because it is described
in architectural documentation.

---

# 15. Stability

Engineering standards evolve conservatively.

Changes that materially affect architectural practice should receive appropriate
architectural review and documentation updates.