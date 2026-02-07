# Rubric: what DR measures (and why)

DR is a **diminishing-returns meter**, not a truth detector.

It tries to answer:

> Are we still producing net-new, decision-relevant information — or mostly rephrasing?

## Components (v0.1 → v0.2)

### 1) Novelty (claim-level)
**What:** count net-new `outputs.claims` per round (set-diff).

**Why:** in real loops (research, critique→revise, debate), novelty typically decays: early rounds add many new claims; later rounds add fewer.

**v0.1 implementation:** exact-string set difference over structured `claims`.

**v0.2 upgrades:**
- semantic dedupe (embedding clustering)
- claim extraction from raw text (structured output enforced via prompt contract)

### 2) Semantic stability (agreement)
**What:** measure semantic similarity between the most recent summaries (or between two agents’ latest responses).

**Why:** once two perspectives are saying the same thing, more turns often yield rephrasing, not new structure.

**v0.2 implementation:** sentence embeddings + cosine similarity.

### 3) Structural agreement
**What:** classify whether the second agent is:
- modifying (introducing changes)
- endorsing (agreeing with small additions)
- rephrasing (restating)

**Why:** “modify vs endorse vs rephrase” is a cheap proxy for whether the conversation is still doing work.

### 4) Action readiness
**What:** detect whether the next step is:
- a clarifying question
- a conditional plan
- an executable next action (run tests, open PR, do the experiment)

**Why:** you can be converged but blocked; DR should not say “stop” if the right move is “ask one missing question.”

---

## Composite stopping rule (recommended)

Stop when all are true for **k rounds**:
- novelty is low
- semantic stability is high
- action readiness is high (or at least not blocked)

Then: **ship a decision + run verification**.

## Non-goals

- DR does not claim correctness.
- DR does not replace evidence gates.

"Two ideas enter. One decision leaves." — but the decision must still be verified.
