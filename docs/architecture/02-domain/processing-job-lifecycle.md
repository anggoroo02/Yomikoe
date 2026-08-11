# Processing Job Lifecycle Specification

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines the lifecycle of a Processing Job in Yomikoe.

A Processing Job represents one request to process one Audio Source.

The lifecycle describes the conceptual execution states of a processing request
and the rules governing transitions between those states.

The document distinguishes the target architecture from the current MVP.

---

# 2. Design Principles

A Processing Job:

- represents exactly one processing request
- has one current lifecycle state
- progresses through explicit state transitions
- produces one ProcessingOutcome when it reaches a terminal state
- remains independent from any specific transcription engine

The current MVP does not yet expose the complete Processing Job lifecycle as an
explicit domain abstraction.

The lifecycle defined here is therefore the target architectural model.

---

# 3. Lifecycle States

The target architecture defines the following states:

Created
↓
Validated
↓
Queued
↓
Running
↓
Completed

Alternative terminal states:

Running
↓
Failed

Running
↓
Cancelled

---

# 4. State Definitions

## Created

The Processing Job has been instantiated.

Input and configuration have not yet been validated.

---

## Validated

The input Audio Source and required processing configuration have been
validated.

The job is eligible for execution.

---

## Queued

The Processing Job has been accepted for execution but has not started
processing.

Queueing is primarily relevant to future batch or scheduled processing.

The current MVP processes one request directly and does not require an
explicit queue state.

---

## Running

The Processing Job is actively executing its processing pipeline.

Progress may be reported while the job is in this state.

---

## Completed

The Processing Job finished successfully.

A successful ProcessingOutcome is available.

---

## Failed

The Processing Job terminated because of an unrecoverable failure.

A failed ProcessingOutcome records the relevant error and diagnostics.

---

## Cancelled

The Processing Job was intentionally stopped before successful completion.

A cancelled ProcessingOutcome records the cancellation and relevant
diagnostics.

Cancellation is a target-architecture capability and is not required by the
current MVP.

---

# 5. Valid State Transitions

The following transitions are valid:

Created
→ Validated

Validated
→ Queued

Queued
→ Running

Running
→ Completed

Running
→ Failed

Running
→ Cancelled

No other state transitions are defined by the current architecture.

---

# 6. Terminal States

The following states are terminal:

- Completed
- Failed
- Cancelled

A terminal Processing Job does not transition to another state.

If processing must be attempted again, a new Processing Job is created.

---

# 7. Processing Outcome

Every terminal Processing Job produces exactly one ProcessingOutcome.

ProcessingOutcome represents the complete result of the processing request.

It records:

- execution status
- generated artifacts
- warnings
- diagnostics
- statistics

The outcome must provide enough information for the caller to determine whether
the processing request succeeded and what was produced.

The current MVP does not yet implement ProcessingOutcome as an explicit
domain model.

---

# 8. Progress Reporting

Progress reporting is meaningful only while a Processing Job is Running.

Progress may describe:

- current processing stage
- stage progress
- overall progress
- optional estimated remaining time

Progress information must not change the lifecycle state by itself.

The current MVP does not yet implement a complete job-level progress model.

---

# 9. Error Handling

An unrecoverable processing failure transitions the job from Running to Failed.

The failure must be represented in the resulting ProcessingOutcome.

Errors should preserve:

- originating context
- error category
- relevant diagnostics

A failed job must not modify the original Audio Source.

---

# 10. Retry

Retrying a failed or cancelled job creates a new Processing Job.

The previous job remains immutable for diagnostic purposes.

A retry must not mutate the lifecycle history of the previous job.

---

# 11. Batch Processing

A batch is a collection of independent Processing Jobs.

Each Processing Job maintains its own lifecycle and ProcessingOutcome.

A future batch coordinator may be responsible for:

- creating jobs
- scheduling jobs
- tracking job states
- reporting aggregate progress

Batch processing is outside the current MVP scope.

---

# 12. MVP Boundary

The current MVP does not yet implement an explicit Processing Job state
machine.

The current execution is conceptually equivalent to:

Input
↓
Validate / Load
↓
Run Pipeline
↓
Success or Failure

The MVP does not currently expose:

- explicit `ProcessingJob`
- explicit lifecycle states
- explicit `ProcessingOutcome`
- explicit queue management
- cancellation
- job-level retry management
- batch coordination
- persistent job history

These capabilities belong to the target architecture and may be implemented
incrementally in future development.

---

# 13. Relationship to the Processing Pipeline

A Processing Job owns one execution of the processing pipeline.

Conceptually:

Processing Job
↓
Processing Pipeline
↓
Processing Outcome

The Processing Job lifecycle describes the execution state.

The Processing Pipeline specification describes the processing stages.

These are related but distinct concepts.

---

# 14. Stability

The Processing Job lifecycle is part of the architectural baseline.

Individual implementation details may evolve while preserving the defined
lifecycle semantics.

Changes to lifecycle states, transitions, or outcome semantics require
architectural review.