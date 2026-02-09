# Rubric: what DR measures (and why)

DR is a **diminishing-returns meter**, not a truth detector.

It tries to answer:

> Are we still producing net-new, decision-relevant information — or mostly rephrasing?

## Components (v0.1 → v0.2)

### 1) Novelty (claim-level) — **implemented**
**What:** count net-new `outputs.claims` per round (set-diff).

**Why:** in real loops (research, critique/revise, debate), novelty typically decays: early rounds add many new claims; later rounds add fewer.

**v0.1 implementation:** normalized-string set difference over structured `claims`, with per-round dedupe. Claims are lowercased and whitespace-collapsed before comparison. The `novelty_rate` is averaged over a 2-round tail window (not just the final round), then divided by peak novelty. The `score` is `1.0 - novelty_rate`.

**Known limitations (v0.1):**
- Paraphrased claims are counted as novel. "Use PgBouncer" and "We should adopt PgBouncer for connection pooling" are treated as completely different claims despite expressing the same idea.
- No stemming or lemmatization. "running tests" and "run tests" are different.
- No minimum round count. A 1-round transcript produces a novelty rate of 1.0 and a score of 0.0, which is technically correct but not informative.

**v0.2 upgrades (planned):**
- Semantic dedupe (embedding clustering via SBERT)
- Claim extraction from raw text (structured output enforced via prompt contract)

### 2) Action readiness — **implemented (heuristic)**
**What:** detect whether the latest round has unresolved questions or executable next actions.

**Why:** you can be converged but blocked; DR should not say "stop" if the right move is "ask one missing question."

**v0.1 implementation:** checks `outputs.open_questions` and `outputs.next_actions` in the final round. Returns 1.0 if no open questions remain and at least one next action exists; 0.0 otherwise. Acts as a blocker on the stop recommendation.

**Known limitations (v0.1):**
- Binary signal (0.0 or 1.0) — no nuance between "one minor clarification" and "fundamental question unresolved."
- Only inspects the latest round, not the trajectory.
- Any non-empty `open_questions` entry suppresses the stop signal, even if the question is trivial.

### 3) K-consecutive stopping rule — **implemented**
**What:** recommend stopping after k consecutive rounds of low novelty (default k=2).

**v0.1 implementation:** a round is "low novelty" if `new_claims / peak_new <= 0.2`. The scorer tracks the maximum run of consecutive low-novelty rounds. Stop is recommended when `max_consecutive >= k` and no blockers are active.

**Known limitations (v0.1):**
- The threshold (0.2) and window size (k=2) are hardcoded and not empirically calibrated.
- The confidence score in `stop_recommendation` combines multiple heuristics but has not been validated against human judgment.

### 4) Semantic stability (agreement) — **not implemented**
**What:** measure semantic similarity between the most recent summaries (or between two agents' latest responses).

**Why:** once two perspectives are saying the same thing, more turns often yield rephrasing, not new structure.

**v0.2 plan:** sentence embeddings + cosine similarity. Returns `null` in v0.1 output.

### 5) Structural agreement — **not implemented**
**What:** classify whether the second agent is:
- modifying (introducing changes)
- endorsing (agreeing with small additions)
- rephrasing (restating)

**Why:** "modify vs endorse vs rephrase" is a cheap proxy for whether the conversation is still doing work.

**Open question:** Should this be an LLM classification (expensive but accurate) or a heuristic (cheap but brittle)? The right answer depends on whether DR is meant to run in hot loops (cheap) or as a post-hoc analysis (can afford LLM calls).

---

## Composite stopping rule

The intended composite rule is: stop when all are true for **k consecutive rounds**:
- Novelty is low
- Semantic stability is high
- Action readiness is high (or at least not blocked)

Then: **ship a decision + run verification**.

**Current implementation (v0.1):** Recommend stop at `k=2` consecutive low-novelty rounds, suppressed if the latest round has unresolved `open_questions`. Semantic stability is not yet factored in.

## Calibration status

| Component | Implemented? | Calibrated? | Data source |
|-----------|-------------|-------------|-------------|
| Novelty rate | Yes | No | Clean-room examples only |
| Action readiness | Yes (heuristic) | No | Clean-room examples only |
| K-consecutive stopping (k=2) | Yes | No | Threshold chosen by intuition |
| Low-novelty threshold (0.2) | Yes | No | Threshold chosen by intuition |
| Semantic stability | No | N/A | — |
| Structural agreement | No | N/A | — |

**What "calibrated" means here:** The component has been validated against human judgments on non-synthetic transcripts. None of the components have reached this bar yet. See [`docs/devils-advocate.md`](./devils-advocate.md) for proposed calibration experiments.

## Non-goals

- DR does not claim correctness.
- DR does not replace evidence gates.
- DR does not detect *false* convergence (agents agreeing on wrong answers). That requires external verification.

"Two ideas enter. One decision leaves." — but the decision must still be verified.
