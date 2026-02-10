# Deep research rubric (DR)

Use this when you (or a subagent) are asked to “do deep research” — especially for academic / technical questions.

## Definition of done (DoD)
A deep research deliverable is **not** a long scroll of links. It is:

1) **Synthesis first** (what’s true, what’s disputed, what we should do next)
2) **Annotated bibliography** (grouped by theme)
3) **Traceability** (every non-trivial claim points to a source)
4) **Testable implications** (what should we measure / falsify)

## Source hierarchy (credibility)
Prefer, in order:

1. Peer‑reviewed papers (ACL/EMNLP/NAACL, NeurIPS/ICLR/ICML, CHI, etc.)
2. arXiv + strong author/venue signals (then verify with citations/replications)
3. Technical reports from reputable labs (DeepMind, Anthropic, OpenAI, Microsoft, etc.)
4. High-quality engineering blog posts **only when** they link to primary sources or ship reproducible artifacts

Avoid:
- “prompt engineering” listicles, Medium posts without sources
- Vendor marketing pages (unless they cite the paper and you follow the citation)

## Required fields per source (minimum)
For each item:
- Citation (authors, title, year)
- Link
- 2–3 line summary
- **What it implies for RPO** (or the question at hand)
- **Hypothesis / measurement** (how we’d test it)

## Rubric (score 0–5 each)
Score the deliverable on:

1) **Relevance** — focuses on the actual mechanism (e.g., structured prompts / constraints / reliability), not general LLM surveys
2) **Credibility** — strong sources, correctly characterized (no overclaims)
3) **Coverage** — key subtopics covered; no obvious missing cornerstone papers
4) **Synthesis quality** — clear themes + tensions; not just summaries
5) **Actionability** — turns into experiments, specs, or decisions

## DR (Diminishing Returns) guidance for research
Use the normal DR notation, but interpret “rounds” as research passes:

- **DR ~0.4**: quick scan (≤ 5 sources), untriangulated
- **DR ~0.6**: solid first bibliography (8–12 sources), 1 synthesis pass
- **DR ~0.75**: grouped bibliography (15–25), contradictions noted, 2nd pass synthesis
- **DR ~0.85+**: includes falsifying/negative evidence, replication notes, and concrete experiment design

## Standard outputs
### 1-page synthesis template
- Claim(s) we’re testing
- What the literature suggests
- What’s uncertain / disputed
- Practical guidance for our system
- Experiments to run next (with success criteria)

### Search prompts (starting points)
- "prompt formatting" LLM performance study
- "structured output" large language model constraint validity
- "instruction following" evaluation prompt sensitivity
- "prompt templates" real-world LLM applications analysis
- "JSON schema" constrained decoding reliability
- "tool use" function calling evaluation robustness

## Storage
- Working notes: `out/research/`
- Promoted canonical guidance: [docs/](./)
