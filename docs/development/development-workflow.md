# Development Workflow

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines the engineering workflow for Yomikoe.

The workflow prioritizes architectural consistency, maintainability, and
verification over implementation speed.

The workflow applies to both MVP development and future architectural work.

---

# 2. Workflow

The general development flow is:

Idea
↓

Discussion

↓

Architecture Review

↓

ADR (if required)

↓

Requirements or Specification Update

↓

Implementation

↓

Testing

↓

Documentation Update

↓

Review

↓

Release

Not every change requires every step.

Small implementation changes and bug fixes may follow a shorter path when they
do not affect requirements or architecture.

---

# 3. Feature Development

Every feature should begin with a clearly stated objective.

Before implementation:

- identify affected requirements
- identify affected architectural boundaries
- determine whether an ADR is required
- update relevant specifications when necessary

Features that change architectural decisions require an ADR before
implementation.

Implementation should remain within the accepted MVP boundary unless the
feature is explicitly approved as future architecture.

---

# 4. Bug Fixes

Bug reports should identify, when applicable:

- affected requirement
- affected module
- affected transformation
- affected test

Confirmed bugs should receive regression tests whenever practical.

Bug fixes should preserve existing behavior outside the affected defect.

---

# 5. Refactoring

Refactoring should preserve externally observable behavior unless a behavior
change is explicitly intended.

Architectural refactoring requires corresponding documentation updates and
architectural review.

Implementation details may change without architectural changes when public
behavior and contracts remain stable.

---

# 6. Documentation

Documentation is part of development.

Documentation should be updated when:

- behavior changes
- public interfaces change
- requirements change
- architectural decisions change
- terminology changes

Architecture documentation describes intended structure.

Implementation remains the authority for currently implemented behavior.

---

# 7. Reviews

Changes should be reviewed from two perspectives:

- architectural correctness
- implementation quality

Architectural review is required when a change affects:

- architectural boundaries
- public contracts
- domain ownership
- requirements
- accepted architectural decisions

Routine implementation changes do not require a new architectural decision.

---

# 8. Testing

Changes should be tested according to their scope.

At minimum:

- new behavior should have appropriate tests
- confirmed bugs should receive regression tests when practical
- architectural contracts should be tested where applicable
- the existing test suite should pass before release

The current MVP prioritizes unit, integration, and end-to-end verification of
implemented behavior.

Future architecture may introduce additional contract testing requirements.

---

# 9. Releases

A release is created only when:

- the intended release requirements are satisfied
- tests pass
- documentation is current
- architectural rules remain satisfied
- release notes or changelog information is updated as required

Future architectural capabilities are not release requirements unless they are
explicitly included in the release scope.

---

# 10. Continuous Improvement

The workflow may evolve as the project matures.

Changes to the workflow should be documented when they materially affect
engineering practice.

Changes that affect architectural governance require architectural review.

---

# 11. Stability

The development workflow is part of the engineering baseline.

Implementation practices may evolve while preserving the principles defined by
this document.