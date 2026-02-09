# Novelty Detection & Action Readiness Spec

**Status:** Draft (v0.2 target)
**Author:** Campion.app
**Date:** 2026-02-08

---

## 1. Overview

This spec defines two new scoring components for the DR pipeline:

1. **Novelty detection** — a 3-level system replacing the v0.1 exact-string set-diff
2. **Action readiness** — a 0..1 signal measuring how close a conversation is to producing an executable decision

Together with the existing novelty curve, these components feed a **stop recommendation** that tells the caller: CONTINUE, SHIP, or ESCALATE.

### Design constraint

DR is a stop/ship signal, not a truth detector. These components measure *convergence* and *readiness to act*, not correctness.

---

## 2. Novelty Detection

### 2.1 Levels

#### L0: Normalization + per-round dedupe

**Input:** `outputs.claims` from each round.

**Algorithm:**
1. Normalize each claim: lowercase, strip whitespace, collapse consecutive whitespace to single space, strip trailing punctuation (`.!?`).
2. Deduplicate within each round (same normalized string = same claim).
3. Track `seen_claims: set[str]` across rounds.
4. Per-round novelty = count of claims whose normalized form is not in `seen_claims`.

**Rationale:** This catches exact repeats and trivial reformatting (capitalization, trailing period) that v0.1 misses. Cheap, deterministic, no dependencies.

**Novelty rate (L0):**
```
novelty_rate_L0 = new_claims_this_round / max(peak_new_claims, 1)
```

#### L1: Fuzzy matching (no embeddings)

**Input:** Normalized claims from L0.

**Algorithm:**
1. For each claim in the current round, compare against all `seen_claims` using token-level Jaccard similarity:
   ```
   jaccard(a, b) = |tokens(a) ∩ tokens(b)| / |tokens(a) ∪ tokens(b)|
   ```
   where `tokens(x) = set(x.split())` after L0 normalization.
2. A claim is **novel** if its maximum Jaccard similarity to any seen claim is below the fuzzy threshold.
3. A claim is a **paraphrase** if its Jaccard similarity is at or above the threshold.

**Fuzzy threshold: 0.6**

Justification:
- Below 0.4: unrelated claims frequently match (false positives).
- 0.5–0.6: catches most paraphrases while allowing genuinely distinct claims that share vocabulary.
- Above 0.7: too strict; misses paraphrases that swap a few words.
- Empirical target: in the meeting-stop example, round 5's claim ("Stop rule (meeting): purpose met OR timebox hit OR loop detected (no net-new substance).") should match round 4's identical claim at Jaccard 1.0, and round 6's restatement of "A clean ending requires an explicit 'decision + next action'" should match round 1's version at high Jaccard.

**Novelty rate (L1):**
```
novelty_rate_L1 = fuzzy_new_claims / max(peak_fuzzy_new_claims, 1)
```

#### L2: Embedding-based semantic novelty (optional, future)

**Input:** Raw claim strings (pre-normalization is fine but not required).

**Algorithm:**
1. Embed each claim using a sentence-transformer model (e.g., `all-MiniLM-L6-v2`).
2. For each claim, compute cosine similarity against all `seen_claim_embeddings`.
3. A claim is **novel** if its max cosine similarity to any seen claim is below the semantic threshold.

**Semantic threshold: 0.82**

Justification:
- Sentence-transformer cosine similarities for paraphrases typically land in 0.80–0.95.
- Below 0.75: even moderately related sentences match.
- 0.80–0.85: catches semantic paraphrases while preserving genuinely new claims.
- This threshold should be tuned per-model; 0.82 is calibrated for MiniLM-L6-v2.

**Novelty rate (L2):**
```
novelty_rate_L2 = semantic_new_claims / max(peak_semantic_new_claims, 1)
```

**Implementation note:** L2 is optional and should be behind a feature flag. L0+L1 are the default.

### 2.2 Combined novelty score

When multiple levels are available, use the **minimum novelty rate** across active levels:

```
novelty_rate = min(novelty_rate_L0, novelty_rate_L1 [, novelty_rate_L2])
```

Rationale: If *any* level detects that claims are not novel, they are not novel. This is conservative — it biases toward stopping, which is the right default for a diminishing-returns meter.

### 2.3 Novelty classification

| Novelty rate | Classification | Meaning |
|---|---|---|
| > 0.5 | HIGH | Significant new content being produced |
| 0.15 – 0.5 | MEDIUM | Some new content, but tapering |
| < 0.15 | LOW | Mostly rehashing; diminishing returns |

**Threshold justification:**
- 0.5: If more than half the novelty peak is still being produced, the conversation is clearly still productive.
- 0.15: Below ~15% of peak novelty, empirically the conversation is in restatement territory. The meeting-stop example hits 0.0 novelty in rounds 5-6; the threshold should catch the transition.
- These thresholds are intentionally simple. Tuning should use the calibration examples.

### 2.4 K-consecutive rule

Novelty is classified as LOW only if it has been LOW for **k = 2 consecutive rounds**. A single low-novelty round may be a natural pause before a new direction.

---

## 3. Action Readiness

### 3.1 Definition

Action readiness measures how close the conversation is to producing an executable outcome. It is a 0..1 float derived from three sub-signals in the most recent round's `outputs`:

1. **next_actions presence and specificity** (weight: 0.5)
2. **open_questions trend** (weight: 0.3)
3. **blocker detection** (weight: 0.2)

### 3.2 Sub-signals

#### 3.2.1 next_actions score (0..1)

| Condition | Score | Rationale |
|---|---|---|
| No `next_actions` field or empty array | 0.0 | Nothing to execute |
| Actions present but all vague (see below) | 0.3 | Intent without specificity |
| At least one specific action | 0.7 | Actionable but possibly incomplete |
| Multiple specific actions with clear ownership language | 1.0 | Ready to execute |

**Vague action detection (L0 heuristic):**
An action is classified as *vague* if it matches any of these patterns:
- Starts with "consider", "think about", "explore", "look into", "investigate"
- Contains "maybe", "possibly", "might", "could potentially"
- Is shorter than 5 words with no verb

An action is classified as *specific* if:
- Contains an imperative verb (run, write, create, open, deploy, send, test, build, merge, ship, implement, add, remove, update, fix, configure)
- References a concrete artifact (file path, URL, tool name, command, PR, branch)

#### 3.2.2 open_questions trend (0..1)

Measures whether open questions are being resolved or accumulating.

```
if current_round has no open_questions:
    oq_score = 1.0
elif len(current_oq) < len(previous_oq):
    oq_score = 0.7  # Trending down — resolving
elif len(current_oq) == len(previous_oq):
    oq_score = 0.4  # Stalled
else:
    oq_score = 0.1  # Accumulating — not converging
```

If there is only one round (no previous), and open questions exist: `oq_score = 0.3`.

#### 3.2.3 blocker detection (0..1)

Scan `open_questions` and `next_actions` for blocker language:

**Blocker keywords:** "blocked", "blocker", "waiting on", "depends on", "need access", "need permission", "can't proceed", "prerequisite", "missing"

```
if any blocker keyword found in open_questions or next_actions:
    blocker_score = 0.0
else:
    blocker_score = 1.0
```

This is intentionally binary. Blockers are decisive — a conversation with a known blocker is not ready to ship regardless of other signals.
In the final decision step, blocker detection acts as a hard override: the recommendation must not be SHIP while blocked.

### 3.3 Composite action readiness

```
action_readiness = (0.5 * next_actions_score) + (0.3 * oq_score) + (0.2 * blocker_score)
```

### 3.4 Action readiness classification

| Score | Classification | Meaning |
|---|---|---|
| >= 0.7 | HIGH | Ready to execute; has specific next steps |
| 0.4 – 0.7 | MEDIUM | Partial readiness; some gaps remain |
| < 0.4 | LOW | Not ready; missing actions, accumulating questions, or blocked |

---

## 4. Stop Recommendation

### 4.1 Decision matrix

| Novelty | Readiness | Recommendation | Rationale |
|---|---|---|---|
| LOW | HIGH | **SHIP** | Converged and ready — execute the plan |
| LOW | MEDIUM | **SHIP** (with caveat) | Converged; minor gaps won't be resolved by more rounds |
| LOW | LOW | **ESCALATE** | Stuck: not producing new ideas AND not ready to act |
| MEDIUM | HIGH | **CONTINUE** (1 more round) | Still some new content; let it settle |
| MEDIUM | MEDIUM | **CONTINUE** | Active exploration with partial progress |
| MEDIUM | LOW | **CONTINUE** | Still exploring; readiness may improve |
| HIGH | HIGH | **CONTINUE** | Productive; let it run |
| HIGH | MEDIUM | **CONTINUE** | Productive exploration |
| HIGH | LOW | **CONTINUE** | Active divergence phase |

### 4.2 ESCALATE conditions

ESCALATE means: "Stop the current loop and change something — bring in a human, add a new agent, change the prompt, or narrow the scope."

ESCALATE triggers when:
1. Novelty is LOW + readiness is LOW (main case), OR
2. Novelty is LOW + any blocker is detected (blocker_score = 0.0), OR
3. Novelty has been LOW for **k = 3+** consecutive rounds AND readiness has not reached HIGH in any of those rounds.

The distinction between ESCALATE and SHIP matters: SHIP means "go do the thing"; ESCALATE means "this conversation cannot produce the thing — change the conversation."

### 4.3 Output format

The stop recommendation extends the existing score output:

```json
{
  "score": 0.92,
  "components": {
    "novelty_rate": 0.08,
    "novelty_rate_L0": 0.0,
    "novelty_rate_L1": 0.08,
    "action_readiness": 0.85,
    "action_readiness_detail": {
      "next_actions_score": 0.7,
      "open_questions_score": 1.0,
      "blocker_score": 1.0
    },
    "semantic_similarity": null,
    "structural_agreement": null
  },
  "novelty_by_round": [...],
  "stop_recommendation": {
    "signal": "SHIP",
    "novelty_classification": "LOW",
    "readiness_classification": "HIGH",
    "k_consecutive_low_novelty": 2,
    "rationale": "Novelty has been low for 2 consecutive rounds. Action readiness is high: specific next actions present, no open questions, no blockers."
  },
  "hint": "Converged. Ship the decision and verify."
}
```

---

## 5. Failure Modes & Mitigations

### 5.1 Paraphrase gaming

**Attack:** An agent restates the same claim with different words each round, keeping exact-string novelty artificially high.

**Detection:** L1 (Jaccard) catches word-shuffling paraphrases. L2 (embeddings) catches deeper semantic equivalence.

**Mitigation:** Use combined novelty (min across levels). Even if L0 is fooled, L1 should catch it.

**Residual risk:** Sophisticated paraphrasing that changes vocabulary substantially while preserving meaning. Only L2 addresses this.

### 5.2 Claim inflation

**Attack:** An agent generates many trivially different claims per round to keep the claim count high.

**Detection:** L1 Jaccard will cluster inflated claims. Also monitor `claims_per_round` — a sudden spike with low novelty suggests inflation.

**Mitigation:** Track the ratio `new_claims / total_claims`. If this drops below 0.1 while total_claims stays high, flag as potential inflation.

### 5.3 Fake readiness

**Attack:** An agent includes next_actions like "Implement the solution" every round without the conversation actually converging.

**Detection:** Cross-reference readiness with novelty. If novelty is HIGH but readiness is also claiming HIGH, the actions may be premature.

**Mitigation:** The decision matrix already handles this: HIGH novelty always produces CONTINUE regardless of readiness. Readiness only matters when novelty is LOW.

### 5.4 Question suppression

**Attack:** An agent omits open_questions to inflate the readiness score.

**Detection:** Difficult to detect from structure alone.

**Mitigation:**
1. Compare question count across rounds — a sudden drop to zero in a round that introduces new claims is suspicious.
2. L2 (future): scan claim text for question-like patterns even when they are not in the `open_questions` field.
3. Ultimately, DR does not claim correctness. It flags convergence. If an agent suppresses questions, the convergence signal is accurate (the loop *is* converging), even if the quality of convergence is poor. Quality is an orthogonal concern.

### 5.5 Blocker evasion

**Attack:** An agent rephrases blockers to avoid blocker keywords: "we'll figure out auth later" instead of "blocked on auth credentials."

**Detection:** L1 keyword matching will miss this.

**Mitigation:**
1. Expand the blocker keyword list over time based on observed evasion patterns.
2. L2 (future): semantic blocker detection using embeddings.
3. Accept the residual risk: DR is advisory. A human or reviewer agent should validate the SHIP recommendation.

### 5.6 Stale readiness

**Attack:** A conversation had high readiness in round 3, then drifted into new territory. The stop_recommendation might still reference old readiness.

**Detection:** Readiness is computed from the *most recent round only*. Stale readiness from earlier rounds does not contribute.

**Mitigation:** Already addressed by design. Readiness is always fresh.

---

## 6. Implementation Notes for Codex.app

### 6.1 What to change

- `src/dr/score.py`: Add L0 normalization, L1 fuzzy matching, action_readiness computation, and stop_recommendation logic.
- Do NOT modify the transcript schema. All new signals are derived from existing fields.
- Update `examples/*.expected.json` to reflect new output fields.

### 6.2 Dependencies

- L0 + L1: **zero new dependencies**. String operations and set math only.
- L2: `sentence-transformers` (optional, behind flag). Do not add this dependency until L2 is explicitly requested.

### 6.3 Backward compatibility

- The `score` field must remain: `1.0 - novelty_rate` (using the combined novelty rate).
- The `components` dict must retain all existing keys, adding new ones.
- The `stop_recommendation` key is new and additive.

### 6.4 Test expectations

Each calibration example in `examples/calibration/` includes an `_expected` section documenting the expected novelty classification, readiness classification, and stop recommendation. Implementation tests should assert against these.

---

## 7. Calibration Examples

See [../examples/calibration/](../examples/calibration/) for 8 adversarial transcript examples:

| File | Scenario | Expected signal |
|---|---|---|
| `paraphrase-rounds.json` | Paraphrased claims that should NOT count as novel | SHIP |
| `exact-repeat.json` | Exact-repeat rounds (baseline) | SHIP |
| `low-novelty-high-readiness.json` | Converged with clear next actions | SHIP |
| `low-novelty-low-readiness.json` | Converged but stuck/blocked | ESCALATE |
| `high-novelty-low-readiness.json` | Active exploration, not ready | CONTINUE |
| `high-novelty-high-readiness.json` | Productive with actions | CONTINUE |
| `blocker-present.json` | Low novelty but blocked | ESCALATE |
| `question-accumulation.json` | Questions growing, no resolution | CONTINUE |

---

## 8. Open Questions (for this spec)

1. Should the K-consecutive threshold differ between SHIP and ESCALATE? Current spec uses k=2 for both.
2. Should `decisions` field contribute to readiness? Currently only `next_actions` and `open_questions` are used.
3. Should there be a STOP signal distinct from SHIP? Current spec merges them: SHIP means stop and execute.

---

## Appendix A: Worked Example (meeting-stop transcript)

Using the existing meeting-stop example:

**Round-by-round novelty (L0 normalization):**

| Round | Claims | New (L0) | Novelty rate (L0) |
|---|---|---|---|
| 1 | 4 | 4 | 1.0 (peak) |
| 2 | 3 | 1 | 0.25 |
| 3 | 3 | 1 | 0.25 |
| 4 | 3 | 1 | 0.25 |
| 5 | 1 | 0 | 0.0 |
| 6 | 2 | 0 | 0.0 |

**Novelty classification at round 6:** LOW (0.0 < 0.15, and LOW for 2 consecutive rounds).

**Action readiness at round 6:**
- `next_actions`: ["End."] — vague (< 5 words, no imperative verb referencing artifact) → 0.3
- `open_questions`: [] → oq_score = 1.0
- Blockers: none → blocker_score = 1.0
- Composite: (0.5 * 0.3) + (0.3 * 1.0) + (0.2 * 1.0) = 0.15 + 0.30 + 0.20 = **0.65**

**Readiness classification:** MEDIUM (0.4 <= 0.65 < 0.7)

**Stop recommendation:** LOW novelty + MEDIUM readiness → **SHIP** (with caveat)

This matches intuition: by round 6, the meeting-stop conversation is clearly converged and should ship, even though the final next_action is not particularly specific.

## Appendix B: Worked Example (round 4 — the recommended stop)

**Novelty at round 4:** novelty_rate_L0 = 0.25, classification = MEDIUM (single round; k=2 not met for LOW).

**Action readiness at round 4:**
- `next_actions`: ["Convert this into a 1-page facilitation checklist."] — specific (imperative verb "convert", concrete artifact "1-page facilitation checklist") → 0.7
- `open_questions`: [] (down from 1 in round 3) → oq_score = 1.0
- Blockers: none → blocker_score = 1.0
- Composite: (0.5 * 0.7) + (0.3 * 1.0) + (0.2 * 1.0) = 0.35 + 0.30 + 0.20 = **0.85**

**Readiness classification:** HIGH (>= 0.7)

**Stop recommendation:** MEDIUM novelty + HIGH readiness → **CONTINUE** (1 more round)

Interesting: even at the human-recommended stop point (round 4), the algorithm says CONTINUE because novelty hasn't been low long enough. By round 5 (k=2 met), it would flip to SHIP. This 1-round lag is acceptable and conservative.
