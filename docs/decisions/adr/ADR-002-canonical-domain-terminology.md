# ADR-002: Canonical Domain Terminology

* **Status:** Accepted
* **Date:** 2026-08-11
* **Decision Type:** Domain / Architecture
* **Scope:** MVP domain model and architecture documentation
* **Related:** ADR-001 MVP Architecture Baseline

---

## 1. Context

Yomikoe's architecture documentation and implementation currently use several
terms that overlap or have unclear boundaries.

Examples include:

* `TranscriptionResult`
* `Transcript`
* `TranscriptionSegment`
* `TranscriptSegment`
* `PipelineResult`
* `ProcessingResult`
* `ProcessingOutcome`
* `Subtitle`
* `SubtitleDocument`
* `SubtitleCue`
* `SubtitleEntry`

Some of these terms represent distinct architectural concepts, while others
appear to describe the same concept using different names.

This creates terminology drift between the architecture documentation and the
implementation.

Consistent terminology is particularly important because Yomikoe is intended
to be modular and contributor-friendly.

A contributor should be able to determine from a name:

* what the object represents;
* which module owns it;
* whether it is raw engine output or normalized domain data;
* whether it represents an intermediate processing result or final output;
* whether it belongs to transcription or subtitle generation.

The project therefore needs a canonical vocabulary.

---

## 2. Problem

Without canonical terminology, the same concept may be represented by different
names in different parts of the project.

For example:

```text
Documentation
    Transcript
        ↓
Implementation
    TranscriptionResult
```

or:

```text
Documentation
    Subtitle Document
        ↓
Implementation
    Subtitle
```

This creates unnecessary cognitive overhead and can lead to incorrect module
boundaries.

The project also risks introducing additional models simply because an existing
concept has been given another name.

The terminology must therefore be resolved before further architectural
refactoring.

---

## 3. Decision

Yomikoe will use a **canonical vocabulary** for the MVP.

The following terminology is established:

```text
Audio
Transcription
TranscriptionResult
TranscriptionSegment
Subtitle
SubtitleCue
PipelineResult
```

The terms:

```text
Transcript
TranscriptSegment
SubtitleDocument
SubtitleEntry
ProcessingResult
ProcessingOutcome
```

will not be used as alternative names for the above concepts in MVP
implementation or documentation.

Some of these terms may become valid concepts in the future architecture, but
they must not be introduced as synonyms for existing MVP concepts.

---

## 4. Transcription Terminology

### 4.1 Transcription

**Transcription** refers to the process of converting audio into textual
segments.

It is an operation, not a data model.

Example:

```text
Audio
  ↓
Transcription
  ↓
TranscriptionResult
```

---

### 4.2 TranscriptionResult

`TranscriptionResult` is the canonical name for the result returned by a
transcription engine in the MVP.

It represents the structured result produced by an implementation of
`TranscriptionEngine`.

Example:

```text
TranscriptionEngine
        │
        ▼
TranscriptionResult
```

The existing implementation of `TranscriptionResult` therefore remains the
canonical MVP model.

---

### 4.3 TranscriptionSegment

`TranscriptionSegment` is the canonical name for an individual segment inside
a `TranscriptionResult`.

A segment contains, at minimum:

```text
start
end
text
```

The relationship is:

```text
TranscriptionResult
    │
    └── TranscriptionSegment[]
```

The term `TranscriptSegment` will not be used as an alternative name.

---

## 5. Transcript Terminology

The term `Transcript` is **not a canonical MVP model**.

The current MVP does not require a separate normalized transcript domain model
between transcription and subtitle generation.

The MVP flow is therefore:

```text
Audio
  ↓
TranscriptionEngine
  ↓
TranscriptionResult
  ↓
Subtitle Generation
  ↓
Subtitle
```

A future architecture may introduce:

```text
TranscriptionResult
        ↓
Transcript Normalization
        ↓
Transcript
```

if there is a concrete requirement for a normalized transcript boundary.

Until that requirement exists, introducing `Transcript` would add an additional
model without sufficient architectural benefit.

Therefore:

> `Transcript` is reserved as a possible future domain concept and must not
> be used as a synonym for `TranscriptionResult`.

---

## 6. Subtitle Terminology

### 6.1 Subtitle

`Subtitle` is the canonical name for the subtitle document/model produced by
the subtitle generation stage.

The MVP relationship is:

```text
TranscriptionResult
        ↓
SubtitleGenerator
        ↓
Subtitle
```

A `Subtitle` contains one or more subtitle cues.

---

### 6.2 SubtitleCue

`SubtitleCue` is the canonical name for an individual subtitle entry.

The relationship is:

```text
Subtitle
   │
   └── SubtitleCue[]
```

A cue represents a timed piece of subtitle text.

At minimum, a cue contains:

```text
start
end
text
```

The term `SubtitleEntry` will not be used as an alternative name.

---

### 6.3 SubtitleDocument

`SubtitleDocument` is not a separate MVP model.

It may be used descriptively when discussing a subtitle file as a document,
but the canonical model name in source code is:

```text
Subtitle
```

Therefore:

```text
Subtitle Document
```

should not be introduced as another class representing the same concept.

---

## 7. Serialization Terminology

Serialization is the process of converting a `Subtitle` model into a concrete
output representation.

For example:

```text
Subtitle
    ↓
SRT serialization
    ↓
serialized SRT text
```

The MVP does not introduce a separate `SerializedSubtitle` model.

The SRT writer remains a concrete serialization implementation.

The architecture may later introduce:

```text
SubtitleSerializerPort
```

when multiple subtitle formats or replaceable serialization backends justify
the abstraction.

---

## 8. Pipeline Result Terminology

### 8.1 PipelineResult

`PipelineResult` is the canonical MVP name for the result returned by the
pipeline orchestration layer.

It represents the result of the Yomikoe processing workflow rather than the
result of a transcription engine.

The conceptual distinction is:

```text
TranscriptionResult
    │
    │ result of one transcription engine
    ▼

PipelineResult
    │
    │ result of the complete processing workflow
    ▼

Output
```

`PipelineResult` therefore belongs to the pipeline/application boundary rather
than the transcription engine boundary.

---

## 9. ProcessingResult

`ProcessingResult` is not a canonical MVP model.

The term is too broad to distinguish clearly between:

* engine output;
* pipeline output;
* final user-facing output.

The MVP will therefore use the more specific terms:

```text
TranscriptionResult
```

for engine output, and:

```text
PipelineResult
```

for pipeline output.

A future architecture may introduce a broader `ProcessingResult` if a concrete
use case requires a generalized processing abstraction.

Until then, `ProcessingResult` must not be introduced as a synonym for
`PipelineResult`.

---

## 10. ProcessingOutcome

`ProcessingOutcome` is reserved for a possible future application-level
operation result.

It may eventually represent concepts such as:

```text
Success
Failure
Partial Success
Cancelled
```

or other lifecycle states.

This concept is outside the current MVP domain model.

Therefore:

```text
ProcessingOutcome
```

is considered **Future** and must not be introduced into the MVP simply as
another name for `PipelineResult`.

---

## 11. Canonical Terminology Table

The following table defines the terminology for the MVP:

| Concept                          | Canonical Name         | Status        |
| -------------------------------- | ---------------------- | ------------- |
| Audio transcription operation    | Transcription          | MVP           |
| Engine transcription output      | `TranscriptionResult`  | Current / MVP |
| Individual transcription segment | `TranscriptionSegment` | Current / MVP |
| Normalized transcript            | `Transcript`           | Future        |
| Normalized transcript segment    | `TranscriptSegment`    | Future        |
| Subtitle model/document          | `Subtitle`             | Current / MVP |
| Individual subtitle item         | `SubtitleCue`          | Current / MVP |
| Subtitle document                | `SubtitleDocument`     | Not a model   |
| Subtitle item                    | `SubtitleEntry`        | Not canonical |
| Complete pipeline result         | `PipelineResult`       | Current / MVP |
| Generic processing result        | `ProcessingResult`     | Future        |
| Application processing outcome   | `ProcessingOutcome`    | Future        |

---

## 12. Domain Relationships

The canonical MVP data flow is:

```text
                    Audio
                      │
                      ▼
              TranscriptionEngine
                      │
                      ▼
           ┌─────────────────────┐
           │ TranscriptionResult │
           └──────────┬──────────┘
                      │
                      ▼
              SubtitleGenerator
                      │
                      ▼
               ┌────────────┐
               │  Subtitle  │
               └─────┬──────┘
                     │
                     │ contains
                     ▼
              SubtitleCue[]
                     │
                     ▼
                SRT Writer
                     │
                     ▼
                Output File
```

The pipeline wraps the processing flow:

```text
Audio
  │
  ▼
Pipeline
  │
  ├── Transcription
  │       └── TranscriptionResult
  │
  ├── Subtitle Generation
  │       └── Subtitle
  │
  ├── Serialization
  │       └── SRT
  │
  └── Output
          └── File

          ↓

     PipelineResult
```

---

## 13. Naming Rules

The following rules apply to future implementation and documentation.

### Rule 1 — One concept, one canonical name

Do not introduce a second name for an existing concept unless the concepts are
actually different.

### Rule 2 — Engine output is `TranscriptionResult`

Concrete transcription engines return:

```text
TranscriptionResult
```

They do not return `Transcript`.

### Rule 3 — Segments from engines are `TranscriptionSegment`

Individual engine result segments use:

```text
TranscriptionSegment
```

not:

```text
TranscriptSegment
```

unless a future normalized transcript model is introduced.

### Rule 4 — Subtitle model is `Subtitle`

The complete subtitle structure uses:

```text
Subtitle
```

not:

```text
SubtitleDocument
```

as a source-code model.

### Rule 5 — Individual subtitle items are `SubtitleCue`

Individual timed subtitle items use:

```text
SubtitleCue
```

not:

```text
SubtitleEntry
```

### Rule 6 — Pipeline output is `PipelineResult`

The result of the complete processing pipeline uses:

```text
PipelineResult
```

and must not be confused with:

```text
TranscriptionResult
```

### Rule 7 — Future terminology must not leak into MVP

Future concepts may be documented as future architecture, but should not be
used interchangeably with current MVP concepts.

---

## 14. Documentation Alignment

The following terminology should be updated in the architecture documentation:

`Transcript` should be used only when referring to the potential future
normalization boundary.

`Transcription Result` should refer to:

```text
TranscriptionResult
```

where the engine output is being discussed.

`Subtitle Entry` should be replaced with:

```text
SubtitleCue
```

when referring to the implementation model.

`Subtitle Document` should be replaced with:

```text
Subtitle
```

when referring to the MVP domain model.

Where `ProcessingResult` and `ProcessingOutcome` are currently presented as
implemented concepts, the documentation must clarify that they belong to the
future architecture unless an implementation is explicitly introduced.

---

## 15. Implementation Alignment

Following acceptance of this ADR:

1. Existing MVP models should retain their canonical names where possible.
2. Documentation should be updated to use the canonical terminology.
3. Duplicate conceptual models should not be introduced merely to match
   terminology in older documentation.
4. `PipelineResult` should be documented according to its actual MVP role.
5. Future `Transcript` and `ProcessingOutcome` concepts should remain
   explicitly marked as future.
6. Tests should use canonical model names.
7. Future architectural ADRs must use this terminology unless a new ADR
   explicitly changes it.

---

## 16. Consequences

### Positive Consequences

This decision:

* reduces terminology drift;
* makes module ownership clearer;
* prevents unnecessary duplicate models;
* improves contributor onboarding;
* makes architecture documentation easier to understand;
* establishes a stable vocabulary for tests and implementation;
* preserves room for future normalization and application-level concepts.

### Negative Consequences

Some existing architecture documentation will need to be updated.

Future introduction of a normalized `Transcript` model may require additional
mapping between:

```text
TranscriptionResult
        ↓
Transcript
```

The distinction between engine output and normalized domain data may therefore
require additional implementation when the architecture evolves.

This is intentional.

---

## 17. Future Evolution

If Yomikoe later requires a normalized transcript boundary, the architecture may
evolve to:

```text
Audio
  ↓
TranscriptionEngine
  ↓
TranscriptionResult
  ↓
TranscriptNormalizer
  ↓
Transcript
  ↓
SubtitleGenerator
  ↓
Subtitle
```

If Yomikoe later requires a generalized processing lifecycle, it may evolve to:

```text
Pipeline
  ↓
ProcessingResult
  ↓
ProcessingOutcome
```

Such changes should be introduced through a separate ADR rather than by silently
reusing or redefining existing terms.

---

## 18. Relationship to ADR-001

ADR-001 establishes that the MVP intentionally implements a smaller subset of
the target architecture.

This ADR defines the vocabulary used within that MVP boundary.

Together:

```text
ADR-001
MVP Architecture Baseline
        │
        ▼
Defines architectural scope
        │
        ▼
ADR-002
Canonical Domain Terminology
        │
        ▼
Defines vocabulary inside that scope
```

---

## 19. Decision Summary

Yomikoe will use the following canonical MVP terminology:

```text
Transcription
    ↓
TranscriptionResult
    ↓
TranscriptionSegment[]

Subtitle
    ↓
SubtitleCue[]

Pipeline
    ↓
PipelineResult
```

`Transcript`, `TranscriptSegment`, `ProcessingResult`, and
`ProcessingOutcome` remain future concepts and must not be used as synonyms for
the MVP models.

`SubtitleDocument` and `SubtitleEntry` are not canonical source-code model
names.

This vocabulary is intended to provide a stable foundation for subsequent
pipeline refactoring, testing, and contributor onboarding.

---

## 20. Status

**Accepted**

This ADR establishes the canonical terminology for the Yomikoe MVP.
