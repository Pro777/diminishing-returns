# References (receipts)

This project is a practical tool, not a literature review. But the core idea — **stop when novelty collapses and stability is high** — is informed by existing work on multi-agent debate, self-refinement loops, semantic similarity metrics, and convergence/stability detection.

Below is a short, opinionated bibliography with **one-line "why it matters" receipts**.

## Multi-agent debate / critique loops

- **Du et al., "Improving Factuality and Reasoning in Language Models through Multiagent Debate" (2023)**
  - arXiv: [2305.14325](https://arxiv.org/abs/2305.14325)
  - Why: demonstrates that multi-agent debate improves factuality but shows diminishing gains after 3-4 rounds — exactly the plateau DR aims to detect.
  - Note: we treat agreement as *a stop signal*, not as correctness. Their work shows agreement can emerge from conformity pressure, not just truth-seeking.

- **Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback" (NeurIPS 2023)**
  - arXiv: [2303.17651](https://arxiv.org/abs/2303.17651)
  - Why: self-critique/revise loops improve outputs for 2-3 iterations, then plateau or degrade. DR provides the termination nudge that Self-Refine lacks.

- **Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" (NeurIPS 2023)**
  - arXiv: [2303.11366](https://arxiv.org/abs/2303.11366)
  - Why: reflexion-style loops accumulate observations across attempts; the marginal value of each new reflection decays — a natural fit for DR-style monitoring.

## Convergence / stability detection

- **Liang et al., "Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate" (2023)**
  - arXiv: [2305.19118](https://arxiv.org/abs/2305.19118)
  - Why: explicitly studies convergence dynamics in multi-agent settings. Shows that agents converge rapidly (often 2-3 rounds) and that post-convergence rounds add noise, not signal.

- **Emergent consensus risks in multi-agent LLM systems**
  - Why: highlights *false convergence* via compression — agents sound aligned without genuinely resolving disagreement. DR should detect this but currently cannot (semantic similarity not yet implemented).

## Semantic similarity metrics

- **Reimers & Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks" (EMNLP 2019)**
  - arXiv: [1908.10084](https://arxiv.org/abs/1908.10084)
  - Why: SBERT embeddings + cosine similarity is the planned v0.2 approach for semantic convergence detection. Cheap, fast, well-understood.

- **Zhang et al., "BERTScore: Evaluating Text Generation with BERT" (ICLR 2020)**
  - arXiv: [1904.09675](https://arxiv.org/abs/1904.09675)
  - Why: alternative similarity signal (heavier than SBERT) useful for offline evaluation of round-over-round stability.

## Diversity / redundancy

- **Carbonell & Goldstein, "The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries" (SIGIR 1998)**
  - Why: MMR captures the relevance-vs-redundancy tradeoff. DR's novelty metric is essentially detecting when redundancy dominates relevance.

- **Friedman & Dieng, "The Vendi Score: A Diversity Evaluation Metric for Machine Learning" (TMLR 2023)**
  - arXiv: [2210.02410](https://arxiv.org/abs/2210.02410)
  - Why: a principled diversity metric. Could be adapted for DR to measure "how diverse are the claims across rounds" as an alternative to set-diff novelty.

## Failure modes

- **Chan et al., "ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate" (2023)**
  - arXiv: [2308.07201](https://arxiv.org/abs/2308.07201)
  - Why: documents failure modes in multi-agent evaluation including groupthink, position bias, and sycophantic agreement. Reminds us that consensus is not truth — DR should always recommend verification.

---

> **Note:** This bibliography is deliberately concise and opinionated. It prioritizes papers that directly inform DR's design choices over comprehensive literature coverage. If a reference is missing, it's probably because the connection to DR's stop/ship decision was too indirect to justify inclusion.
