# High-Level Architecture

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines the high-level software architecture of Yomikoe.

It describes the architectural boundaries between user interfaces,
application orchestration, processing modules, and infrastructure.

The document distinguishes the target architecture from the current MVP
implementation.

---

# 2. Architectural Model

Yomikoe uses a modular architecture organized around explicit responsibilities
and replaceable components.

The target architecture separates:

- User Interface
- Application
- Pipeline
- Processing Modules
- Infrastructure

The current MVP implements a narrower subset of these boundaries.

---

# 3. Target Architecture

The target architecture is conceptually organized as follows:

```text
┌──────────────────────────────┐
│ User Interface               │
│ CLI / Future GUI / API       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Application                  │
│ Use Cases / Job Coordination │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Pipeline                     │
│ Processing Orchestration     │
└──────────────┬───────────────┘
               │
       ┌───────┼─────────────────────┐
       ▼       ▼                     ▼
┌──────────┐ ┌──────────────┐ ┌──────────────┐
│ Audio    │ │ Transcription│ │ Subtitle     │
│ Module   │ │ Module       │ │ Module       │
└────┬─────┘ └──────┬───────┘ └──────┬───────┘
     │              │                │
     └──────────────┼────────────────┘
                    ▼
          ┌─────────────────────┐
          │ Infrastructure      │
          │ Files / Libraries   │
          │ Environment         │
          └─────────────────────┘
```

The exact implementation may evolve while preserving these architectural
responsibilities.

---

# 4. Layer Responsibilities

## User Interface

Responsibilities:

- receive user input
- invoke application use cases
- display progress
- display errors
- present results

The User Interface must not contain core processing logic.

The current MVP provides a CLI.

Future interfaces may include a GUI or other application frontends.

---

## Application

Responsibilities:

- expose application use cases
- validate processing requests
- create and manage Processing Jobs
- invoke pipeline execution
- report results

The Application layer coordinates use cases but does not implement individual
processing stages.

The current MVP has not yet implemented the complete target Application layer.

---

## Pipeline

Responsibilities:

- execute processing stages
- maintain stage order
- pass data between stages
- coordinate processing progress
- propagate failures

The Pipeline owns orchestration.

Individual processing modules must not coordinate other processing modules
directly.

The current MVP provides pipeline orchestration but does not implement every
target pipeline abstraction.

---

## Processing Modules

Processing modules implement individual processing responsibilities.

Examples include:

- Audio
- Transcription
- Subtitle

Each module should expose explicit contracts and hide implementation details.

---

## Infrastructure

Infrastructure provides technical capabilities required by the application.

Examples include:

- filesystem access
- external libraries
- runtime dependencies
- environment interaction
- logging
- configuration sources

Infrastructure must not contain domain or application business rules.

---

# 5. Dependency Rules

The target dependency direction is:

```text
User Interface
      ↓
Application
      ↓
Pipeline
      ↓
Processing Modules
      ↓
Infrastructure
```

Processing modules may depend on infrastructure capabilities through documented
Ports and Adapters.

The following dependencies are forbidden:

```text
Processing Module → Processing Module
Infrastructure → Application
Infrastructure → Pipeline
Infrastructure → User Interface
Transcription → Subtitle
Subtitle → Transcription
```

Processing stages communicate through explicit data models and contracts rather
than direct implementation coupling.

---

# 6. Core Architectural Principles

The architecture follows these principles:

- Single Responsibility
- Explicit Data Flow
- Engine Independence
- Offline First
- Replaceable Components
- Stable Contracts
- Minimal Coupling
- Public Interfaces
- Testable Boundaries

These principles are part of the architectural baseline.

---

# 7. Extension Strategy

New capabilities should normally be introduced by:

- adding a new implementation behind an existing Port
- adding a new module when a new responsibility is required
- extending an existing contract only when necessary

Examples include:

- additional transcription engines
- additional subtitle formats
- audio-processing capabilities
- future translation
- future speaker diarization

Extensions must not bypass established architectural boundaries.

---

# 8. Current MVP Boundary

The current MVP intentionally implements a smaller architecture.

The implemented path is conceptually:

```text
CLI
 ↓
Audio Loading
 ↓
Transcription Engine
 ↓
Subtitle Generation
 ↓
SRT Writer
 ↓
Output File
```

The MVP does not yet implement every target layer as an explicit abstraction.

In particular, the following remain architectural targets:

- complete Application use-case layer
- explicit Audio Stream boundary
- explicit Transcript normalization boundary
- complete Port and Adapter infrastructure
- explicit Output Writer abstraction
- complete Processing Job lifecycle
- complete ProcessingOutcome model

The absence of these abstractions from the MVP does not change their canonical
architectural meaning.

---

# 9. Stability

The high-level architecture is part of the architectural baseline.

Implementation details may evolve while preserving the defined boundaries and
dependency direction.

Changes to architectural layers or dependency rules require architectural
