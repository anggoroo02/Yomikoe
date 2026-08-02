# Release Strategy & Versioning

Version: 1.0

Status: Accepted

---

# 1. Purpose

This document defines the release philosophy and versioning strategy for Yomikoe.

The objective is to provide predictable releases while preserving long-term maintainability.

---

# 2. Versioning

Yomikoe follows Semantic Versioning (SemVer):

MAJOR.MINOR.PATCH

Example:

0.1.0

1.0.0

1.2.3

---

# 3. Pre-1.0 Releases

Versions below 1.0 are considered evolving.

However:

Architectural discipline remains identical to post-1.0 releases.

Pre-1.0 does not justify poor engineering practices.

---

# 4. Stable Release

Version 1.0.0 represents:

- stable architecture
- stable public CLI
- documented public interfaces
- complete MVP
- production-quality documentation

It does not imply every planned feature has been implemented.

---

# 5. Patch Releases

PATCH releases include:

- bug fixes
- documentation improvements
- implementation refinements

No intentional breaking changes.

---

# 6. Minor Releases

MINOR releases may include:

- new features
- additional extensions
- new capabilities

Existing public contracts should remain compatible.

---

# 7. Major Releases

MAJOR releases may introduce:

- breaking architectural changes
- incompatible public API changes
- migration requirements

Major releases require migration documentation.

---

# 8. Release Criteria

A release requires:

- passing tests
- updated documentation
- updated changelog
- architectural review completed

---

# 9. Support Policy

The latest stable release receives active maintenance.

Older releases may receive critical fixes when practical.

---

# 10. Stability

The release strategy evolves conservatively.

Changes require architectural review.