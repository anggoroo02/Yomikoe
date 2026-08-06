# Domain Model

Version: 1.0

Status: Accepted

---

# 1. Purpose

This document defines the core domain concepts used throughout the project.

The goal is to establish a consistent vocabulary shared by developers, contributors, documentation, and implementation.

---

# 2. Core Principles

Domain models represent business concepts.

They are independent of:

- programming language
- transcription engine
- subtitle format
- storage implementation
- user interface

---

# 3. Domain Entities

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

---

## Processing Job

Represents one execution request.

A processing job contains:

- input audio
- configuration
- selected transcription engine
- output destination

Represents:

"What the application is currently doing."

---

## Audio Stream

Represents normalized audio ready for transcription.

Produced by:

Audio Decoder

Consumed by:

Transcription Engine

---

## Transcript Segment

Represents recognized speech.

Contains:

- start timestamp
- end timestamp
- recognized text

Represents speech only.

It is NOT a subtitle.

---

## Transcript

An ordered collection of Transcript Segments.

Represents complete recognition output.

---

## Transcription Result

Represents the raw output produced by a transcription engine.

A Transcription Result may contain:

- transcript segments
- confidence scores
- token-level timestamps
- detected language
- engine metadata
- processing duration
- engine-specific diagnostics

This model is considered an intermediate domain object.

It isolates engine-specific details from the rest of the application.

The remainder of the processing pipeline should consume a normalized Transcript rather than engine-specific output whenever possible.

---

## Subtitle Entry

Represents one subtitle block.

Contains:

- index
- start time
- end time
- displayed text

---

## Subtitle Document

Represents the complete subtitle before serialization.

Independent from SRT or WebVTT.

---

## Subtitle Format

Represents a serialization target.

Examples:

- SRT
- WebVTT

---

## Transcription Engine

Represents a speech recognition implementation.

It consumes Audio Stream.

It produces Transcript.

---

## Pipeline Stage

Represents one logical processing step.

Examples:

- Decoder
- Transcription
- Serializer

---

## Processing Result

Represents the final outcome.

Contains:

- success/failure
- generated files
- statistics
- diagnostics

---

# 4. Domain Relationships

Audio Source

↓

Processing Job

↓

Audio Stream

↓

Transcription Engine

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

---

# 5. Invariants

Transcript is never a subtitle.

Subtitle Document is independent of file format.

Audio Stream is independent of audio file format.

Processing Job owns the pipeline execution.

Pipeline Stages are stateless whenever possible.

---

# 6. Naming Rules

One concept.

One name.

One definition.

No synonyms should be introduced into implementation without architectural review.

---

# 7. Stability

These domain concepts are expected to remain stable over the lifetime of the project.

Implementation details may change.

Domain terminology should not.