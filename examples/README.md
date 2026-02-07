# 🧪 Examples

These transcripts are **clean-room**: created only to demonstrate DR behavior.

## 1) 🧑‍💼 [When to stop a meeting](./meeting-stop.md)
- Transcript: [`transcript.meeting-stop.json`](./transcript.meeting-stop.json)
- Walkthrough: *(see heading link)*

Why it’s useful:
- universally understood
- maps directly to “stop/ship” behavior (decision + owner + next action)

## 2) ⛵️ [Ship of Theseus](./ship-of-theseus.md)
- Transcript: [`transcript.ship-of-theseus.json`](./transcript.ship-of-theseus.json)
- Walkthrough: *(see heading link)*

Why it’s useful:
- engineer-adjacent
- maps neatly to artifact identity/provenance questions

## 3) 🀄️ [Chinese Room](./chinese-room.md)
- Transcript: [`transcript.chinese-room.json`](./transcript.chinese-room.json)
- Walkthrough: *(see heading link)*

Why it’s useful:
- a classic “define your criterion” debate
- converges naturally once scope is explicit

---

Each transcript includes:
- `outputs.claims` / `outputs.decisions` / `outputs.open_questions` / `outputs.next_actions`
- `diminishing_returns_note.recommended_stop_round`

Each example also has a checked-in **expected output** (computed, not hand-waved):
- `*.expected.json` is the JSON emitted by `dr score` for that transcript.

Run:

```bash
# after installing the package
# (or run via PYTHONPATH=src for local dev)
dr score examples/transcript.meeting-stop.json
```

