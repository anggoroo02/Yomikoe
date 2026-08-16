# Yomikoe Documentation

This directory contains the technical and project documentation for Yomikoe.

Yomikoe is an offline-first Japanese audio subtitle generator designed to
produce synchronized subtitles from Japanese audio while keeping the
transcription workflow local and modular.

## Documentation Structure

### Foundation

Documents that define the project's purpose, scope, and requirements.

- [Project Vision](/docs/architecture/01-foundation/project-vision.md)
- [Requirements Specification](/docs/architecture/01-foundation/requirements.md)

### Domain

Documents describing Yomikoe's domain concepts and processing flow.

- [Glossary](/docs/reference/glossary.md)
- [Processing Pipeline Specification](/docs/architecture/02-domain/processing-pipeline.md)

### Core

Documents describing the system's technical architecture and module
boundaries.

- [Architecture](/docs/architecture/03-core/extension-architecture.md)
- [Module Specification](/docs/architecture/03-core/module-specification.md)

### Governance

Documents that record project decisions and development conventions.

- [Development Workflow](/docs/development/development-workflow.md)
- [Testing Strategy](/docs/development/testing-strategy.md)
- [Architecture Decision Records](/docs/decisions/adr/README.md)

## Architecture Decisions

Architecture decisions are recorded as Architecture Decision Records (ADRs).

See the [ADR index](decisions/adr/README.md) for the current decision history.

Accepted decisions currently include:

- [ADR-001 — MVP Architecture Baseline](/docs/decisions/adr/ADR-001-mvp-architecture-baseline.md)
- [ADR-002 — Canonical Domain Terminology](/docs/decisions/adr/ADR-002-canonical-domain-terminology.md)

The glossary is the project's canonical dictionary, while ADRs are the source
of architectural decisions.

## Current Implementation

The current MVP implementation is a CLI-first transcription pipeline:

```text
Audio File
    │
    ▼
Audio Loader
    │
    ▼
Transcription Engine
    │
    ▼
TranscriptionResult
    │
    ▼
Subtitle Generator
    │
    ▼
SRT Writer
    │
    ▼
SRT File