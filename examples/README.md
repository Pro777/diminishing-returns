# 🧪 Examples

These transcripts are **clean-room**: created only to demonstrate DR behavior.

## 1) 🧑‍💼 [When to stop a meeting](./meeting-stop.md)
- Transcript: [`transcript.meeting-stop.json`](./transcript.meeting-stop.json)

Why it’s useful:
- universally understood
- maps directly to “stop/ship” behavior (decision + owner + next action)

## 2) ⛵️ [Ship of Theseus](./ship-of-theseus.md)
- Transcript: [`transcript.ship-of-theseus.json`](./transcript.ship-of-theseus.json)

Why it’s useful:
- engineer-adjacent
- maps neatly to artifact identity/provenance questions

## 3) 🀄️ [Chinese Room](./chinese-room.md)
- Transcript: [`transcript.chinese-room.json`](./transcript.chinese-room.json)

Why it’s useful:
- a classic “define your criterion” debate
- converges naturally once scope is explicit

---

Each transcript includes:
- `outputs.claims` / `outputs.decisions` / `outputs.open_questions` / `outputs.next_actions`
- `diminishing_returns_note.recommended_stop_round`

Each example also has checked-in computed artifacts:
- ✅ [`*.expected.json`](./transcript.meeting-stop.expected.json) — the JSON emitted by `dr score`
- 🧵 [`trace.*.jsonl`](./trace.meeting-stop.jsonl) — the same transcript as an event stream (machine-friendly)

Run (either format):

```bash
# JSON transcript
dr score examples/transcript.meeting-stop.json

# JSONL trace (event stream)
dr score examples/trace.meeting-stop.jsonl
```

---

## Score range across examples

Post-hardening, the three examples now show meaningful variation:

| Example | Score | Stop recommended? | Why |
|---------|-------|-------------------|-----|
| Meeting stop | 1.0 | Yes | 2 consecutive low-novelty rounds, no blockers |
| Ship of Theseus | 0.83 | No | Open questions in latest round block the stop signal |
| Chinese Room | 0.75 | No | Only 1 consecutive low-novelty round (needs 2) |

This demonstrates three different DR outcomes: full convergence, blocked convergence, and still-productive.

## What's still missing

- A **very low-DR** transcript (score < 0.5) showing a conversation in its early productive phase
- A **false convergence** transcript where agents agree but are wrong
- A **blocker-cleared** example where removing open questions flips the stop recommendation

These gaps are tracked in the [roadmap](../docs/roadmap.md).

> **Note:** The `*.expected.json` files are checked in but are now stale (they predate the hardening changes). They are not validated by CI. Updating them and adding automated validation is tracked as a v0.1 stabilization item.

