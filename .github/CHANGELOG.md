# Changelog

All notable changes to this project will be documented in this file.

The format is based on *Keep a Changelog*, and this project aims to follow Semantic Versioning when releases are cut.

## [Unreleased]

### Added
- Devil's advocate critique document ([`docs/devils-advocate.md`](../docs/devils-advocate.md)) — 10-point honest failure mode analysis
- Status and limitations section in README — makes pre-release state explicit
- Pip install disclaimer — clarifies the package is not yet on PyPI
- Six proposed calibration experiments in roadmap (paraphrase sensitivity, threshold calibration, K-window, adversarial convergence, real-world calibration, action readiness sensitivity)
- Open questions section in attestation spec (score semantics, evidence privacy, clock trust, score gaming, revocation discovery, round definition)
- Implementation maturity table in attestation spec
- Calibration status table in rubric (distinguishes implemented from calibrated)
- Missing example coverage notes in examples/README

### Changed
- README: "What it measures" section now distinguishes implemented (novelty rate, action readiness, K-consecutive) from planned (semantic convergence, structural agreement)
- README: Quick start uses install-from-source instead of `pip install` (not yet on PyPI)
- README: Output example updated to match post-hardening format (includes `stop_recommendation`)
- README: Limitations section updated to reflect two implemented components (not one)
- Roadmap: accurately reflects post-hardening state (normalization, K-consecutive, blockers, action readiness all shipped)
- Roadmap: six calibration experiments proposed (was five; added action readiness sensitivity)
- Roadmap: added automated test suite and expected.json updates to adoption track
- Rubric: restructured to five components (novelty, action readiness, K-consecutive, semantic stability, structural agreement) with per-component implementation status and known limitations
- References: replaced placeholder citations with specific papers (arXiv links, venues, years)
- References: removed TODO section
- Attestation spec: added implementation maturity table and six open design questions

## [0.0.0] - YYYY-MM-DD

Initial placeholder.
