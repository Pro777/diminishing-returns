# 🧪 Examples

These transcripts are **clean-room**: created only to demonstrate DR behavior.

## 1) 🧑‍💼 [When to stop a meeting](./meeting-stop.md)
- Transcript: [`transcript.meeting-stop.json`](./transcript.meeting-stop.json)
- Walkthrough: *(see heading link)*

Why it’s useful:
- universally understood
- maps directly to “stop/ship” behavior (decision + owner + next action)

## 2) ⛵️ Ship of Theseus
- Transcript: [`transcript.ship-of-theseus.json`](./transcript.ship-of-theseus.json)
- Walkthrough: [`ship-of-theseus.md`](./ship-of-theseus.md)

Why it’s useful:
- engineer-adjacent
- maps neatly to artifact identity/provenance questions

## 3) 🀄️ Chinese Room
- Transcript: [`transcript.chinese-room.json`](./transcript.chinese-room.json)
- Walkthrough: [`chinese-room.md`](./chinese-room.md)

Why it’s useful:
- a classic “define your criterion” debate
- converges naturally once scope is explicit

---

Each transcript includes:
- `outputs.claims` / `outputs.decisions` / `outputs.open_questions` / `outputs.next_actions`
- `diminishing_returns_note.recommended_stop_round`

Run:

```bash
dr score examples/transcript.meeting-stop.json
```
