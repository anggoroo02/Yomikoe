# Development Workflow

Version: 1.0

Status: Accepted

---

# 1. Purpose

This document defines the official engineering workflow for Yomikoe.

The workflow prioritizes architectural consistency over implementation speed.

---

# 2. Workflow

Idea
↓

Discussion

↓

Architecture Review

↓

ADR (if required)

↓

Requirements Update

↓

Implementation Specification

↓

Implementation

↓

Architecture Review

↓

Testing

↓

Documentation Update

↓

Release

---

# 3. Feature Development

Every feature should begin with a clearly stated objective.

If the feature changes architecture, an ADR is required before implementation.

Implementation begins only after requirements and specifications are approved.

---

# 4. Bug Fixes

Bug reports should identify:

- affected requirement
- affected module
- affected transformation
- affected test (if applicable)

Confirmed bugs should receive regression tests whenever practical.

---

# 5. Refactoring

Refactoring shall preserve externally observable behavior unless explicitly approved.

Architectural refactoring requires documentation updates.

---

# 6. Documentation

Documentation is updated as part of development.

Documentation is not a post-development activity.

---

# 7. Reviews

Every implementation is reviewed from two perspectives:

- architectural correctness
- implementation quality

Architectural correctness takes precedence.

---

# 8. Releases

A release is created only when:

- requirements are satisfied
- tests pass
- documentation is current
- architectural rules remain satisfied

---

# 9. Continuous Improvement

The workflow itself may evolve.

Changes require architectural review and documentation updates.