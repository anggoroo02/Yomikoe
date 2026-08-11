# Domain

## Purpose

This section defines the canonical domain concepts and processing behavior of
Yomikoe.

Domain documentation describes what the system means and how processing is
conceptually performed.

It should remain independent of specific implementation technologies whenever
possible.

---

## Scope

The documents in this directory define:

- domain concepts
- processing stages
- processing job lifecycle
- data transformations
- error behavior

These documents describe the target architectural model while explicitly
identifying differences from the current MVP where necessary.

---

## Documents

### Domain Model

`domain-model.md`

Defines the canonical domain concepts and their relationships.

### Processing Pipeline

`processing-pipeline.md`

Defines the logical processing stages from input audio to generated subtitle
output.

### Processing Job Lifecycle

`processing-job-lifecycle.md`

Defines the conceptual lifecycle and state transitions of a Processing Job.

### Data Transformation Specification

`data-transformation-specification.md`

Defines the conceptual transformations between domain models and their
responsibilities.

### Error Model

`error-model.md`

Defines error categories, ownership, propagation, recovery, and the
relationship between errors and processing outcomes.

---

## Recommended Reading Order

For understanding the domain from the beginning:

1. `domain-model.md`
2. `processing-pipeline.md`
3. `processing-job-lifecycle.md`
4. `data-transformation-specification.md`
5. `error-model.md`

---

## MVP Boundary

The domain documentation describes the architectural target.

The current MVP intentionally implements only a subset of these concepts.

MVP-specific boundaries are documented within the relevant documents rather
than by redefining the canonical domain terminology.

---

## Stability

Domain concepts and their canonical terminology are part of the architectural
baseline.

Changes to domain concepts, relationships, or terminology require architectural
review.