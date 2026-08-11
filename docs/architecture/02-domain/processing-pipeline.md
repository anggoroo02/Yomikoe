# Processing Pipeline Specification

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines the logical processing pipeline used by Yomikoe.

It describes how input audio moves through the system and becomes a generated
subtitle file.

The document distinguishes the current MVP pipeline from the target
architecture.

It defines responsibilities and data flow, not implementation details.

---

# 2. Design Principles

Every processing stage should:

- perform one logical responsibility
- consume a well-defined input
- produce a well-defined output
- avoid unnecessary knowledge of other stages
- avoid modifying input models
- expose failures explicitly

The current MVP may combine responsibilities that are separate stages in the
target architecture.

Such combinations are intentional MVP simplifications.

---

# 3. Target Architecture Pipeline

The target architecture defines the following conceptual flow:

User Input
↓
Audio Validation
↓
Audio Decoding
↓
Transcription
↓
Transcript Normalization
↓
Post Processing
↓
Subtitle Generation
↓
Subtitle Serialization
↓
Output File

Each stage has a distinct responsibility.

---

# 4. Target Architecture Stage Descriptions

## Stage 1 — User Input

Responsibility:

Receive the user-provided Audio Source.

Output:

Audio Source.

---

## Stage 2 — Audio Validation

Responsibility:

Verify that the Audio Source can be processed.

Validation may include:

- file existence
- accessibility
- supported format
- required input invariants

Output:

Validated Audio Source.

---

## Stage 3 — Audio Decoding

Responsibility:

Convert the validated source into normalized audio suitable for transcription.

Possible operations include:

- sample rate normalization
- channel normalization
- PCM conversion

Output:

Audio Stream.

The transcription engine should not be responsible for arbitrary media-format
handling at the architecture boundary.

---

## Stage 4 — Transcription

Responsibility:

Convert speech into timestamped recognized speech.

Output:

Transcription Result.

The Transcription Engine is replaceable.

---

## Stage 5 — Transcript Normalization

Responsibility:

Convert engine-specific recognition output into the canonical Transcript
model.

Output:

Transcript.

This stage isolates engine-specific representation from downstream domain
processing.

---

## Stage 6 — Post Processing

Responsibility:

Apply optional deterministic transformations to the Transcript.

Possible operations include:

- whitespace cleanup
- punctuation normalization
- language-specific corrections
- confidence-based filtering

Output:

Processed Transcript.

Post processing is not required by the current MVP.

---

## Stage 7 — Subtitle Generation

Responsibility:

Transform a Transcript into a Subtitle Document.

Possible responsibilities include:

- subtitle timing
- line breaking
- subtitle numbering
- presentation constraints

Output:

Subtitle Document.

No file-format-specific serialization occurs at this stage.

---

## Stage 8 — Subtitle Serialization

Responsibility:

Serialize a Subtitle Document into a selected subtitle format.

Examples:

- SRT
- WebVTT

Output:

Serialized Subtitle.

---

## Stage 9 — File Output

Responsibility:

Persist the Serialized Subtitle as an Output File.

No transcription or subtitle-generation logic occurs at this stage.

---

# 5. Current MVP Pipeline

The current MVP intentionally uses a narrower pipeline:

Audio Source
↓
Audio Loading
↓
Transcription
↓
Subtitle Generation
↓
SRT Serialization
↓
Output File

The current implementation does not expose every target-architecture stage as
a separate abstraction.

In particular, the MVP does not yet implement explicit:

- Audio Stream
- Transcript normalization
- Post Processing
- Serialized Subtitle model
- Output File model
- Application-level pipeline orchestration

These are target-architecture capabilities rather than MVP requirements.

---

# 6. Current MVP Responsibilities

## Audio Loading

The MVP loads and validates the input audio and provides the information
required by the transcription engine.

This responsibility is currently implemented by the audio module.

The MVP does not yet expose the target-architecture Audio Stream model.

---

## Transcription

The MVP invokes a replaceable Transcription Engine.

The engine produces a `TranscriptionResult`.

Available implementations include:

- `DummyTranscriptionEngine`
- `FasterWhisperEngine`

---

## Subtitle Generation

The MVP converts the transcription result into the subtitle model used by the
current implementation.

The target architecture defines Transcript as the intended stable input to
this stage.

---

## SRT Serialization

The MVP serializes the generated subtitle model into SRT format.

The current implementation provides an SRT writer.

Additional subtitle formats are outside the current MVP scope.

---

## Output

The MVP writes the serialized SRT content to the filesystem.

A separate Output Writer abstraction is part of the target architecture but is
not required by the current MVP.

---

# 7. Pipeline Rules

The following rules apply to both the MVP and target architecture:

- Original user audio must not be modified by subtitle generation.
- Each stage must have a clearly defined responsibility.
- Stage failures must not silently disappear.
- Data passed between stages should use explicit models or contracts.
- Subtitle generation must not contain transcription-engine-specific logic.
- Subtitle serialization must not contain transcription logic.
- Output persistence must not contain subtitle-generation logic.

---

# 8. Error Handling

A pipeline failure terminates the current processing operation when recovery
is not safe.

Errors must preserve relevant context while propagating toward the operation
boundary.

The application must not silently ignore stage failures.

The original Audio Source must remain unchanged when processing fails.

---

# 9. Progress

Progress reporting belongs to the processing operation rather than to an
individual transcription engine.

The target architecture may report progress at stage boundaries.

Progress reporting is not yet part of the current MVP implementation.

---

# 10. Future Extensions

The architecture may introduce additional stages or transformations such as:

- Voice Activity Detection
- Speaker Diarization
- Subtitle Quality Enhancement
- Translation
- Subtitle Alignment
- Confidence Analysis

Future stages should extend the pipeline without introducing unnecessary
coupling between existing stages.

---

# 11. Stability

The logical pipeline is part of the architectural baseline.

Individual implementations may change while preserving the responsibilities
and contracts of the pipeline stages.

Changes to the logical pipeline require architectural review.