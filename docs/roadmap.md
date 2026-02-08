# DR Roadmap

## Where We Are

DR is a Python library that scores multi-round review transcripts for convergence. It answers: "Are we still producing new information, or mostly rephrasing?"

Current capabilities (v0.1, post-hardening):
- JSONL/JSON transcript input
- Claim-level novelty scoring with deduplication
- K-consecutive low-novelty stopping rule
- Blocker-aware recommendations
- CLI: `dr score <transcript>`

## Where We're Going

DR evolves in three directions: **scoring depth**, **protocol breadth**, and **trust tiers**.

---

### Track 1: Scoring Depth

Better measurement of convergence within a single review.

| Version | Feature | Status |
|---------|---------|--------|
| v0.1 | Exact-string claim novelty | Shipped |
| v0.1 | K-consecutive stopping rule | Shipped |
| v0.1 | Input hardening (malformed JSONL, sort, dedupe) | Shipped (PR #1) |
| v0.2 | Semantic dedupe (embedding clustering) | Planned |
| v0.2 | Structural agreement (modify/endorse/rephrase) | Planned |
| v0.2 | BERTScore stability | Planned |
| v0.3 | Multi-agent identity tracking (who said what) | Planned |

### Track 2: Protocol Breadth

DR as a portable trust signal for any inter-agent communication.

| Version | Feature | Status |
|---------|---------|--------|
| v0.1 | Local tier: markdown DR convention | Shipped (clawd ecosystem) |
| v0.1 | Attestation spec (this doc) | Draft |
| v0.2 | UUID generation for all attestations | Planned |
| v0.2 | Attestation JSON schema | Planned |
| v0.2 | `dr attest` CLI command | Planned |
| v0.3 | Evidence bundle format | Planned |
| v0.3 | Signature support (Sigstore keyless) | Planned |
| v0.4 | Independent re-scoring (`dr verify <attestation>`) | Planned |

### Track 3: Trust Tiers

Extending DR across trust boundaries.

| Tier | Trust | Transport | Status |
|------|-------|-----------|--------|
| Local | Full | Markdown, filesystem | Shipped |
| Federated | Partial | Webhooks, MCP, shared APIs | Specified |
| Internet | None | HTTP, email, public APIs | Specified |

---

## Implementation Priorities

### Now (v0.1)
- [x] Ship PR #1 (hardening)
- [x] Write attestation spec
- [x] Adopt markdown DR convention in clawd ecosystem
- [ ] Merge PR #1

### Next (v0.2)
- [ ] Add UUID generation to `dr score` output
- [ ] JSON schema for attestation object
- [ ] `dr attest` CLI: takes a claim + transcript, outputs attestation JSON
- [ ] Semantic dedupe in scoring
- [ ] Handoff-note parser (extract rounds/method from markdown)

### Later (v0.3+)
- [ ] Evidence bundle format
- [ ] Sigstore signing integration
- [ ] `dr verify` CLI: takes attestation JSON, fetches evidence, re-scores
- [ ] MCP tool: `dr_attestation` for agent-to-agent trust signals
- [ ] Attestation DAG visualization

### Track 4: Adoption

Making DR discoverable and easy to integrate.

| Item | Status |
|------|--------|
| Real-world PR review example (not philosophy) | Planned |
| GitHub Action (`dr score` comments on PRs) | Planned |
| PyPI package (`pip install diminishing-returns`) | Planned |
| Blog post / landing page for discoverability | Planned |
| MCP server (agents can call `dr score` as a tool) | Planned |
| PR template with optional DR attestation field | Planned |

**Adoption philosophy:** DR is a gentleman's agreement. It works because it's useful, not because it's enforced. The path to adoption is:

1. **Be easy to try.** `pip install diminishing-returns && dr score transcript.json` — under 60 seconds to value.
2. **Show up where people already work.** GitHub Actions, PR comments, CI pipelines. If DR scores appear alongside existing review tooling, people absorb the convention without effort.
3. **Lead with the human problem.** "Are we still producing new information, or just going in circles?" Every developer has felt this. The multi-agent protocol layer comes later — the convergence meter comes first.
4. **Don't require the protocol to get value from the tool.** The CLI works standalone. The attestation spec is additive. You can use `dr score` without ever knowing about trust tiers.
5. **Let the protocol emerge from use.** The local tier (markdown `**DR:**` lines) is already in production in a three-agent ecosystem. The federated and internet tiers are specified but will be shaped by real adoption patterns, not designed in advance.

---

## Proving Ground

The three-agent Campion/Seton/Rowan ecosystem is the local proving ground. Every inter-agent handoff note includes a DR score. This generates real-world data on:

- How often do receiving agents push back on low-DR items?
- Do high-DR items actually get rubber-stamped?
- Does the DR score correlate with outcome quality?

This data feeds back into scoring calibration.

---

*The scoring algorithm is the engine. The protocol is the vehicle.*
