# Release Strategy & Versioning

Version: 2.0

Status: Accepted

---

# 1. Purpose

This document defines the release philosophy and versioning strategy for
Yomikoe.

The objective is to provide predictable releases while preserving
long-term maintainability.

---

# 2. Versioning

Yomikoe follows Semantic Versioning (SemVer):

MAJOR.MINOR.PATCH

Examples:

0.1.0

1.0.0

1.2.3

---

# 3. Pre-1.0 Releases

Versions below 1.0 are considered evolving.

Pre-1.0 status does not justify poor engineering practices.

Architectural discipline, testing, and documentation remain important throughout
development.

---

# 4. Stable Release

Version 1.0.0 represents a stable MVP release.

A 1.0.0 release is expected to provide:

- complete MVP acceptance criteria
- stable public CLI behavior
- documented implemented public interfaces
- passing tests
- current documentation
- production-quality release packaging

A 1.0.0 release does not imply that every capability described by the target
architecture has been implemented.

---

# 5. Patch Releases

PATCH releases may include:

- bug fixes
- documentation improvements
- implementation refinements
- non-breaking maintenance changes

Patch releases must not intentionally introduce breaking public behavior.

---

# 6. Minor Releases

MINOR releases may include:

- new features
- additional capabilities
- new extension implementations
- additional subtitle formats

Existing public contracts should remain compatible.

---

# 7. Major Releases

MAJOR releases may introduce:

- breaking architectural changes
- incompatible public API changes
- contract changes
- migration requirements

Major releases require appropriate migration documentation.

---

# 8. Release Criteria

A release requires:

- intended release requirements are satisfied
- tests pass
- documentation is updated
- architectural constraints remain satisfied
- release notes or changelog information is updated

Only capabilities included in the release scope are release requirements.

Future architectural capabilities do not block an MVP release unless explicitly
included in its scope.

---

# 9. Support Policy

The latest stable release receives active maintenance.

Older releases may receive critical fixes when practical.

---

# 10. Stability

The release strategy evolves conservatively.

Changes to versioning or release policy require appropriate architectural
review and documentation updates.