# Diminishing Returns (DR) — academic research packet (2026-02-10)

Purpose: ground our **Diminishing Returns / convergence meter** idea in established research on **stopping rules**, **sequential decision making**, and **evaluation under uncertainty** — then translate it into testable, product-grade hypotheses for multi-agent / LLM workflows.

## 1-page synthesis (what the literature implies)

### What DR “really is”
A DR meter is an **optimal stopping** problem: keep iterating while the *expected value of another round* exceeds the *expected cost* (time, money, latency, attention, risk).

In classical terms, this lives at the intersection of:
- **Early stopping** (stop when improvement plateaus to avoid wasted compute / overfitting)
- **Sequential analysis** (stop when evidence is strong enough; keep sampling when uncertain)
- **Bandits / best-arm identification** (allocate trials where marginal gains are highest)
- **Behavioral testing / evaluation** (measure not just accuracy but robustness and failure modes)

### What “good” DR policies look like
The research repeatedly points to the same design pattern:

1) **Pick a scalar objective to monitor** (or a small vector with weights)
   - e.g., rubric score, correctness, constraint satisfaction, test pass rate, judge score.

2) **Use a patience / confidence rule**
   - Stop after *k* rounds without improvement (patience), or when improvement is below a threshold.
   - Or stop when sequential evidence crosses a confidence boundary.

3) **Separate exploration from exploitation**
   - Use one cheap probe round to estimate “is there headroom?”
   - If headroom exists, spend more budget; if not, ship.

4) **Treat evaluation as a test suite, not a vibe**
   - Behavioral tests (CheckList-style) make it harder to “improve” by overfitting to one example.

### How this maps to LLM / agent workflows
In LLM workflows, “more rounds” can improve:
- formatting compliance
- factuality (sometimes)
- planning completeness

…but also increases:
- hallucination surface area
- instruction drift
- token/cost

So DR should prioritize **measurable invariants**:
- contract compliance (parseable outputs, schema validity)
- correctness on a small fixed test suite
- stability across re-runs (variance)

### Concrete DR hypotheses we should test
- **H1 (Patience beats polishing):** A simple “patience=2” stop rule (no improvement for 2 rounds) captures most gains vs always running N rounds.
- **H2 (Sequential confidence is cheaper):** Wald-style sequential thresholds reduce average rounds needed to reach a target accuracy vs fixed-round policies.
- **H3 (Variance as hallucination proxy):** High between-sample variance predicts hallucination / unreliability; DR should stop or escalate when variance stays high.
- **H4 (Bandit budget allocation):** Allocate more iterations to tasks with higher measured headroom; overall throughput improves under a fixed time budget.

---

## Annotated bibliography (18 items)

### Theme A — Optimal stopping & sequential analysis (the theoretical core)

1) **Wald, A. (1945). _Sequential Tests of Statistical Hypotheses._**
Link: https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-16/issue-2/Sequential-Tests-of-Statistical-Hypotheses/10.1214/aoms/1177731118.full
Summary: Introduces the Sequential Probability Ratio Test (SPRT): decide as evidence accumulates rather than fixing sample size.
Implication for DR: replace “N rounds” with “stop when confident enough.”
Hypothesis: sequential thresholds reduce average rounds to reach a target quality at the same error rate.

2) **Chow, Y. S., Robbins, H., & Siegmund, D. (1971). _Great Expectations: The Theory of Optimal Stopping._**
Link: https://onlinelibrary.wiley.com/doi/book/10.1002/9780470317014
Summary: Foundational text for optimal stopping (when to stop sampling/iterating).
Implication: DR is optimal stopping with explicit cost-of-delay.
Hypothesis: modeling a cost curve yields better stop decisions than a fixed patience rule.

3) **Siegmund, D. (1985). _Sequential Analysis: Tests and Confidence Intervals._**
Link: https://doi.org/10.1007/978-1-4612-5122-9
Summary: Practical sequential methods for decisions under uncertainty.
Implication: DR can use confidence intervals over quality metrics.
Hypothesis: CI-based stops are more stable than point-estimate stops.

### Theme B — Early stopping & plateau detection (simple, effective policies)

4) **Prechelt, L. (1998). _Early Stopping — But When?_**
Link: https://doi.org/10.1007/3-540-49430-8_3
Summary: Classic discussion of early stopping criteria; highlights patience-like heuristics.
Implication: patience + smoothed metrics are sensible defaults.
Hypothesis: smoothing + patience reduces false stops from metric noise.

5) **Goodfellow, I., Bengio, Y., & Courville, A. (2016). _Deep Learning_ (Early stopping section).**
Link: https://www.deeplearningbook.org/
Summary: Standard reference on early stopping as regularization.
Implication: DR should treat “extra rounds” as overfitting risk to the current prompt/context.
Hypothesis: more rounds can degrade out-of-distribution robustness even if in-sample looks better.

### Theme C — Bandits / adaptive allocation (where to spend iteration budget)

6) **Lai, T. L., & Robbins, H. (1985). _Asymptotically efficient adaptive allocation rules._**
Link: https://projecteuclid.org/journals/advances-in-applied-mathematics/volume-6/issue-1/Asymptotically-efficient-adaptive-allocation-rules/10.1016/0196-8858(85)90002-8.full
Summary: Foundational results for bandit allocation: spend trials where marginal value is high.
Implication: DR across a queue is a budget allocation problem, not just per-task stopping.
Hypothesis: headroom-estimated allocation increases total delivered value per hour.

7) **Bubeck, S., & Cesa-Bianchi, N. (2012). _Regret Analysis of Stochastic and Nonstochastic Multi-armed Bandit Problems._**
Link: https://arxiv.org/abs/1204.5721
Summary: Survey of bandit theory and practical policies.
Implication: treat “try another refinement” as pulling an arm with uncertain payoff.
Hypothesis: UCB-like policies outperform naive equal-iterations across tasks.

### Theme D — Behavioral testing & holistic evaluation (avoiding “vibes”) 

8) **Ribeiro et al. (2020). _Beyond Accuracy: Behavioral Testing of NLP Models with CheckList._ ACL’20.**
Link: https://arxiv.org/abs/2005.04118
Summary: Behavioral test suites detect failures not seen in average accuracy.
Implication: DR meters should be computed against a stable behavioral suite.
Hypothesis: CheckList-style suites reduce “illusory improvements” that don’t generalize.

9) **Bommasani et al. (2022). _Holistic Evaluation of Language Models (HELM)._**
Link: https://arxiv.org/abs/2211.09110
Summary: Multi-metric evaluation across robustness, calibration, efficiency, etc.
Implication: DR should monitor a small vector (quality, compliance, cost), not a single number.
Hypothesis: multi-metric DR reduces regressions vs single-metric stops.

### Theme E — LLM self-refinement / iterative improvement (closest analogs)

10) **Madaan et al. (2023). _Self-Refine: Iterative Refinement with Self-Feedback._**
Link: https://arxiv.org/abs/2303.17651
Summary: LLM produces feedback then revises; iterative loop improves outputs on several tasks.
Implication: DR needs a stop condition for self-refine loops.
Hypothesis: “feedback→revise” loops show steep early gains then plateau; patience rule captures most value.

11) **Shinn et al. (2023). _Reflexion: Language Agents with Verbal Reinforcement Learning._**
Link: https://arxiv.org/abs/2303.11366
Summary: Reflection memory improves performance over repeated episodes.
Implication: DR should distinguish one-off tasks vs repeated tasks with learning.
Hypothesis: investing extra rounds is more valuable when the reflection can be reused.

12) **Wang et al. (2023). _Self-Consistency Improves Chain of Thought Reasoning in Language Models._ ICLR’23.**
Link: https://arxiv.org/abs/2203.11171
Summary: Sample multiple reasoning paths; choose consistent answer.
Implication: DR can trade “more samples” for confidence.
Hypothesis: confidence gains saturate after N samples; sequential stop saves cost.

13) **Manakul et al. (2023). _SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection._**
Link: https://arxiv.org/abs/2303.08896
Summary: Uses inconsistency across samples to detect hallucinations.
Implication: variance is a measurable proxy for unreliability.
Hypothesis: high variance predicts failure; DR should escalate instead of iterating.

### Theme F — Practical stopping criteria in active learning (useful heuristics)

14) **Bloodgood, M., & Vijay-Shanker, K. (2009). _A method for stopping active learning based on stabilizing predictions._**
Link: https://aclanthology.org/P09-2052/
Summary: Stop active learning when model predictions stabilize.
Implication: stop iterating when outputs stabilize under perturbations.
Hypothesis: “stabilizing answer” rules correlate with true quality plateaus.

15) **Vlachos, A. (2008). _A stopping criterion for active learning._**
Link: https://aclanthology.org/W08-0601/
Summary: Early work on principled stopping criteria in active learning.
Implication: DR can borrow stopping criteria that account for uncertainty/coverage.
Hypothesis: uncertainty-aware stops outperform naive patience when metrics are noisy.

---

## Suggested next artifact for this repo
Create `docs/dr-metrics.md` with:
- the minimal metric vector (quality, compliance, cost)
- the default stop policy (patience=2 + variance threshold)
- the evaluation suite harness (CheckList-style)
