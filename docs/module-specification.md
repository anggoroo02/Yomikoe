# Module Specification

Version: 1.0

Status: Accepted

---

# 1. Purpose

This document defines the logical modules that compose the Japanese Audio Subtitle Generator.

Logical modules represent architectural responsibilities.

They do not prescribe source code layout or implementation details.

---

# 2. Module Principles

Every module:

- has one primary responsibility
- owns one area of the domain
- exposes a well-defined public interface
- hides internal implementation details
- communicates through stable contracts

Modules are architectural concepts.

They are not folders, packages, or namespaces.

---

# 3. Logical Modules

## 3.1 Application Module

### Responsibility

Acts as the public entry point of the system.

Coordinates user requests and manages processing jobs.

### Owns

- Processing Job lifecycle
- Application use cases
- Progress reporting
- Request validation

### Does Not Own

- Audio decoding
- Transcription
- Subtitle generation

---

## 3.2 Pipeline Module

### Responsibility

Coordinates execution of the processing pipeline.

### Owns

- Pipeline orchestration
- Stage execution order
- Stage communication
- Pipeline state

### Does Not Own

- Business logic of individual stages

---

## 3.3 Audio Module

### Responsibility

Handles audio-related concepts before transcription.

### Owns

- Audio Source
- Audio Stream
- Audio validation
- Audio decoding
- Audio normalization

### Does Not Own

- Speech recognition

---

## 3.4 Transcription Module

### Responsibility

Converts normalized audio into textual representations.

### Owns

- Transcription Engine abstraction
- Transcription Result
- Transcript
- Engine selection

### Does Not Own

- Subtitle generation
- File output

---

## 3.5 Subtitle Module

### Responsibility

Transforms transcripts into subtitle documents.

### Owns

- Subtitle Entry
- Subtitle Document
- Subtitle formatting
- Subtitle serialization

### Does Not Own

- Speech recognition

---

## 3.6 Configuration Module

### Responsibility

Provides application configuration.

### Owns

- Configuration loading
- Configuration validation
- Default values

---

## 3.7 Logging Module

### Responsibility

Produces diagnostic information.

### Owns

- Logging
- Diagnostics
- Processing statistics

---

## 3.8 Infrastructure Module

### Responsibility

Provides access to external systems.

### Owns

- Filesystem access
- External libraries
- Environment interaction

Infrastructure contains no business rules.

---

# 4. Dependency Rules

Application
→ Pipeline

Pipeline
→ Audio

Pipeline
→ Transcription

Pipeline
→ Subtitle

Application
→ Configuration

Application
→ Logging

Audio
→ Infrastructure

Transcription
→ Infrastructure

Subtitle
→ Infrastructure

Forbidden:

Audio
→ Subtitle

Subtitle
→ Audio

Transcription
→ Subtitle

Subtitle
→ Transcription

Infrastructure
→ Application

Infrastructure
→ Pipeline

---

# 5. Public Interfaces

Every module exposes only documented public interfaces.

Implementation details are private.

No module may depend on another module's internal implementation.

---

# 6. Module Ownership

Each domain concept has exactly one owning module.

Ownership must never be duplicated.

If ownership becomes unclear, architecture review is required.

---

# 7. Stability

Logical modules are expected to remain stable.

Implementation may evolve independently.

Module responsibilities should change only through an Architecture Decision Record (ADR).