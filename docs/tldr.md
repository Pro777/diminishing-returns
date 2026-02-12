# Diminishing Returns — Plain-English Explainer

## The one-sentence version

DR is a "should we keep talking?" meter for AI conversations.

## The problem

When you have multiple AI agents (or people) going back and forth — debating, reviewing, critiquing — how do you know when to stop? Usually someone just says "one more round" forever, or someone gets bored and stops arbitrarily. Both waste time.

## What DR does

DR watches a conversation and asks two questions:

1. **Is anyone saying anything new?** (novelty detection) — It compares each round's claims against everything said before. If round 5 is just rephrasing what was said in rounds 2 and 3, that's low novelty.

2. **Are we ready to act?** (action readiness) — Are there clear next steps? Have the open questions been resolved? Do any blockers remain?

Then it gives you one of three signals:

| Signal       | Meaning                                                                 |
|-------------|-------------------------------------------------------------------------|
| **CONTINUE** | Still learning new things, keep going.                                  |
| **SHIP**     | Nothing new is coming in and we know what to do. Stop talking, start doing. |
| **ESCALATE** | Something's stuck or weird, a human should look at this.                |

## How novelty detection works

DR doesn't need any AI models to run. It uses two layers of plain text comparison:

- **L0 (exact match):** Normalize the text (lowercase, trim leading bullets/prefixes and trailing punctuation/whitespace) and check if the same claim appeared before. Simple deduplication.
- **L1 (fuzzy match):** Break claims into tokens, remove common stopwords, and compare using Jaccard similarity. Catches paraphrases like "we should deploy on Friday" vs. "Friday deployment is recommended."

A planned L2 layer will use embeddings for deeper semantic matching, but the core works without it.

## How the stop signal works

DR bases its stop/ship decision primarily on the **most recent round's novelty rate**. It also tracks how many consecutive rounds have had low novelty — that count feeds into reporting and the ESCALATE condition (3+ rounds stuck). Combined with action readiness, this produces the CONTINUE/SHIP/ESCALATE signal.

## The trust signal angle

DR is evolving beyond a scoring library into a **trust signal for agent-to-agent communication**. When Agent A sends a recommendation to Agent B, a DR attestation tells B: "this recommendation was reviewed for 6 rounds and converged" vs. "this was a first draft, handle with care."

Three trust tiers:
- **Local** — Markdown-based, for trusted agents in the same workspace.
- **Federated** — Signed, for partially trusted agents across teams.
- **Internet** — Full evidence audit, for untrusted agents in the wild.

## What DR is not

- It is **not a truth detector**. A conversation can converge on the wrong answer. DR measures whether new information is still arriving, not whether the information is correct.
- It is **not confidence**. A high DR score means "we're done talking," not "we're right."
- It is **not an AI model**. It's a lightweight scoring utility with zero external dependencies.
