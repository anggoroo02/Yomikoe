# Processing Job Lifecycle Specification

Version: 1.0

Status: Accepted

---

# 1. Purpose

This document defines the lifecycle of a Processing Job.

A Processing Job represents one processing request for one Audio Source.

Batch processing is represented as multiple independent Processing Jobs.

---

# 2. Design Principles

A Processing Job:

- has exactly one owner
- has exactly one current state
- progresses through explicit state transitions
- produces one ProcessingOutcome

State transitions are deterministic.

---

# 3. State Machine

Created
    ↓
Validated
    ↓
Queued
    ↓
Running
    ↓
Completed

Possible alternative terminal states:

Running
    ↓
Failed

Running
    ↓
Cancelled

---

# 4. State Definitions

## Created

The job has been instantiated.

No validation has occurred.

---

## Validated

Input and configuration have been verified.

The job is eligible for execution.

---

## Queued

The job is waiting for execution.

---

## Running

Pipeline execution is in progress.

---

## Completed

Processing finished successfully.

A ProcessingOutcome is available.

---

## Failed

Processing terminated due to an unrecoverable failure.

A ProcessingOutcome describing the failure is available.

---

## Cancelled

Execution was intentionally stopped.

The ProcessingOutcome records the cancellation.

---

# 5. Transition Rules

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

No other transitions are allowed.

---

# 6. Progress Reporting

Progress is reported only while the job is Running.

Completed, Failed, and Cancelled are terminal states.

---

# 7. Retry

Retry creates a new Processing Job.

Previous jobs remain immutable for diagnostic purposes.

---

# 8. Batch Processing

A batch consists of multiple independent Processing Jobs.

Each job maintains its own lifecycle.

The batch coordinator is responsible for scheduling jobs.

---

# 9. Outcome

Every terminal state produces one ProcessingOutcome.

The outcome records:

- execution status
- generated artifacts
- warnings
- diagnostics
- statistics

---

# 10. Stability

The lifecycle is considered part of the public architecture.

Changes require architectural review.