# Ports & Contracts Specification

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines the architectural Ports and Contracts used to isolate the
core application from replaceable implementations.

A Port defines a stable capability boundary.

An Adapter provides a concrete implementation of a Port.

The current MVP implements only a subset of the target Port architecture.

---

# 2. Design Principles

Every Port should:

- represent one capability
- remain independent of concrete technologies
- define stable behavior
- define explicit inputs and outputs
- define possible failures
- hide implementation details
- remain replaceable

Adapters may evolve independently from Ports.

---

# 3. Architectural Model

The target relationship is:

```text
Core
 ↓
Port
 ↓
Adapter
 ↓
Technology
```

The Core depends on the Port contract rather than a concrete technology.

Adapters implement the behavior required by Ports.

---

# 4. Core Ports

## AudioDecoderPort

### Purpose

Convert an Audio Source into normalized Audio Stream data.

### Input

Audio Source

### Output

Audio Stream

### MVP Status

Not yet implemented as an explicit Port.

---

## TranscriptionEnginePort

### Purpose

Convert available audio input into a Transcription Result.

### Input

Audio input

### Output

Transcription Result

### MVP Status

Implemented conceptually by the current `TranscriptionEngine` abstraction.

Concrete implementations include:

- `DummyTranscriptionEngine`
- `FasterWhisperEngine`

---

## TranscriptNormalizerPort

### Purpose

Convert a Transcription Result into the canonical Transcript model.

### Input

Transcription Result

### Output

Transcript

### MVP Status

Not yet implemented.

---

## SubtitleSerializerPort

### Purpose

Serialize a Subtitle Document into a selected subtitle format.

### Input

Subtitle Document

### Output

Serialized Subtitle

### MVP Status

The current MVP provides an SRT writer, but does not yet expose the complete
target Port abstraction.

---

## OutputWriterPort

### Purpose

Persist serialized subtitle content to an output destination.

### Input

Serialized Subtitle

### Output

Output File

### MVP Status

Not yet implemented as a separate Port.

---

## ConfigurationProviderPort

### Purpose

Provide validated application configuration.

### MVP Status

Target architecture concept.

---

## LoggerPort

### Purpose

Provide diagnostic logging.

### MVP Status

Target architecture concept.

---

# 5. Contract Rules

Ports define:

- accepted inputs
- produced outputs
- behavioral guarantees
- possible failures

Ports must not:

- expose concrete implementation details
- depend on a specific external library
- require a specific transcription engine
- contain technology-specific behavior

---

# 6. Adapter Rules

Adapters:

- implement one or more Ports
- contain technology-specific integration code
- may depend on external libraries
- translate external behavior into the Port contract
- must not contain unrelated business rules

Examples of possible adapters include:

- FFmpeg audio decoder
- Faster Whisper transcription adapter
- Whisper.cpp transcription adapter
- SRT serializer
- WebVTT serializer
- filesystem output writer

The existence of an adapter in this document does not imply that it is
currently implemented.

---

# 7. Error Contract

Ports must define how failures are exposed to their callers.

Failures should preserve:

- error category
- originating context
- relevant diagnostics

The target architecture may use structured operation results.

The current MVP primarily uses exceptions and module-specific exception classes.

Ports must not terminate the application directly.

---

# 8. Versioning

Breaking changes to a Port require:

- architectural review
- version increment where applicable
- migration documentation

Backward-compatible additions should avoid changing existing behavior.

---

# 9. MVP Boundary

The current MVP uses a simpler abstraction model.

Implemented or partially implemented boundaries include:

- transcription engine abstraction
- subtitle writer abstraction
- pipeline orchestration

The following remain target architectural abstractions:

- AudioDecoderPort
- TranscriptNormalizerPort
- SubtitleSerializerPort as a generalized format-independent Port
- OutputWriterPort
- ConfigurationProviderPort
- LoggerPort

The target Port model must not be interpreted as a claim that all Ports already
exist in the MVP implementation.

---

# 10. Stability

Ports and their contracts are part of the architectural baseline.

Adapters may change independently as long as they preserve the applicable Port
contract.

Changes to Port responsibilities, inputs, outputs, or failure semantics require
architectural review.
