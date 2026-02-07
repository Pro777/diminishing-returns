# Examples

These transcripts are **clean-room**: created only to demonstrate DR behavior.

## 1) When to stop a meeting
- Transcript: `transcript.meeting-stop.json`
- Walkthrough: `meeting-stop.md`

Why it’s useful:
- universally understood
- maps directly to “stop/ship” behavior (decision + owner + next action)

## 2) Ship of Theseus
File: `transcript.ship-of-theseus.json`

Why it’s useful:
- engineer-adjacent
- maps neatly to artifact identity/provenance questions

---

Each transcript includes:
- `outputs.claims` / `outputs.decisions` / `outputs.open_questions` / `outputs.next_actions`
- `diminishing_returns_note.recommended_stop_round`

Run:

```bash
dr score examples/transcript.meeting-stop.json
```
