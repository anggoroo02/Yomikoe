# Domain

## Purpose

This section describes the business domain of Yomikoe.

It explains how audio moves through the system and how the application models transcription and subtitle generation.

---

## Scope

The documents in this directory answer questions such as:

- What concepts exist in the domain?
- How is audio processed?
- What processing stages exist?
- How are errors represented?
- How is data transformed between stages?

These documents describe the problem domain rather than software implementation.

---

## Contains

- `domain-model.md`
- `processing-pipeline.md`
- `processing-job-lifecycle.md`
- `data-transformation-specification.md`
- `error-model.md`

---

## Recommended Reading Order

1. Domain Model
2. Processing Pipeline
3. Processing Job Lifecycle
4. Data Transformation Specification
5. Error Model

---

## Notes

Domain documents should remain independent of implementation technologies whenever possible.