# Glossary

Version: 2.0

Status: Accepted

---

## Adapter

A component that implements a Port using a specific technology.

Adapters belong to the technical boundary of the architecture and provide
concrete implementations for abstract Ports.

---

## Architecture Decision Record (ADR)

A permanent record of an accepted architectural decision.

ADRs document significant architectural decisions, their context, consequences,
and rationale.

ADRs are the authoritative source for architectural decisions.

---

## Capability

A declared feature or behavior supported by an Extension.

Capabilities describe what an Extension can provide without requiring callers
to depend on its concrete implementation.

---

## Domain Model

A technology-independent representation of business concepts.

Domain models should represent concepts and relationships rather than concrete
technology or infrastructure details.

---

## Engineering Proposal (EP)

A proposal describing an engineering idea before an architectural decision is
made.

An Engineering Proposal may be used to explore alternatives, requirements, or
implementation approaches before a decision is recorded as an ADR.

---

## Extension

A replaceable implementation that integrates with the Core through documented
Ports.

The Extension concept belongs to the broader target architecture and is not
required to have a formal discovery and registration system in the MVP.

---

## Module

A logical unit of responsibility within the architecture.

A Module should have a clear responsibility and a defined dependency boundary.

---

## Pipeline

The ordered sequence of processing stages used to transform an Audio input into
generated subtitle output.

In the MVP, the Pipeline is the primary processing orchestration boundary.

---

## PipelineResult

The result produced by the processing Pipeline.

`PipelineResult` represents the outcome of the complete MVP processing workflow,
rather than the result of an individual transcription engine.

It must not be confused with `TranscriptionResult`.

---

## Port

A stable interface owned by the Core architecture.

A Port defines a boundary through which the Core communicates with an external
or replaceable implementation.

Not every target-architecture Port is required to exist in the MVP.

---

## ProcessingJob

A conceptual representation of a single processing request.

`ProcessingJob` belongs to the broader target architecture and is not required
as a complete lifecycle abstraction in the MVP.

A future implementation may use `ProcessingJob` to represent processing
lifecycle, state, diagnostics, and related metadata.

---

## ProcessingOutcome

A future application-level representation of the outcome of a ProcessingJob.

It may eventually represent states such as:

- success
- failure
- partial success
- cancellation

`ProcessingOutcome` is not a canonical MVP result model.

It must not be used as a synonym for `PipelineResult`.

---

## Subtitle

The canonical MVP domain model representing generated subtitle content.

A `Subtitle` contains one or more `SubtitleCue` objects and exists before
serialization into a concrete subtitle format.

---

## SubtitleCue

The canonical MVP name for an individual timed subtitle item.

A `SubtitleCue` represents a piece of subtitle text associated with a start and
end time.

The canonical relationship is:

```
    Subtitle
        |
        +-- SubtitleCue[]
```

`SubtitleEntry` is not the canonical name for this concept.

---

## SubtitleDocument

A descriptive term for subtitle content as a document.

`SubtitleDocument` is not the canonical MVP source-code model name.

The canonical MVP model is `Subtitle`.

---

## Transcript

A normalized representation of recognized speech.

`Transcript` is reserved as a potential future domain model.

The MVP does not currently require a separate Transcript model between
`TranscriptionResult` and subtitle generation.

`Transcript` must therefore not be used as a synonym for
`TranscriptionResult`.

---

## Transcription

The process of converting audio into textual segments.

`Transcription` describes an operation rather than a data model.

The MVP transcription flow is:

```
    Audio
      |
      v
    TranscriptionEngine
      |
      v
    TranscriptionResult
```

---

## TranscriptionResult

The structured result returned by a TranscriptionEngine.

`TranscriptionResult` is the canonical MVP model for transcription engine
output.

It contains one or more `TranscriptionSegment` objects and represents the
result of an individual transcription engine rather than the result of the
complete processing Pipeline.

---

## TranscriptionSegment

An individual segment contained within a `TranscriptionResult`.

A `TranscriptionSegment` represents a timed portion of recognized speech and
contains, at minimum:

- start
- end
- text

`TranscriptionSegment` is the canonical MVP name for this concept.

`TranscriptSegment` is reserved for a possible future normalized Transcript
model and must not be used as a synonym for `TranscriptionSegment`.

---

## Transformation

A deterministic conversion from one domain model to another.

Every Transformation has one owner.

Examples may include converting transcription data into subtitle data or
converting a domain model into a serialization representation.

---

## Yomikoe

The official product name of this project.

Yomikoe is an offline-first Japanese audio subtitle generator designed around
modularity, free/open-source technologies, and replaceable processing
components.

---

## Terminology Status

The following terminology is canonical for the MVP:

| Concept                          | Canonical Name         | Status           |
| :------------------------------- | :--------------------- | :--------------- |
| Audio transcription operation    | `Transcription`        | MVP              |
| Engine transcription output      | `TranscriptionResult`  | MVP              |
| Individual transcription segment | `TranscriptionSegment` | MVP              |
| Subtitle model                   | `Subtitle`             | MVP              |
| Individual subtitle item         | `SubtitleCue`          | MVP              |
| Complete pipeline result         | `PipelineResult`       | MVP              |
| Normalized transcript            | `Transcript`           | Future           |
| Normalized transcript segment    | `TranscriptSegment`    | Future           |
| Processing request lifecycle     | `ProcessingJob`        | Future           |
| Processing operation outcome     | `ProcessingOutcome`    | Future           |
| Subtitle document                | `SubtitleDocument`     | Descriptive only |
| Subtitle item                    | `SubtitleEntry`        | Not canonical    |

---

## Documentation Authority

The Yomikoe documentation follows this distinction:

- **Glossary** defines the official meaning and usage of project terminology.
- **Architecture specifications** describe the intended structure and
  responsibilities of the system.
- **Architecture Decision Records (ADRs)** record authoritative architectural
  decisions and their rationale.
- **Implementation** represents the currently implemented behavior.

When terminology conflicts with an architectural decision, the relevant ADR
takes precedence and the Glossary should be updated accordingly.