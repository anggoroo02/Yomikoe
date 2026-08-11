# Data Transformation Specification

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines the conceptual transformations between the domain models
used by Yomikoe.

Transformations describe how data moves between processing stages.

The document distinguishes the target architecture from the current MVP
implementation.

---

# 2. Transformation Principles

Every transformation should:

- consume a well-defined input
- produce a well-defined output
- avoid mutating input models
- validate required invariants
- expose failure explicitly
- have one logical owner

Transformations should be deterministic whenever technically possible.

The current MVP may combine multiple target transformations within a single
implementation component.

---

# 3. Target Architecture Transformation Flow

The target architecture defines the following conceptual transformations:

File Path
↓
Audio Source
↓
Validated Audio Source
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

Each transformation has a distinct responsibility.

---

# 4. Transformation Definitions

## File Path → Audio Source

Owner:

Audio Module

Purpose:

Represent the user-selected input as an Audio Source.

The transformation should establish the identity of the resource without
performing transcription or subtitle processing.

---

## Audio Source → Validated Audio Source

Owner:

Audio Module

Purpose:

Verify that the Audio Source is accessible and supported.

Validation may include:

- existence
- readability
- supported format
- required input invariants

---

## Validated Audio Source → Audio Stream

Owner:

Audio Module

Purpose:

Decode and normalize the validated audio into a representation suitable for
transcription.

Possible normalization includes:

- sample rate normalization
- channel normalization
- PCM conversion

Output:

Audio Stream.

The current MVP does not yet expose this transformation as an explicit
domain-level operation.

---

## Audio Stream → Transcription Result

Owner:

Transcription Module

Purpose:

Perform speech recognition using a selected Transcription Engine.

Output:

Transcription Result.

The concrete engine implementation must remain replaceable.

---

## Transcription Result → Transcript

Owner:

Transcription Module

Purpose:

Normalize engine-specific recognition output into the canonical Transcript
model.

This transformation isolates engine-specific details from downstream
processing.

The current MVP does not yet implement a separate Transcript model.

---

## Transcript → Subtitle Document

Owner:

Subtitle Module

Purpose:

Transform recognized speech into subtitle content.

Possible responsibilities include:

- subtitle timing
- line breaking
- subtitle numbering
- presentation constraints

Output:

Subtitle Document.

---

## Subtitle Document → Serialized Subtitle

Owner:

Subtitle Module

Purpose:

Serialize subtitle content into a selected subtitle format.

Examples:

- SRT
- WebVTT

Output:

Serialized Subtitle.

---

## Serialized Subtitle → Output File

Owner:

Infrastructure Module

Purpose:

Persist serialized subtitle content to the selected output destination.

No subtitle-generation logic belongs in this transformation.

---

# 5. Current MVP Transformations

The current MVP implements a narrower transformation flow:

File Path
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

The current implementation combines or omits several target transformations.

In particular, the MVP does not yet expose separate transformations for:

- Audio Source → Validated Audio Source
- Validated Audio Source → Audio Stream
- Transcription Result → Transcript
- Subtitle Document → Serialized Subtitle
- Serialized Subtitle → Output File

The MVP still satisfies its current acceptance boundary without requiring these
target abstractions.

---

# 6. Transformation Ownership

Each transformation has one logical owner.

Ownership determines:

- validation responsibility
- transformation rules
- failure handling
- contract maintenance

Ownership must not be duplicated across modules.

---

# 7. Invariants

Every transformation should:

- validate its preconditions
- preserve the input model
- produce a complete output model
- expose possible failures
- preserve relevant error context

A failed transformation must not produce partially valid output.

The original Audio Source must remain unchanged.

---

# 8. Failure Rules

A transformation failure terminates the current processing operation when
recovery is not safe.

Failures should preserve:

- originating module
- error category
- relevant diagnostics
- transformation context

Intermediate modules may add context but must not silently discard the
original failure information.

---

# 9. Future Transformations

The architecture may introduce additional transformations such as:

Audio Stream
↓
Noise-Reduced Audio Stream

Transcript
↓
Aligned Transcript

Transcript
↓
Translated Transcript

Subtitle Document
↓
Quality-Enhanced Subtitle Document

Future transformations should extend existing contracts rather than modify
unrelated transformations.

---

# 10. Stability

Transformation contracts are part of the architectural baseline.

Implementation details may evolve while preserving the logical transformation
responsibilities.

Changes to transformation ownership, inputs, outputs, or invariants require
architectural review.