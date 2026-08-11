# Error Model & Result Specification

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines how failures are represented, propagated, and reported
throughout Yomikoe.

The objective is to establish a consistent error model across the application
while distinguishing the target architecture from the current MVP.

---

# 2. Principles

Errors are expected parts of processing.

Every public operation has two conceptual outcomes:

- Success
- Failure

Failures must not be silently swallowed.

Error information should remain available as it propagates through the
application.

The current MVP primarily uses exceptions, while the target architecture
defines a more explicit operation-result model.

---

# 3. Error Categories

## User Errors

Errors caused by invalid user input or command usage.

Examples:

- file not found
- invalid argument
- unsupported option

---

## Validation Errors

Errors caused by input or configuration that does not satisfy required
invariants.

Examples:

- invalid audio
- unsupported audio format
- unsupported subtitle format

---

## Infrastructure Errors

Errors caused by technical resources required by the application.

Examples:

- filesystem failure
- permission denied
- insufficient disk space
- unavailable external runtime dependency

---

## Engine Errors

Errors originating from a transcription engine.

Examples:

- model unavailable
- engine initialization failure
- transcription failure
- decoder failure within the engine

---

## Pipeline Errors

Errors caused by processing-stage execution or contract violations.

Examples:

- stage failure
- invalid transformation
- unexpected stage output

---

## Internal Errors

Unexpected implementation defects.

Internal errors indicate a software defect and should preserve sufficient
diagnostic information for debugging.

---

# 4. Error Ownership

Every error has one originating module.

The originating module is responsible for providing the initial error context.

Intermediate modules may:

- add context
- translate an error for a higher-level boundary
- classify an error

Intermediate modules must not silently discard the original failure
information.

---

# 5. Error Propagation

Errors propagate toward the current operation boundary.

A module may enrich an error with additional context, but it must preserve the
underlying cause whenever possible.

Errors must not be swallowed silently.

A processing failure should terminate only the current Processing Job when the
failure cannot be safely recovered.

The application itself should remain operational whenever possible.

---

# 6. User-Facing Errors

Internal errors and user-facing messages are separate concerns.

For example:

Internal diagnostic:

Decoder initialization failed because the required runtime dependency is
unavailable.

User-facing message:

Unable to process the selected audio.

User-facing messages should be:

- understandable
- actionable when possible
- free from unnecessary implementation details

Detailed diagnostics may be exposed through logging or verbose output.

---

# 7. Result Model

The target architecture defines public operations conceptually as producing one
of two outcomes:

Success

or

Failure

A successful operation contains its expected result.

A failed operation contains structured error information.

No third success/failure state is defined.

The exact result abstraction is an implementation concern and is not yet
implemented as a unified model in the current MVP.

---

# 8. Relationship to ProcessingOutcome

ProcessingOutcome represents the complete outcome of a Processing Job.

It is broader than an individual operation result.

A ProcessingOutcome may contain:

- execution status
- generated artifacts
- warnings
- diagnostics
- statistics

The target architecture uses ProcessingOutcome for terminal Processing Job
states.

The current MVP does not yet implement ProcessingOutcome as an explicit
domain model.

---

# 9. Recovery

Recoverable failures may allow processing to continue when doing so is safe.

Examples may include:

- optional metadata unavailable
- non-critical diagnostic information unavailable

Fatal failures terminate the current processing operation.

Recovery must never compromise the integrity of the original Audio Source or
produce partially valid output.

---

# 10. Logging

Failures should be loggable without modifying their semantic meaning.

Logging may provide:

- error category
- originating module
- operation context
- technical details
- diagnostic information

Logging is separate from error ownership and propagation.

The current MVP provides only limited logging and diagnostic behavior.

---

# 11. MVP Boundary

The current MVP primarily represents failures using exceptions and
module-specific exception classes.

The MVP does not yet provide a single unified result abstraction across all
public operations.

The target architecture may introduce:

- structured operation results
- standardized error metadata
- centralized error translation
- ProcessingOutcome
- richer diagnostics

These are implementation targets rather than requirements for the current MVP.

---

# 12. Stability

The error model is part of the architectural baseline.

Error categories, ownership rules, and propagation semantics should remain
stable even when individual implementations change.

Changes to the public error model require architectural review.