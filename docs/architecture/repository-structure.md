# Repository Structure Specification

Version: 1.0

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

/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── pyproject.toml
├── docs/
├── src/
├── tests/
├── scripts/
├── assets/
├── examples/
└── tools/

---

# 4. Documentation Layout

docs/
│
├── architecture/
│   ├── project-vision.md
│   ├── requirements-specification.md
│   ├── processing-pipeline.md
│   ├── high-level-architecture.md
│   ├── domain-model.md
│   ├── module-specification.md
│   ├── ports-and-contracts.md
│   ├── extension-architecture.md
│   ├── data-transformation-specification.md
│   ├── error-model.md
│   ├── processing-job-lifecycle.md
│   └── architectural-rules.md
│
├── adr/
│   ├── ADR-0001.md
│   ├── ADR-0002.md
│   └── ...
│
├── specifications/
│   ├── codex/
│   ├── milestones/
│   └── implementation/
│
├── development/
│   ├── coding-standards.md
│   ├── testing-strategy.md
│   ├── development-workflow.md
│   └── release-process.md
│
└── reference/
    ├── glossary.md
    ├── capabilities.md
    └── supported-formats.md

---

# 5. Source Layout

src/

Contains implementation only.

Architecture documentation does not belong here.

---

# 6. Tests Layout

tests/

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