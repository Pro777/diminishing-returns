# ⛵️ Example: Ship of Theseus

This clean-room transcript is engineer-adjacent: it’s really about **identity under change**.

- Transcript: [`transcript.ship-of-theseus.json`](./transcript.ship-of-theseus.json)
- Expected behavior: DR should recommend stopping around **round 5**.

## 🧮 Computed signals (from `dr score`)

- **score:** `1.0`
- **hint:** Mostly converged; move to implementation and verification.

**Novelty by round**

| round | claims | new_claims |
|---:|---:|---:|
| 1 | 3 | 3 |
| 2 | 3 | 2 |
| 3 | 3 | 2 |
| 4 | 3 | 2 |
| 5 | 3 | 1 |
| 6 | 3 | 0 |

## What’s happening round-by-round

### Round 1 — The paradox (identity vs replacement)
We set up the basic tension between continuity-based identity and parts-based identity.

See: [`transcript.ship-of-theseus.json#L6-L35`](./transcript.ship-of-theseus.json#L6-L35)

### Round 2 — Map the solution space
We enumerate the major families of answers (part-essentialism vs continuity/constitution vs deflationary 4D framing).

See: [`transcript.ship-of-theseus.json#L35-L64`](./transcript.ship-of-theseus.json#L35-L64)

### Round 3 — Artifacts are socially tracked
The key “programmer adjacent” move: artifacts are often tracked by role/history/convention, not micro-material sameness.

See: [`transcript.ship-of-theseus.json#L64-L93`](./transcript.ship-of-theseus.json#L64-L93)

### Round 4 — Hobbes’ discriminator (two claimants)
We introduce the reconstruction variant that forces an explicit criterion (maintained ship vs reassembled ship vs neither).

See: [`transcript.ship-of-theseus.json#L93-L122`](./transcript.ship-of-theseus.json#L93-L122)

### Round 5 — The tipping point (pluralism/context selection)
By round 5, we have a stable conceptual map: there are multiple legitimate “sameness relations,” and the paradox appears when we demand one relation do all the work.

See: [`transcript.ship-of-theseus.json#L122-L151`](./transcript.ship-of-theseus.json#L122-L151)

### Round 6 — Intentional taper
Round 6 mostly packages the same synthesis and suggests domain-specific stipulations.

See: [`transcript.ship-of-theseus.json#L151-L184`](./transcript.ship-of-theseus.json#L151-L184)

## Why this is a good DR demo
- It naturally converges to a small number of stable distinctions.
- Later rounds tend to add *applications/examples* rather than new structure.
- It mirrors the engineering question: **what counts as the same artifact** when parts (or versions) change?
