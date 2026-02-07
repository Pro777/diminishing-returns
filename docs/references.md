# References (receipts)

This project is a practical tool, not a literature review. But the core idea — **stop when novelty collapses and stability is high** — is informed by existing work on multi-agent debate, self-refinement loops, semantic similarity metrics, and convergence/stability detection.

Below is a short, opinionated bibliography with **one-line “why it matters” receipts**.

## Multi-agent debate / critique loops

- **Multi-agent debate (general line of work)**
  - Why: debate/critique loops tend to show an early burst of novel objections followed by plateau; DR aims to detect the plateau.
  - Note: we treat agreement as *a stop signal*, not as correctness.

- **Self-Refine / Reflexion (iterative critique→revise patterns)**
  - Why: these methods often improve outputs for a few iterations and then yield diminishing returns; DR provides a termination nudge.

## Convergence / stability detection

- **Adaptive stability detection (sequential stopping tests; plateau detection)**
  - Why: formalizes “stop when improvements are no longer statistically meaningful,” a close cousin of DR’s stopping rule.

- **Emergent convergence / semantic compression in multi-agent systems**
  - Why: highlights a key risk: *false convergence* via compression (everyone sounds aligned) without external verification.

## Semantic similarity metrics

- **Sentence embeddings (e.g., SBERT) + cosine similarity**
  - Why: cheap, robust proxy for “are two responses saying the same thing?”

- **BERTScore (semantic similarity for text generation evaluation)**
  - Why: alternative similarity signal (heavier than embeddings) useful for offline evaluation.

## Diversity / redundancy

- **MMR (Maximal Marginal Relevance)**
  - Why: captures the relevance-vs-redundancy tradeoff; DR’s novelty metric is essentially “redundancy is dominating.”

- **Vendi Score / diversity metrics (distributional diversity)**
  - Why: provides a principled way to quantify “how diverse are these samples,” useful for multi-draft / self-consistency settings.

## Failure modes

- **Multi-agent failure taxonomies**
  - Why: reminds us that *consensus is not truth*; DR should always recommend verification (tests/evidence) before shipping.

---

## TODO (tighten citations)

We will replace the placeholders above with specific paper links (arXiv/ACL/NeurIPS) and short annotations.

Seed memo:
- `out/research/diminishing-returns-convergence-meter-multiagent.md` (in our workspace)
