# 🀄️ Example: Chinese Room

This clean-room transcript is about a familiar pattern: debates that only stop once we **name the criterion** we’re actually optimizing for.

- Transcript: [`transcript.chinese-room.json`](./transcript.chinese-room.json)
- Expected behavior: DR should recommend stopping around **round 4**.

## 🧮 Computed signals (from `dr score`)

- **score:** `1.0`
- **hint:** Mostly converged; move to implementation and verification.

**Novelty by round**

| round | claims | new_claims |
|---:|---:|---:|
| 1 | 4 | 4 |
| 2 | 4 | 2 |
| 3 | 4 | 2 |
| 4 | 4 | 2 |
| 5 | 4 | 0 |

## What’s happening round-by-round

### Round 1 — Set up the ambiguity (syntax vs semantics)
We establish the core claim and the meta-problem: "understanding" is underspecified unless we say what counts as evidence.

See: [`transcript.chinese-room.json#L6-L31`](./transcript.chinese-room.json#L6-L31)

### Round 2 — Enumerate the standard replies
We map the common replies (systems/robot/brain-simulator) and split the debate into three targets: behavior, grounding, experience.

See: [`transcript.chinese-room.json#L32-L53`](./transcript.chinese-room.json#L32-L53)

### Round 3 — Convergence move: choose a criterion
We show the natural stopping point: once everyone agrees which criterion matters, further rounds tend to be rhetoric.

See: [`transcript.chinese-room.json#L54-L77`](./transcript.chinese-room.json#L54-L77)

### Round 4 — The tipping point (scope it)
We adopt a scoped, decision-friendly stance: for engineering decisions, stop at behavior + grounding proxies and bracket the rest.

See: [`transcript.chinese-room.json#L78-L96`](./transcript.chinese-room.json#L78-L96)

### Round 5 — Intentional taper
Round 5 restates the outcome to demonstrate diminishing returns.

See: [`transcript.chinese-room.json#L97-L117`](./transcript.chinese-room.json#L97-L117)

## Why this is a good DR demo
- It converges when we **name the criterion**.
- Later rounds add heat, not light.
- The next action is testable: define proxies, evaluate on tasks.
