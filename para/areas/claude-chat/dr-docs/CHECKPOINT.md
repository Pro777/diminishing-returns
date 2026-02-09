# DR Docs Hardening — Checkpoint Log

Append-only. Each entry records state at a point in time.

---

## Checkpoint 1 — 2026-02-09T06:15Z

### PR state
| PR | State | Notes |
|----|-------|-------|
| #1 | Open (stale) | Superseded by #3 and #4 |
| #2 | Closed | WIP, never merged |
| #3 | Merged | Hardening follow-ups (normalization, K-consecutive, tests) |
| #4 | Merged | Merge-forward of #1 content |
| #5 | Open | This branch (docs hardening) |

### Branch state
- `claude/sweet-payne` rebased onto `origin/main` (includes #3 and #4)
- No merge conflicts
- 8 unit tests pass locally
- `dr score` verified on all 8 example files

### Ground truth audit (src/ vs docs)

| Feature | src/ | README | Rubric | Roadmap | DA |
|---------|------|--------|--------|---------|-----|
| Normalized-string novelty | `score.py:7-9` | Correct | Correct | Correct | Correct |
| Per-round dedupe | `score.py:55-64` | — | — | Correct | — |
| K-consecutive (k=2, thresh=0.2) | `score.py:78-92` | Correct | Correct | Correct | Correct |
| Action readiness (binary) | `score.py:93-99` | Correct | Correct | Correct | Correct |
| Blocker-aware stop | `score.py:101-108` | — | Correct | Correct | — |
| stop_recommendation + confidence | `score.py:126-145` | Correct | — | Correct | — |
| Input validation | `score.py:34-53`, `io.py:26-41,63-69` | — | — | Correct | — |
| Tail window (2-round avg) | `score.py:72-75` | — | **Fixed** | — | Correct |
| Semantic similarity | `score.py:120` returns None | Correct | Correct | Correct | Correct |
| Structural agreement | `score.py:122` returns None | Correct | Correct | Correct | Correct |
| Unit tests | `tests/test_score.py` (8 tests) | — | — | **Fixed** | **Fixed** |
| CI runs tests | `ci.yml:17-18` still smoke | — | — | — | **Fixed** → CI updated |

### Changes made this round
1. Devil's advocate #9: updated from "no tests" to "tests exist, CI doesn't run them"
2. Roadmap: updated test suite status from "Planned" to "Partial"; added [x] for unit tests
3. Rubric: added tail-window detail to novelty implementation description
4. CI (`ci.yml`): replaced `print('ok')` with `python -m unittest discover -s tests -v`

### Files modified
- `docs/devils-advocate.md` — point #9 corrected
- `docs/roadmap.md` — test status and checklist updated
- `docs/rubric.md` — tail-window detail added
- `.github/workflows/ci.yml` — now runs actual tests

### Remaining known issues
- `*.expected.json` files are stale (pre-hardening format)
- PR #1 is still open (should probably be closed as superseded)
- `para/` directory tracked intentionally (task spec said "commit checkpoint every 15-20 min")

---

## Checkpoint 2 — 2026-02-09T06:45Z

### Trigger
Post-hoc review flagged self-referential contradiction: PR #5 fixes CI but DA #9 and roadmap describe CI as broken. Resolved by making docs describe post-merge state.

### Changes made
1. DA #9: rewritten from "tests exist, CI doesn't run them" to "expected output files are stale and unvalidated" — the CI gap is closed by this PR, so the critique shifts to the remaining gap
2. Roadmap: `[ ] CI runs tests` → `[x] CI runs tests` (this PR ships the fix)
3. Roadmap adoption table: updated wording to "unit tests in CI; expected.json validation pending"

### Verified
- `.github/workflows/ci.yml` confirmed in PR #5 file list via `gh pr view 5 --json files`
- CI green on prior push (both check runs pass)
- No new files added

### Remaining known issues
- `*.expected.json` files are stale (pre-hardening format) — tracked as unchecked roadmap item
- PR #1 is still open (should probably be closed as superseded)
- arXiv links in `docs/references.md` not click-verified
