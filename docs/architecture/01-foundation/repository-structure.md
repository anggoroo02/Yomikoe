# Repository Structure Specification

Version: 1.1

Status: Accepted

---

# 1. Purpose

This document defines the physical organization of the Yomikoe repository.

The repository structure reflects architectural ownership and documentation hierarchy.

It does not prescribe internal implementation details beyond the repository level.

---

# 2. Repository Principles

The repository shall:

- separate architecture from implementation
- separate specifications from guides
- separate reference material from active design
- remain understandable to first-time contributors

---

# 3. Top-Level Layout

```
/
├── .github/
├── assets/
├── docs/
├── examples/
├── scripts/
├── src/
├── tests/
├── tools/
│
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
└── pyproject.toml
```

---

# 4. Documentation Layout

```
docs/
│
├── README.md
│
├── architecture/
│   ├── README.md
│   │
│   ├── 01-foundation/
│   │   ├── README.md
│   │   ├── architectural-rules.md
│   │   ├── project-vision.md
│   │   ├── repository-structure.md
│   │   └── requirements.md
│   │
│   ├── 02-domain/
│   │   ├── README.md
│   │   ├── data-transformation-specification.md
│   │   ├── domain-model.md
│   │   ├── error-model.md
│   │   ├── processing-job-lifecycle.md
│   │   └── processing-pipeline.md
│   │
│   ├── 03-core/
│   │   ├── README.md
│   │   ├── extension-architecture.md
│   │   ├── high-level-architecture.md
│   │   ├── module-specification.md
│   │   └── ports-and-contracts.md
│   │
│   └── 04-governance/
│       └── README.md
│
├── decisions/
│   └── adr/
│       ├── README.md
│       ├── ADR-001-mvp-architecture-baseline.md
│       └── ADR-002-canonical-domain-terminology.md
│
├── development/
│   ├── development-workflow.md
│   ├── engineering-standards.md
│   ├── release-strategy.md
│   └── testing-strategy.md
│
├── diagrams/
│
├── engineering/
│
├── reference/
│
└── specifications/
    ├── codex/
    ├── implementation/
    └── milestones/
```

The documentation areas have distinct purposes:

- `architecture/` — architectural models, rules, and system specifications.
- `decisions/` — accepted architectural decisions recorded as ADRs.
- `development/` — contributor and development guidance.
- `diagrams/` — visual representations of the system and architecture.
- `engineering/` — engineering proposals and technical planning.
- `reference/` — stable reference material such as terminology and supported capabilities.
- `specifications/` — detailed implementation and planning specifications.

---

# 5. Source Layout

`src/`

Contains implementation only.

Architecture documentation does not belong here.

---

# 6. Tests Layout

`tests/`

Organized to mirror architectural ownership rather than internal implementation details whenever practical.

---

# 7. Assets

Contains non-source assets:

- diagrams
- logos
- screenshots
- sample media (where licensing permits)

---

# 8. Examples

Contains example usage and sample workflows.

No production implementation belongs here.

---

# 9. Scripts

Contains automation scripts only.

Business logic does not belong here.

---

# 10. Stability

Repository organization evolves conservatively.

Frequent restructuring should be avoided.