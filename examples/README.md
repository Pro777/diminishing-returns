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
- ✅ `*.expected.json` — the JSON emitted by `dr score`
- 🧵 `trace.*.jsonl` — the same transcript as an event stream (machine-friendly)

Run (either format):

```bash
# JSON transcript
dr score examples/transcript.meeting-stop.json

# JSONL trace (event stream)
dr score examples/trace.meeting-stop.jsonl
```

