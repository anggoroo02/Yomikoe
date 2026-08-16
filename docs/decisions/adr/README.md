# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for Yomikoe.

ADRs document significant architectural decisions that affect the structure,
behavior, or long-term direction of the project.

They provide historical context for why a decision was made, what alternatives
were considered, and what consequences the decision introduces.

---

## What belongs here?

An ADR should be created when a decision:

* affects the system architecture;
* establishes or changes an architectural boundary;
* introduces or removes an important abstraction;
* affects module responsibilities or dependencies;
* establishes a long-term technical direction;
* resolves a significant architectural ambiguity.

ADRs should not be used for every implementation detail or routine code change.

---

## ADR Lifecycle

Each ADR follows this lifecycle:

```text
Proposed
   │
   ▼
Accepted
   │
   ▼
Superseded / Deprecated
```

### Proposed

The decision is being discussed and has not yet been accepted.

### Accepted

The decision is currently valid and should be followed by implementation.

### Superseded

The decision has been replaced by a newer ADR.

The superseding ADR should reference the previous decision.

### Deprecated

The decision is no longer applicable, but remains useful as historical
documentation.

---

## ADR Format

ADRs should contain, where applicable:

1. Title
2. Status
3. Date
4. Context
5. Problem
6. Decision
7. Consequences
8. Alternatives considered
9. Implementation or migration notes
10. Related decisions or documents

The exact structure may vary depending on the complexity of the decision.

---

## Naming Convention

ADR files use the following naming convention:

```text
ADR-NNN-short-description.md
```

Examples:

```text
ADR-001-mvp-architecture-baseline.md
ADR-002-canonical-domain-terminology.md
ADR-003-transcription-engine-boundary.md
```

The numeric identifier is assigned sequentially.

---

## Current ADRs

| ID                                                                     | Decision                     | Status   |
| :--------------------------------------------------------------------- | :--------------------------- | :------- |
| [ADR-001](/docs/decisions/adr/ADR-001-mvp-architecture-baseline.md)    | MVP Architecture Baseline    | Accepted |
| [ADR-002](/docs/decisions/adr/ADR-002-canonical-domain-terminology.md) | Canonical Domain Terminology | Accepted |

---

## Relationship to Architecture Documentation

Architecture specifications describe the intended structure and responsibilities
of Yomikoe.

ADRs document the decisions that establish, constrain, or change that structure.

In general:

```text
Architecture Specifications
        │
        │ describe
        ▼
Architectural Structure
        ▲
        │ influenced by
        │
Architecture Decision Records
```

An ADR may therefore reference architecture specifications, while architecture
specifications may reference an ADR when a particular design decision requires
additional historical context.

---

## Guidelines

When adding or changing an architectural decision:

1. Check existing ADRs for related decisions.
2. Explain the problem before documenting the solution.
3. Prefer explicit trade-offs over absolute statements.
4. Avoid documenting implementation details that do not affect architecture.
5. Update related architecture documentation when necessary.
6. If a decision replaces an existing ADR, explicitly mark the relationship.
7. Keep the ADR focused on the decision rather than the implementation process.

ADRs are historical records. Once accepted, they should generally not be rewritten
to hide the original reasoning. If a decision changes, create a new ADR and
supersede the previous one.
