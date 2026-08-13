# Domain Model

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines the canonical domain concepts used throughout Yomikoe.

The domain model establishes a shared vocabulary for developers, contributors,
documentation, and implementation.

The model distinguishes concepts required by the current MVP from concepts
defined by the target architecture.

---

# 2. Core Principles

Domain models represent project concepts independently of implementation
technologies.

They should remain independent of:

- programming language
- transcription engine
- subtitle format
- storage implementation
- user interface

The current MVP may use simpler representations where the corresponding
target-architecture domain model has not yet been implemented.

Such differences are intentional architectural gaps, not undocumented
exceptions.

---

# 3. Core Domain Concepts

## Audio Source

Represents an audio resource supplied by the user.

Examples:

- podcast
- audiobook
- lecture
- radio recording
- voice recording

Represents:

"What the user wants to process."

The current MVP represents the input through the loaded-audio abstraction.

---

## Processing Job

Represents one request to process one Audio Source.

A Processing Job is responsible for the lifecycle of one processing request.

The target architecture defines explicit job states and a
ProcessingOutcome.

The current MVP does not yet implement the complete Processing Job lifecycle.

---

## Audio Stream

Represents normalized audio data ready for transcription.

An Audio Stream is independent of the original audio file format.

The target architecture defines Audio Stream as the output of audio decoding.

The current MVP does not yet expose Audio Stream as an explicit domain model.

---

## Transcription Result

Represents the output produced by a transcription engine before normalization.

It may contain:

- recognized segments
- detected language
- engine-specific metadata
- engine-specific diagnostics

The exact contents may vary between transcription engines.

The current MVP uses `TranscriptionResult` as the primary transcription output.

---

## Transcript Segment

Represents one recognized portion of speech.

Contains:

- start timestamp
- end timestamp
- recognized text

A Transcript Segment represents recognized speech.

It is not a subtitle entry.

---

## Transcript

Represents normalized recognized speech as an ordered collection of
Transcript Segments.

A Transcript is the stable speech representation intended to separate
transcription from downstream subtitle generation.

The target architecture uses Transcript as the boundary between transcription
and subtitle generation.

The current MVP does not yet implement a separate Transcript model.

---

## Subtitle Entry

Represents one subtitle block.

Contains:

- index
- start time
- end time
- displayed text

A Subtitle Entry is intended for subtitle presentation rather than raw speech
recognition.

---

## Subtitle Document

Represents the complete subtitle content before serialization.

A Subtitle Document is independent of any specific subtitle file format.

The current MVP uses the subtitle model for this responsibility.

---

## Subtitle Format

Represents a serialization format for subtitle content.

Examples:

- SRT
- WebVTT

A format is not itself a domain document.

It defines how a Subtitle Document is represented externally.

---

## Serialized Subtitle

Represents subtitle content serialized into a specific subtitle format.

Examples:

- serialized SRT
- serialized WebVTT

The serialized representation is an output artifact rather than a domain model.

---

## Output File

Represents a persisted generated artifact.

The target architecture separates serialization from file persistence.

The current MVP writes the serialized subtitle directly to the filesystem.

---

# 4. Processing Relationships

The target architecture defines the following conceptual flow:

Audio Source
↓
Audio Stream
↓
Transcription Result
↓
Transcript
↓
Subtitle Document
↓
Serialized Subtitle
↓
Output File

The current MVP implements a narrower flow:

Audio Source
↓
Loaded Audio
↓
Transcription Result
↓
Subtitle
↓
SRT
↓
Output File

The difference between these flows represents the current MVP boundary and
target-architecture gap.

---

# 5. Transcription Engine

A Transcription Engine is a replaceable implementation responsible for speech
recognition.

It consumes the available audio input and produces a Transcription Result.

The architecture must not depend on a specific engine implementation.

The current MVP provides:

- `TranscriptionEngine`
- `DummyTranscriptionEngine`
- `FasterWhisperEngine`

---

# 6. Pipeline Stage

A Pipeline Stage represents one logical processing responsibility.

Examples include:

- audio loading
- transcription
- subtitle generation
- subtitle serialization
- output writing

Pipeline stages should have clearly defined inputs and outputs.

The target architecture may introduce additional explicit stages such as:

- audio decoding
- transcript normalization
- post-processing

These stages are not required to exist as separate implementations in the
current MVP.

---

# 7. Processing Result and Processing Outcome

## Processing Result

Processing Result represents a result produced by a processing operation.

The current MVP may expose narrower result models for individual operations.

It is not currently the canonical public operation outcome.

## Processing Outcome

ProcessingOutcome represents the complete outcome of a Processing Job.

It includes:

- execution status
- generated artifacts
- warnings
- diagnostics
- statistics

ProcessingOutcome belongs to the target architecture and is not yet fully
implemented by the MVP.

---

# 8. Domain Invariants

The following invariants apply to the architecture:

- Transcript is not a subtitle.
- Transcript Segment represents recognized speech.
- Subtitle Entry represents subtitle presentation.
- Subtitle Document is independent of a specific file format.
- Serialized Subtitle is an external representation of subtitle content.
- Audio Stream is independent of the original audio file format.
- A Processing Job represents one processing request.
- A Processing Job produces exactly one ProcessingOutcome in the target
  architecture.

---

# 9. Naming Rules

Yomikoe uses one canonical name for each domain concept.

Canonical terminology is defined by:

- `docs/reference/glossary.md`
- accepted Architecture Decision Records

Synonyms must not be introduced into implementation or documentation without
architectural review.

When an implementation uses a different technical name for an existing domain
concept, the relationship must be documented explicitly.

---

# 10. MVP Boundary

The current MVP intentionally does not implement every domain concept defined
by the target architecture.

In particular, the following remain target-architecture concepts:

- explicit Audio Stream
- explicit Transcript
- explicit Processing Job lifecycle
- explicit ProcessingOutcome
- explicit Serialized Subtitle model
- explicit Output File model

Their absence from the current implementation does not invalidate the domain
model.

Future implementation may introduce these concepts without changing their
canonical meaning.

---

# 11. Stability

The domain model is part of the architectural baseline.

Changes to canonical domain concepts or their relationships require
architectural review.