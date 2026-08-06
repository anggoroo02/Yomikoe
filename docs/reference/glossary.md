# Glossary

Version: 1.0

Status: Accepted

---

## Adapter

A component that implements a Port using a specific technology.

---

## Architecture Decision Record (ADR)

A permanent record of an accepted architectural decision.

---

## Capability

A declared feature or behavior supported by an Extension.

---

## Domain Model

A technology-independent representation of business concepts.

---

## Engineering Proposal (EP)

A proposal describing an engineering idea before an architectural decision is made.

---

## Extension

A replaceable implementation that integrates with the Core through documented Ports.

---

## Module

A logical unit of responsibility within the architecture.

---

## Pipeline

The ordered sequence of processing stages from Audio Source to generated subtitle.

---

## Port

A stable interface owned by the Core architecture.

---

## ProcessingJob

A single request to process one Audio Source.

Each ProcessingJob produces exactly one ProcessingOutcome.

---

## ProcessingOutcome

The complete outcome of a ProcessingJob.

Includes:

- execution status
- generated artifacts
- warnings
- diagnostics
- statistics

---

## SubtitleDocument

A domain model representing subtitle content before serialization.

---

## Transcript

A normalized representation of recognized speech.

---

## TranscriptionResult

The engine-specific recognition output before normalization into a Transcript.

---

## Transformation

A deterministic conversion from one domain model to another.

Every Transformation has one owner.

---

## Yomikoe

The official product name of this project.