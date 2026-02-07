# 🧑‍💼 Example: When to stop a meeting

This example is a clean-room transcript meant to be instantly legible to product and business folks.

- Transcript: [`transcript.meeting-stop.json`](./transcript.meeting-stop.json)
- Expected behavior: DR should recommend stopping around **round 4**.

## 🧮 Computed signals (from `dr score`)

- **score:** `1.0`
- **hint:** Mostly converged; move to implementation and verification.

**Novelty by round**

| round | claims | new_claims |
|---:|---:|---:|
| 1 | 4 | 4 |
| 2 | 3 | 1 |
| 3 | 3 | 1 |
| 4 | 3 | 1 |
| 5 | 1 | 0 |
| 6 | 2 | 0 |

## What’s happening round-by-round

### Round 1 — Establish the stop criteria vocabulary
We introduce the basic control concepts (see [`transcript.meeting-stop.json#L7-L31`](./transcript.meeting-stop.json#L7-L31)):
- a meeting has a **purpose**
- meetings need **timeboxes**
- if the purpose is unclear, continued discussion tends to go negative-ROI
- a meeting ends well only if it produces a **decision + next action**

At this point, novelty is high. We’re still mapping the space.

### Round 2 — Tighten “decision” into something checkable
A key refinement: “decision” only counts if it’s paired with **owner + next action + deadline** (see [`transcript.meeting-stop.json#L34-L53`](./transcript.meeting-stop.json#L34-L53)).

This is the start of convergence: we’re not adding new domains; we’re making the rule operational.

### Round 3 — Add a looping / diminishing-returns stop signal
We add a DR-like heuristic: if the group is repeating without adding **new options, evidence, or constraints**, we’re looping (see [`transcript.meeting-stop.json#L55-L76`](./transcript.meeting-stop.json#L55-L76)).

That gives us a third termination condition besides purpose/timebox.

### Round 4 — The tipping point (composite rule is stable)
By round 4, the conversation has effectively converged into a compact composite rule (see [`transcript.meeting-stop.json#L78-L94`](./transcript.meeting-stop.json#L78-L94)):

> Stop when **purpose is met** OR **timebox is hit** OR **loop is detected**.

At this point, additional rounds mostly rephrase. The correct next move is packaging (checklist/script), not more discussion.

### Rounds 5–6 — Intentional taper
These rounds intentionally restate the already-stable rule to demonstrate what “diminishing returns” looks like (see rounds 5–6 in [`transcript.meeting-stop.json#L95-L131`](./transcript.meeting-stop.json#L95-L131)).

## Why this is a good DR demo
- The “stop” decision is *obvious* to humans.
- The transcript structure lets DR measure novelty directly via `outputs.claims` set-diff.
- It ends with a practical next action: **ship the checklist**.
