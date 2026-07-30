# Ports & Contracts Specification

Version: 1.0

Status: Accepted

---

# 1. Purpose

This document defines the architectural contracts between logical modules.

Ports represent capabilities required by the core application.

Adapters provide concrete implementations of those capabilities.

The core application depends only on Ports.

---

# 2. Design Principles

Every Port shall:

- represent one capability
- remain technology-independent
- expose stable behavior
- hide implementation details
- be replaceable

Adapters may change.

Ports should remain stable.

---

# 3. Architectural Rule

Core
↓

Ports
↓

Adapters

Dependencies always point toward Ports.

Adapters never define system behavior.

They only implement required capabilities.

---

# 4. Core Ports

## AudioDecoderPort

Purpose:

Convert an Audio Source into a normalized Audio Stream.

Consumes:

Audio Source

Produces:

Audio Stream

---

## TranscriptionEnginePort

Purpose:

Convert Audio Stream into Transcription Result.

Consumes:

Audio Stream

Produces:

Transcription Result

---

## TranscriptNormalizerPort

Purpose:

Convert Transcription Result into Transcript.

Consumes:

Transcription Result

Produces:

Transcript

---

## SubtitleSerializerPort

Purpose:

Serialize Subtitle Document into a specific file format.

Consumes:

Subtitle Document

Produces:

Serialized Subtitle

---

## OutputWriterPort

Purpose:

Persist generated output.

Consumes:

Serialized Subtitle

Produces:

Output File

---

## ConfigurationProviderPort

Purpose:

Provide validated application configuration.

---

## LoggerPort

Purpose:

Provide diagnostic logging.

---

# 5. Contract Rules

Ports must:

- define behavior
- define expected inputs
- define expected outputs
- define possible failures

Ports must not:

- expose implementation details
- depend on concrete libraries
- require a specific engine

---

# 6. Adapter Rules

Adapters:

- implement one or more Ports
- contain technology-specific code
- may depend on external libraries
- must not contain business rules

Examples:

FFmpeg Decoder

Whisper.cpp Engine

Faster Whisper Engine

WebVTT Serializer

SRT Serializer

---

# 7. Error Model

Every Port returns one of:

Success

Recoverable Failure

Fatal Failure

Ports never terminate the application directly.

---

# 8. Versioning

Breaking changes to a Port require:

- architectural review
- version increment
- migration documentation

---

# 9. Stability

Ports are expected to remain stable for multiple releases.

Adapters may evolve independently.