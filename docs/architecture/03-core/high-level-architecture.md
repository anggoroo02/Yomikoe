# High-Level Architecture

Version: 1.0

Status: Accepted

---

# 1. Overview

The Japanese Audio Subtitle Generator is organized as a layered, modular architecture.

The design separates user interfaces, application orchestration, processing pipeline, and infrastructure.

Each layer has a single responsibility.

Dependencies always point downward.

Lower layers never depend on higher layers.

---

# 2. Architectural Layers

┌──────────────────────────────┐
│ User Interfaces              │
│ CLI                          │
│ Future GUI                   │
│ Future REST API              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Application Layer            │
│ Use Cases                    │
│ Job Coordination             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Pipeline Orchestrator        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Processing Modules           │
│ Validation                   │
│ Decoder                      │
│ Transcription                │
│ Post Processing              │
│ Subtitle Generator           │
│ Serializer                   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Infrastructure               │
│ File System                  │
│ External Libraries           │
│ Logging                      │
│ Configuration                │
└──────────────────────────────┘

---

# 3. Layer Responsibilities

## User Interface Layer

Responsibilities:

- Receive user input.
- Display progress.
- Display errors.
- Present results.

Must not contain business logic.

---

## Application Layer

Responsibilities:

- Validate requests.
- Build processing jobs.
- Invoke the Pipeline Orchestrator.
- Return results.

This layer exposes the public API of the application.

---

## Pipeline Orchestrator

Responsibilities:

- Execute pipeline stages in order.
- Pass data between stages.
- Handle recoverable failures.
- Report progress.

This is the only component allowed to coordinate processing stages.

---

## Processing Modules

Each module performs exactly one transformation.

Modules communicate only through defined data contracts.

Modules never invoke each other directly.

---

## Infrastructure Layer

Provides technical capabilities such as:

- filesystem access
- audio decoding libraries
- logging
- configuration loading

Infrastructure must never contain business rules.

---

# 4. Dependency Rules

Allowed:

UI
→ Application

Application
→ Pipeline Orchestrator

Pipeline Orchestrator
→ Processing Modules

Processing Modules
→ Infrastructure (only when required)

Forbidden:

Processing Module
→ Processing Module

Infrastructure
→ Application

Infrastructure
→ UI

Engine
→ Serializer

Serializer
→ Engine

---

# 5. Core Architectural Principles

- Single Responsibility
- Explicit Data Flow
- Engine Independence
- Offline First
- Replaceable Components
- Public Interfaces Only
- Stable Contracts
- Minimal Coupling

---

# 6. Extension Strategy

Future features should be introduced by adding new modules or replacing existing implementations.

Existing module boundaries should remain stable.

Examples:

- new transcription engine
- additional subtitle format
- subtitle editor
- translation module
- speaker diarization

These extensions should not require redesigning the architecture.

---

# 7. Stability

The architecture is intended to remain stable across future releases.

Implementation details may evolve.

Module responsibilities should not.