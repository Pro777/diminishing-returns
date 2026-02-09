# DR Roadmap

## Where We Are

DR is a Python library that scores multi-round review transcripts for convergence. It answers: "Are we still producing new information, or mostly rephrasing?"

Current capabilities (v0.1, post-hardening):
- JSONL/JSON transcript input with validation
- Claim-level novelty scoring (normalized-string set-diff, per-round dedupe)
- K-consecutive low-novelty stopping rule (k=2, threshold 0.2)
- Blocker-aware stop recommendations (checks `open_questions` / `next_actions`)
- Action readiness heuristic (binary: blocked or ready)
- `stop_recommendation` object with confidence score
- CLI: `dr score <transcript>`

## Where We're Going

DR evolves in four directions: **scoring depth**, **protocol breadth**, **trust tiers**, and **adoption**.

---

### Track 1: Scoring Depth

Better measurement of convergence within a single review.

| Version | Feature | Status |
|---------|---------|--------|
| v0.1 | Normalized-string claim novelty (lowercase, whitespace-collapsed) | Shipped |
| v0.1 | Per-round claim deduplication | Shipped |
| v0.1 | K-consecutive stopping rule (k=2, threshold 0.2) | Shipped |
| v0.1 | Action readiness heuristic (binary, from open_questions/next_actions) | Shipped |
| v0.1 | Input validation (type checks, error messages) | Shipped |
| v0.2 | Semantic dedupe (embedding clustering via SBERT) | Planned |
| v0.2 | Structural agreement (modify/endorse/rephrase classification) | Planned |
| v0.2 | Graduated action readiness (not just binary) | Planned |
| v0.3 | BERTScore round-over-round stability | Planned |
| v0.3 | Multi-agent identity tracking (who said what) | Planned |

### Track 2: Protocol Breadth

DR as a portable trust signal for any inter-agent communication.

| Version | Feature | Status |
|---------|---------|--------|
| v0.1 | Local tier: markdown DR convention | In use |
| v0.1 | Attestation spec ([`spec/attestation.v0.1.md`](../spec/attestation.v0.1.md)) | Draft |
| v0.2 | UUID generation for all attestations | Planned |
| v0.2 | Attestation JSON schema | Planned |
| v0.2 | `dr attest` CLI command | Planned |
| v0.3 | Evidence bundle format | Planned |
| v0.3 | Signature support (Sigstore keyless) | Planned |
| v0.4 | Independent re-scoring (`dr verify <attestation>`) | Planned |

### Track 3: Trust Tiers

Extending DR across trust boundaries.

| Tier | Trust | Transport | Status |
|------|-------|-----------|--------|
| Local | Full | Markdown, filesystem | In use |
| Federated | Partial | Webhooks, MCP, shared APIs | Specified (not implemented) |
| Internet | None | HTTP, email, public APIs | Specified (not implemented) |

### Track 4: Adoption

Making DR discoverable and easy to integrate.

| Item | Status |
|------|--------|
| Real-world PR review example (not philosophy) | Planned |
| GitHub Action (`dr score` comments on PRs) | Planned |
| PyPI package (`pip install diminishing-returns`) | Planned |
| Automated test suite (unit tests exist; CI doesn't run them yet) | Partial |
| Blog post / landing page for discoverability | Planned |
| MCP server (agents can call `dr score` as a tool) | Planned |
| PR template with optional DR attestation field | Planned |
| Low-DR example transcript (score < 0.85, "keep going") | Planned |

---

## Implementation Priorities

### Now (v0.1 stabilization)
- [x] Normalized-string novelty scoring
- [x] K-consecutive stopping rule (k=2)
- [x] Blocker-aware stop recommendations
- [x] Action readiness heuristic
- [x] Input validation
- [x] JSONL + JSON input support
- [x] Write attestation spec (draft)
- [x] Three clean-room example transcripts
- [x] Devil's advocate critique ([`docs/devils-advocate.md`](./devils-advocate.md))
- [x] Unit tests (`tests/test_score.py` — dedup, stopping, JSONL ordering, error reporting)
- [ ] CI runs tests (currently just `print('ok')`)
- [ ] Update `*.expected.json` to match post-hardening output format
- [ ] CI validates `dr score` output against `*.expected.json`
- [ ] PyPI-ready packaging (but don't publish yet — validate first)

### Next (v0.2)
- [ ] Add UUID generation to `dr score` output
- [ ] JSON schema for attestation object
- [ ] `dr attest` CLI: takes a claim + transcript, outputs attestation JSON
- [ ] Semantic dedupe in scoring (optional SBERT dependency)
- [ ] At least one low-DR example (score < 0.85)
- [ ] Graduated action readiness (severity tiers, not just binary)
- [ ] Handoff-note parser (extract rounds/method from markdown)

### Later (v0.3+)
- [ ] Evidence bundle format
- [ ] Sigstore signing integration
- [ ] `dr verify` CLI: takes attestation JSON, fetches evidence, re-scores
- [ ] MCP tool: `dr_attestation` for agent-to-agent trust signals
- [ ] Attestation DAG visualization
- [ ] Multi-agent identity tracking

---

## Experiments Needed

These are calibration and validation experiments that should be run before v0.2 ships. See also [`docs/devils-advocate.md`](./devils-advocate.md) for the full critique.

### Experiment 1: Paraphrase Sensitivity
**Question:** How often does normalized-string matching miss semantic duplicates in real conversations?
**Method:** Take 5-10 real multi-agent transcripts. Have a human annotate "actually new ideas" per round. Compare human novelty counts against DR's counts. Measure precision/recall.
**Success criterion:** If precision > 0.8, normalized-string matching is good enough for v0.2. If not, semantic dedupe is a prerequisite.

### Experiment 2: Threshold Calibration
**Question:** Is the low-novelty threshold (0.2) the right cutoff for detecting convergence?
**Method:** Collect or synthesize 20+ transcripts spanning 0.5-1.0 scores. Have humans label each as "should stop" or "should continue." Find the empirical decision boundary.
**Success criterion:** The threshold should agree with human judgment > 80% of the time.

### Experiment 3: K-Consecutive Window Size
**Question:** What value of K (consecutive low-novelty rounds) gives the best stop signal?
**Method:** Run DR with K=1, 2, 3 on transcripts where the "right" stop round is human-annotated. Measure false-stop and false-continue rates.
**Success criterion:** K=2 is the current default. Validate or reject.

### Experiment 4: Adversarial Convergence
**Question:** Can an agent game its DR score by repeating claims verbatim?
**Method:** Construct a transcript where Agent B copies Agent A's claims word-for-word while subtly changing the recommendation. DR should report high convergence even though the agents disagree.
**Success criterion:** Identify the attack and document how semantic similarity (v0.2) would mitigate it.

### Experiment 5: Real-World Calibration
**Question:** Does DR's score correlate with decision quality in production?
**Method:** Collect DR scores from the proving ground. For each scored handoff, track whether the receiving agent accepted, modified, or rejected the recommendation. Correlate DR score with acceptance rate and outcome quality.
**Success criterion:** Higher DR scores should correlate with higher acceptance rates. If they don't, the scoring model needs recalibration.

### Experiment 6: Action Readiness Sensitivity
**Question:** Does the binary action readiness heuristic match human judgment about what blocks shipping?
**Method:** Collect transcripts with varying `open_questions` entries (trivial, important, rhetorical). Check whether the binary blocker signal aligns with human assessment of "should this block the stop recommendation?"
**Success criterion:** The heuristic should agree with human judgment > 75% of the time. If not, graduated severity is needed for v0.2.

---

## Adoption Philosophy

DR is a gentleman's agreement. It works because it's useful, not because it's enforced. The path to adoption is:

1. **Be easy to try.** Install from source, score a transcript — under 60 seconds to value.
2. **Show up where people already work.** GitHub Actions, PR comments, CI pipelines. If DR scores appear alongside existing review tooling, people absorb the convention without effort.
3. **Lead with the human problem.** "Are we still producing new information, or just going in circles?" Every developer has felt this. The multi-agent protocol layer comes later — the convergence meter comes first.
4. **Don't require the protocol to get value from the tool.** The CLI works standalone. The attestation spec is additive. You can use `dr score` without ever knowing about trust tiers.
5. **Let the protocol emerge from use.** The local tier (markdown `**DR:**` lines) is in use. The federated and internet tiers are specified but will be shaped by real adoption patterns, not designed in advance.

---

## Proving Ground

The proving ground generates real-world data on:

- How often do receiving agents push back on low-DR items?
- Do high-DR items actually get rubber-stamped?
- Does the DR score correlate with outcome quality?

This data feeds back into scoring calibration.

> **Note:** No proving-ground data is currently included in this repo. When anonymized examples become available, they should be added to `examples/` with appropriate context.

---

*The scoring algorithm is the engine. The protocol is the vehicle.*
