# CLAUDE.md

Notes for Claude (or any AI pair) working in this repo.

## What this repo is
A diminishing-returns meter for multi-round / multi-agent conversations.
It is a **stop/ship signal**, not a truth detector.

## What to optimize for
- Ship a usable CLI + clear examples.
- Keep transcript formats stable and well documented.
- Prefer reproducible artifacts over hand-wavy numbers.

## Constraints
- Do not claim “confidence” or correctness.
- Do not embed computed scores into transcripts; keep scores derived.
- Keep examples **clean-room** (no personal data).

## When making changes
- Update docs if behavior changes.
- Update `examples/*.expected.json` if scoring changes.
- Prefer relative links in repo markdown.
