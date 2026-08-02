# Codex Implementation Specification

Version: 1.0

Status: Accepted

---

# Purpose

This document defines the required structure for every implementation specification provided to Codex.

Implementation specifications translate architectural decisions into executable engineering tasks.

Codex implements.

Architecture remains the responsibility of the Technical Lead.

---

# Required Sections

Every implementation specification shall contain:

## 1. Identifier

Example:

IMP-0007

---

## 2. Title

Short implementation title.

---

## 3. Objective

Describe the intended engineering outcome.

---

## 4. Scope

Clearly define what is included.

Clearly define what is excluded.

---

## 5. References

List all applicable documents.

Examples:

- Requirements
- ADRs
- Module Specification
- Ports
- Engineering Standards

---

## 6. Preconditions

Implementation assumptions.

Required completed milestones.

Dependencies.

---

## 7. Allowed Modifications

List files that may be modified.

---

## 8. Forbidden Modifications

List files that must not change.

---

## 9. Implementation Tasks

Ordered engineering tasks.

Each task should be independently reviewable.

---

## 10. Acceptance Criteria

Observable behavior.

Not implementation details.

---

## 11. Testing Requirements

Required:

- Unit Tests
- Contract Tests
- Integration Tests

As applicable.

---

## 12. Documentation Updates

Required documentation changes.

---

## 13. Definition of Done

Implementation is complete only when:

- acceptance criteria satisfied
- tests pass
- documentation updated
- architecture unchanged