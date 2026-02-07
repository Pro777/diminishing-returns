# Diminishing Returns

**Two ideas enter. One decision leaves.**

A small utility for measuring **diminishing returns** in multi-agent / multi-LLM conversations.

This is **not “confidence.”** It’s a stop/ship signal: *are we still producing novel, decision-relevant information?*

## What it measures (v0.1)
A weighted score from observable transcript signals:

- **Semantic convergence**: are two agents saying the same thing?
- **Novelty rate**: are we still generating net-new claims?
- **Structural agreement**: are agents modifying each other or just rephrasing?
- **Action readiness**: are we asking more questions or ready to execute?

## Why
Teams waste cycles in “one more round” loops.

A diminishing-returns meter nudges you toward the next correct move: **run the test, cut the PR, ship the artifact**.

## Quick start (planned)

```bash
# install
python -m pip install diminishing-returns

# score a transcript
dr score transcript.json
```

## Output (planned)

```json
{
  "score": 0.92,
  "components": {
    "semantic_similarity": 0.95,
    "novelty_rate": 0.10,
    "structural_agreement": 0.80,
    "action_readiness": 0.90
  },
  "hint": "Mostly converged; move to implementation and verification."
}
```

## Naming / hosting
- Canonical concept: **Diminishing Returns**
- Suggested subdomain: `diminishing-returns.proofofship.com` (alias: `dr.proofofship.com`)

## License
MIT.
