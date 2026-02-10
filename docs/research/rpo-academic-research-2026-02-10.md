# RPO academic research — annotated bibliography (2026-02-10)

This is a copy of the RPO-focused deep research packet (kept here because the diminishing-returns project is the evaluation substrate for testing RPO hypotheses).

See: `docs/deep-research-rubric.md` for the DoD and scoring rubric.

---

## 1-page synthesis: what the literature implies for “RPO”

**RPO framing:** treat prompts as *interfaces* — a “contract” between user intent and model behavior.

### Pillar 1) Prompt as program / prompt as specification
Work like **LMQL** and **DSPy** formalizes prompting with **variables, constraints, control flow, and optimization loops**. This is “prompt contracts” implemented as code.

**Implication:** RPO should be designed like an API: typed fields, explicit invariants, and defined failure modes.

### Pillar 2) Reliability via decomposition + self-verification
**CoT / least-to-most / ToT / ReAct / Reflexion / PoT / PAL** show consistent gains via decomposition, separating reasoning from execution, search, and feedback/tool use.

**Implication:** RPO “checklists” and structured sections are *cognitive scaffolds* that reduce instruction conflict and increase controllability.

### Pillar 3) Evaluation needs behavioral tests, not just average accuracy
**CheckList**, **HELM**, **BIG-bench**, **BBH** support systematic evaluation of robustness and failure modes.

**Implication:** define **contract compliance metrics**: schema validity, constraint satisfaction, refusal correctness, calibration/uncertainty, instruction hierarchy robustness, cost/latency.

### Cross-cutting hypotheses worth testing
- H1: explicit “Output Contract” increases parseable structured-output rate.
- H2: “Rules/Priority” reduces errors under conflicting constraints.
- H3: “Checklist/Verify” improves factuality/consistency.
- H4: decoding constraints/typed variables increase validity at equal/lower cost.
- H5: optimization loops (DSPy) beat static templates.

---

## Annotated bibliography (20 items)

### Theme A — Prompt programming languages, “prompt as code”, and prompt tooling

1) Fischer et al. (2023). Prompting Is Programming: A Query Language for Large Language Models (LMQL). PLDI’23.
https://arxiv.org/abs/2212.06094

2) Khattab et al. (2023). DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines.
https://arxiv.org/abs/2310.03714

3) Bach et al. (2022). PromptSource: An Integrated Development Environment and Repository for Natural Language Prompts. ACL’22 Demo.
https://arxiv.org/abs/2202.01279

### Theme B — Structured prompting for reasoning & controllability

4) Wei et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.
https://arxiv.org/abs/2201.11903

5) Kojima et al. (2022). Large Language Models are Zero-Shot Reasoners.
https://arxiv.org/abs/2205.11916

6) Wang et al. (2023). Self-Consistency Improves Chain of Thought Reasoning in Language Models. ICLR’23.
https://arxiv.org/abs/2203.11171

7) Zhou et al. (2022). Least-to-Most Prompting Enables Complex Reasoning in Large Language Models.
https://arxiv.org/abs/2205.10625

8) Yao et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS’23.
https://arxiv.org/abs/2305.10601

9) Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models.
https://arxiv.org/abs/2210.03629

10) Shinn et al. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning.
https://arxiv.org/abs/2303.11366

11) Chen et al. (2022). Program of Thoughts Prompting (PoT): Disentangling Computation from Reasoning.
https://arxiv.org/abs/2211.12588

12) Gao et al. (2022). PAL: Program-aided Language Models.
https://arxiv.org/abs/2211.10435

### Theme C — “Rules” as governance

13) Bai et al. (2022). Constitutional AI: Harmlessness from AI Feedback.
https://arxiv.org/abs/2212.08073

14) Ouyang et al. (2022). Training language models to follow instructions with human feedback (InstructGPT).
https://arxiv.org/abs/2203.02155

15) Chung et al. (2022). Scaling Instruction-Finetuned Language Models (FLAN).
https://arxiv.org/abs/2210.11416

### Theme D — Constrained outputs

16) Hokamp & Liu (2017). Lexically Constrained Decoding for Sequence Generation Using Grid Beam Search. ACL’17.
https://arxiv.org/abs/1704.07138

### Theme E — Evaluation & hallucination checks

17) Manakul et al. (2023). SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative LLMs.
https://arxiv.org/abs/2303.08896

18) Ribeiro et al. (2020). Beyond Accuracy: Behavioral Testing of NLP Models with CheckList. ACL’20.
https://arxiv.org/abs/2005.04118

19) Bommasani et al. (2022). Holistic Evaluation of Language Models (HELM).
https://arxiv.org/abs/2211.09110

20) Srivastava et al. (2022). Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models (BIG-bench).
https://arxiv.org/abs/2206.04615

Optional stress suite:
- Suzgun et al. (2022). Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them (BBH).
  https://arxiv.org/abs/2210.09261
