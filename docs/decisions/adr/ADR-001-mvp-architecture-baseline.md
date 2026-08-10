# ADR: MVP Architecture Baseline

* **Status:** Accepted
* **Date:** 2026-08-10
* **Decision Type:** Architecture
* **Scope:** MVP implementation
* **Related Areas:** Application, Pipeline, Audio, Transcription, Subtitle, CLI

---

## 1. Context

Yomikoe is designed as an offline-first Japanese audio subtitle generator.

The project's architecture documentation defines a modular system with clear
module boundaries, domain concepts, ports, adapters, infrastructure, pipeline
orchestration, and future extension capabilities.

The current implementation, however, intentionally represents a smaller MVP
architecture.

The implemented repository currently provides:

* CLI entry point
* Audio inspection and loading
* Transcription engine abstraction
* Dummy transcription engine
* Faster-Whisper transcription engine
* Transcription result models
* Subtitle generation
* SRT serialization
* Partial pipeline orchestration

The accepted architecture describes additional components that are not yet
implemented, including:

* Application Layer
* AudioDecoderPort
* TranscriptNormalizerPort
* SubtitleSerializerPort
* OutputWriterPort
* ConfigurationProviderPort
* LoggerPort
* ProcessingOutcome and processing lifecycle
* Extension discovery and registration
* Progress and job lifecycle infrastructure
* Future GUI and API interfaces

Implementing all of these components before the MVP is complete would introduce
additional abstraction and complexity without being required by the current
processing workflow.

At the same time, allowing the implementation to diverge indefinitely from the
documented architecture would make the repository difficult to understand and
contribute to.

A clear architectural baseline is therefore required.

---

## 2. Problem

The project currently has two architectural levels:

1. A broader target architecture described by the architecture documentation.
2. A smaller architecture represented by the current MVP implementation.

Without an explicit boundary between these two levels, contributors may assume
that every component described in the target architecture must already exist
in the codebase.

This can lead to:

* premature abstraction;
* unnecessary implementation work;
* confusion about module responsibilities;
* inconsistent terminology;
* difficulty understanding which architectural rules apply to the MVP;
* unnecessary refactoring before feature development can continue.

The project therefore needs an explicit MVP architecture baseline.

---

## 3. Decision

Yomikoe will use a **deliberately reduced architecture for the MVP**.

The MVP architecture will preserve the project's core modular boundaries and
existing useful abstractions while deferring architectural components that are
not yet required.

The target architecture remains valid as the long-term architectural direction,
but it is not considered fully implemented by the MVP.

The distinction between architecture levels is therefore:

```text
Target Architecture
        │
        ├── MVP Architecture
        │
        └── Future Architecture
```

The MVP will prioritize:

1. clear module ownership;
2. pipeline-centered orchestration;
3. replaceable transcription engines;
4. stable domain models;
5. testability;
6. simple CLI interaction;
7. minimal unnecessary abstraction.

---

## 4. MVP Architectural Boundary

The MVP processing flow is defined as:

```text
User
 │
 ▼
CLI
 │
 │ request
 ▼
Pipeline
 │
 ├── Audio
 │
 ├── Transcription
 │
 ├── Subtitle Generation
 │
 ├── Serialization
 │
 └── Output
 │
 ▼
Result
```

The CLI is responsible for user interaction and argument handling.

The Pipeline is responsible for coordinating the processing workflow.

Processing modules remain responsible for their respective domain or technical
responsibilities.

The CLI must not become the primary location for processing orchestration.

---

## 5. Current Components

The following components are already implemented and remain part of the MVP:

### 5.1 CLI

The CLI is the primary user interface for the MVP.

Responsibilities include:

* parsing command-line arguments;
* validating user-facing input;
* invoking the processing workflow;
* displaying results and diagnostics.

The CLI should not own the internal processing sequence.

---

### 5.2 Audio

The Audio module currently provides:

* audio metadata inspection;
* supported-format validation;
* audio loading;
* audio-related models and exceptions.

The current MVP does not require a complete audio decoding abstraction.

The existing implementation may therefore remain simpler than the target
AudioDecoderPort architecture.

---

### 5.3 Transcription

The Transcription subsystem provides a replaceable engine abstraction.

The current implementation includes:

```text
TranscriptionEngine
        │
        ├── DummyTranscriptionEngine
        │
        └── FasterWhisperEngine
```

This abstraction is considered an important MVP boundary because multiple engine
implementations already exist.

The transcription subsystem produces a `TranscriptionResult`.

---

### 5.4 Subtitle

The Subtitle subsystem is responsible for converting transcription data into
subtitle-oriented structures and preparing them for serialization.

The MVP currently supports SRT serialization.

The existing subtitle model and naming will be aligned with the canonical
terminology defined by subsequent architectural decisions.

---

### 5.5 SRT Writer

SRT output is an MVP requirement.

The existing SRT writer remains a concrete implementation.

A generic `SubtitleSerializerPort` is not required solely for the MVP.

Additional subtitle formats may later justify introducing a formal serializer
port.

---

### 5.6 Pipeline

The Pipeline is an MVP component and is the primary processing orchestration
boundary.

The Pipeline will coordinate the stages required to transform an input audio
file into subtitle output.

The current partial implementation will be aligned with this responsibility.

The intended MVP direction is:

```text
Pipeline
 ├── Audio processing
 ├── Transcription
 ├── Subtitle generation
 ├── SRT serialization
 └── Output handling
```

The Pipeline should coordinate these stages without absorbing the internal
business logic of individual modules.

---

## 6. MVP Abstractions

Only abstractions that provide a concrete architectural benefit to the MVP
will be required.

### Required

The following abstraction is already justified:

```text
TranscriptionEngine
```

It has multiple concrete implementations:

```text
DummyTranscriptionEngine
FasterWhisperEngine
```

This makes engine replacement and testing practical.

### Not Required Yet

The following abstractions remain deferred:

```text
AudioDecoderPort
TranscriptNormalizerPort
SubtitleSerializerPort
OutputWriterPort
ConfigurationProviderPort
LoggerPort
```

Their absence from the MVP implementation does not invalidate the target
architecture.

They will only be introduced when a concrete requirement justifies them.

---

## 7. Application Layer

A dedicated Application Layer is part of the target architecture but is not
required for the initial MVP.

The MVP may use:

```text
CLI
 ↓
Pipeline
```

instead of:

```text
CLI
 ↓
Application
 ↓
Pipeline
```

A dedicated Application Layer may be introduced when multiple user interfaces
or application-level use cases justify it, for example:

```text
CLI
GUI
REST API
   │
   ▼
Application
   │
   ▼
Pipeline
```

Until that need exists, introducing the layer would add indirection without
sufficient benefit.

---

## 8. Ports and Adapters

The target architecture uses a broader Ports and Adapters model.

For the MVP, the architecture will use a **selective abstraction strategy**.

Existing abstractions with demonstrated value will be retained.

New ports will not be introduced solely to make the implementation match the
target architecture diagram.

The following principle applies:

> An abstraction should be introduced when it protects a meaningful boundary,
> enables substitution, improves testing, or solves a concrete architectural
> problem.

This means the MVP may contain concrete implementations where the target
architecture eventually expects adapters.

---

## 9. Infrastructure

The target architecture defines Infrastructure as a distinct architectural
concern.

The current MVP does not require a complete Infrastructure package.

Technical dependencies may remain within their current feature-oriented
modules while the architecture is stabilized.

Examples include:

```text
Mutagen
Faster-Whisper
CTranslate2
Filesystem output
```

These may later be reorganized behind explicit adapters when the need for
stronger isolation or replaceability arises.

---

## 10. Processing Results and Outcomes

The target architecture contains broader concepts such as:

```text
ProcessingResult
ProcessingOutcome
```

while the current implementation contains:

```text
PipelineResult
TranscriptionResult
```

These concepts are not assumed to be interchangeable.

Their relationships and canonical terminology must be resolved before the
corresponding abstractions are expanded.

The MVP will avoid introducing a complete processing-outcome system until its
behavioral requirements are clearly established.

The existence of `PipelineResult` in the implementation must therefore be
treated as an MVP implementation detail pending terminology alignment.

---

## 11. Progress Reporting

Progress reporting is considered an MVP capability because transcription can be
a long-running operation.

The initial implementation should favor a simple mechanism such as:

* progress callbacks;
* progress events;
* CLI progress display.

A complete job lifecycle or event infrastructure is not required.

The MVP should therefore provide useful progress information without introducing
the full processing-job architecture.

---

## 12. Configuration

Configuration is an MVP capability, but a formal
`ConfigurationProviderPort` is not required yet.

Configuration may initially be provided through:

```text
CLI options
 ↓
Engine / Pipeline configuration
```

A dedicated configuration abstraction may be introduced when configuration
sources become more complex.

Examples include:

* configuration files;
* environment variables;
* multiple interfaces;
* persistent user configuration;
* engine-specific configuration providers.

---

## 13. Logging and Diagnostics

Logging and diagnostics are MVP capabilities.

The implementation may use Python's standard logging facilities.

A formal `LoggerPort` is deferred until the project has a concrete need for
replaceable logging backends or stronger architectural isolation.

The MVP should prioritize useful diagnostics over logging abstraction.

---

## 14. Extension System

Yomikoe's target architecture includes a formal extension model with:

* discovery;
* validation;
* capability inspection;
* registration;
* lifecycle management.

This system is **Future** for the MVP.

The existing transcription engine abstraction already provides a useful
extension boundary:

```text
TranscriptionEngine
        │
        ├── DummyTranscriptionEngine
        └── FasterWhisperEngine
```

A formal plugin discovery and registration mechanism will only be introduced
when external extensions become a real project requirement.

---

## 15. Future Architecture

The following components remain part of the long-term architectural direction:

```text
Application Layer
Full Ports and Adapters
AudioDecoderPort
TranscriptNormalizerPort
SubtitleSerializerPort
OutputWriterPort
ConfigurationProviderPort
LoggerPort
ProcessingOutcome
Processing Job lifecycle
Extension discovery and registration
Advanced progress/event infrastructure
GUI
REST API
```

These components are not considered MVP blockers.

Their architectural documentation may remain in the repository as long-term
design guidance, provided that their implementation status is clear.

---

## 16. Architectural Status Model

Architecture documentation should distinguish implementation status using the
following model:

### CURRENT

Implemented and actively used by the repository.

### MVP

Required for the MVP and must be stabilized before the MVP is considered
complete.

### FUTURE

Intentionally deferred architectural capability.

A component marked `FUTURE` must not be treated as a missing MVP feature.

---

## 17. Consequences

### Positive Consequences

This decision:

* keeps the MVP implementation small;
* prevents premature abstraction;
* preserves the existing modular architecture;
* gives contributors a clear understanding of current scope;
* allows the target architecture to evolve incrementally;
* reduces unnecessary refactoring;
* makes testing easier by focusing on stable boundaries;
* provides a clear distinction between architectural intent and implementation
  status.

### Negative Consequences

The MVP will temporarily be less abstract than the target architecture.

Some infrastructure concerns will remain inside feature modules.

Some target ports will not yet exist.

The MVP may therefore require future refactoring when:

* additional engines are introduced;
* additional subtitle formats are required;
* multiple interfaces are introduced;
* configuration becomes more complex;
* external extensions become supported.

These trade-offs are intentional.

---

## 18. Migration Principle

Future architectural improvements should be introduced incrementally.

The project should not attempt to implement the entire target architecture in a
single refactoring effort.

Instead:

```text
Concrete Requirement
        │
        ▼
Architectural Pressure
        │
        ▼
Small Boundary
        │
        ▼
Port / Adapter / Abstraction
        │
        ▼
Test
        │
        ▼
Document
```

Architecture should evolve in response to real requirements and demonstrated
complexity.

---

## 19. Implementation Alignment Required After This ADR

Following acceptance of this ADR, the repository should be aligned with the
MVP baseline in the following order:

1. Establish canonical terminology.
2. Move processing orchestration from the CLI into the Pipeline.
3. Keep the CLI focused on user interaction.
4. Clarify the role of `PipelineResult`.
5. Add or improve progress reporting.
6. Add appropriate logging and diagnostics.
7. Add tests around the stabilized module boundaries.
8. Update architecture documentation to clearly distinguish Current, MVP, and
   Future components.

No full Ports and Adapters refactor is required as part of this alignment.

---

## 20. Non-Goals

This ADR does not:

* redefine the complete Yomikoe architecture;
* remove the existing target architecture;
* require implementation of every documented Port;
* introduce a plugin system;
* introduce a GUI;
* introduce a REST API;
* introduce a job queue;
* require a dedicated Application Layer;
* require complete infrastructure isolation;
* define the final domain terminology.

Those decisions may be addressed by separate ADRs when required.

---

## 21. Relationship to Other Architecture Documents

This ADR establishes the implementation scope of the MVP.

The existing architecture documents continue to describe the broader architectural
direction.

In case of ambiguity between the target architecture and MVP implementation
scope, this ADR defines which target components are intentionally deferred.

More specific architectural decisions should be documented through additional
ADRs rather than silently changing this baseline.

---

## 22. Decision Summary

Yomikoe will **not** implement its entire target architecture as part of the
MVP.

The MVP will retain the following core structure:

```text
CLI
 │
 ▼
Pipeline
 │
 ├── Audio
 ├── Transcription
 ├── Subtitle
 ├── Serialization
 └── Output
```

The existing `TranscriptionEngine` abstraction will remain a primary extension
boundary because it already supports multiple implementations.

Other ports, application layers, infrastructure abstractions, extension
registration, processing lifecycle, and additional interfaces will be
introduced incrementally when justified by concrete requirements.

The target architecture remains the long-term direction.

The MVP is intentionally a smaller, testable, and contributor-friendly subset
of that architecture.

---

## 23. Status

**Accepted**

This ADR establishes the baseline for subsequent MVP implementation and
repository cleanup work.
