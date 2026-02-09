# DR Attestation Spec v0.1

> A portable trust signal for inter-agent communication.

## Status

**Draft.** This spec describes the target wire format for DR attestations. The local tier (markdown convention) is implemented. The federated and internet tiers are specified but not yet implemented.

## Problem

When Agent A sends a recommendation to Agent B, B has no way to gauge how much scrutiny that recommendation received. Did A think for 30 seconds or run three rounds of adversarial review? Without this signal, B must either blindly trust A or re-do all the work.

DR attestations solve this by attaching a machine-readable trust signal to any inter-agent message.

## Design Principles

1. **Lightweight at the local tier.** A markdown line is enough for trusted environments.
2. **Auditable at the federated tier.** Signatures and evidence URIs for partially-trusted peers.
3. **Verifiable at the internet tier.** Full evidence bundles, independent re-scoring, replay protection.
4. **Backwards compatible.** Always additive. A system that doesn't understand DR ignores the attestation and reads the message normally.

---

## Attestation Object

Every DR attestation is a JSON object with a stable schema.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `dr_version` | string | Spec version. Currently `"0.1"`. |
| `id` | string | Globally unique identifier. Format: `dr:<UUIDv4>`. |
| `timestamp` | string | ISO 8601 UTC. When the attestation was created. |
| `origin` | object | Who produced this attestation (see Origin). |
| `claim` | string | The recommendation or statement being attested. |
| `score` | number | DR convergence score, 0.0–1.0. |
| `rounds` | integer | Number of review/revision cycles. |
| `method` | string | How the score was produced (see Method Labels). |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `refs` | array[string] | IDs of prior attestations this one builds on. |
| `evidence_uri` | string | URI to the full evidence bundle (transcript, rounds). |
| `evidence_hash` | string | SHA-256 of the evidence bundle (for integrity). |
| `signature` | string | Cryptographic signature over the attestation (see Signing). |
| `expires` | string | ISO 8601 UTC. After this time, the attestation should be re-evaluated. |
| `tags` | array[string] | Freeform labels (e.g., `["security", "architecture"]`). |
| `supersedes` | string | ID of a prior attestation this one replaces. |

### Origin Object

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string | Identifier for the producing agent. Freeform at local tier; URI or DID at higher tiers. |
| `system` | string | The system/model that produced the work (e.g., `"claude-code/opus-4.6"`). |
| `trust_domain` | string | The trust boundary this agent belongs to (e.g., `"clawd.local"`, `"spitfirecowboy.com"`). |

### Method Labels

Standard labels for the `method` field:

| Label | Meaning |
|-------|---------|
| `solo` | Single agent, no adversarial review |
| `N-subagent` | N subagents reviewed and converged (e.g., `2-subagent`) |
| `cross-agent` | Another named agent in the same trust domain reviewed |
| `human-reviewed` | A human reviewed and approved |
| `DA` | Devil's advocate pass was run |
| `re-scored` | A receiving agent independently re-scored the evidence |

Labels can be combined with `+`: `"2-subagent + DA + human-reviewed"`.

---

## Trust Tiers

### Tier 1: Local (Trusted)

- **Transport:** Markdown front matter, file system
- **Verification:** None required
- **Identity:** Agent names (Campion, Seton, Rowan)
- **Format:** Inline markdown or full JSON

Markdown shorthand:

```markdown
**DR:** 0.85 / 3 rounds / 2-subagent + DA
**DR-ID:** dr:550e8400-e29b-41d4-a716-446655440000
```

### Tier 2: Federated (Partially Trusted)

- **Transport:** Webhooks, MCP tool results, shared APIs
- **Verification:** Signature check, optional evidence spot-check
- **Identity:** Signing key or OIDC identity (e.g., via Sigstore)
- **Format:** Full JSON with `signature` field

The receiving agent verifies the signature and may spot-check the evidence URI. The `trust_domain` in the origin tells the receiver what trust boundary the attestation comes from.

### Tier 3: Internet (Untrusted)

- **Transport:** HTTP, email, public APIs
- **Verification:** Full evidence audit, independent re-scoring
- **Identity:** DIDs, public keys, or Sigstore keyless signing
- **Format:** Full JSON with `signature`, `evidence_uri`, `evidence_hash`

The receiving agent:
1. Verifies the signature
2. Fetches the evidence bundle
3. Verifies `evidence_hash` matches the bundle
4. Optionally runs `dr score` on the evidence independently
5. Compares its own score against the claimed score

If scores diverge significantly, the attestation is flagged as unreliable.

---

## Evidence Bundles

An evidence bundle is a standard DR transcript (per `transcript.v0.1.schema.json`) with optional metadata:

```json
{
  "version": "0.1",
  "conversation_id": "...",
  "attestation_id": "dr:550e8400-...",
  "rounds": [ ... ],
  "participants": [
    {"agent_id": "campion@clawd.local", "role": "proposer"},
    {"agent_id": "subagent-1", "role": "reviewer"},
    {"agent_id": "subagent-2", "role": "reviewer"}
  ]
}
```

This reuses the existing transcript schema and adds `attestation_id` and `participants` for traceability.

---

## Lifecycle

### Creation

An agent produces an attestation when it makes a recommendation that crosses any boundary (agent, system, trust domain).

### Reference

Other attestations can cite prior ones via the `refs` field. This creates a DAG of trust — you can trace any decision back through its attestation chain.

### Supersession

When a recommendation is revised, the new attestation includes `supersedes` pointing to the old one. The old attestation is not deleted but is marked as superseded.

### Expiration

Attestations can include an `expires` field. After expiration, the claim should be re-evaluated. This prevents stale recommendations from persisting unchallenged.

### Revocation

An attestation can be revoked by publishing a new attestation with:
- `supersedes` pointing to the revoked ID
- `score: 0.0`
- `claim` explaining why it was revoked

---

## Implementation Maturity

| Feature | Status | Notes |
|---------|--------|-------|
| Markdown shorthand (`**DR:** ...`) | In use | Local tier convention |
| Full attestation JSON object | Specified | No tooling generates this yet |
| `dr attest` CLI | Not implemented | Planned for v0.2 |
| UUID generation (`dr:<UUIDv4>`) | Not implemented | Planned for v0.2 |
| Evidence bundles | Specified | No tooling creates or consumes these |
| Sigstore signing | Specified | Not implemented; dependency not added |
| `dr verify` re-scoring | Specified | Planned for v0.4 |
| Attestation DAG | Specified | No tooling or visualization exists |
| Revocation | Specified | No mechanism to discover revocations |
| Expiration | Specified | No tooling enforces TTL checks |

---

## Open Questions

These are design decisions that remain unresolved. They should be answered before the spec moves beyond draft status.

### 1. Score Semantics Across Versions

If v0.1 scores are based on exact-string novelty and v0.2 scores use semantic embeddings, a `score: 0.85` means different things depending on which version produced it. Should the attestation include `scoring_version` separately from `dr_version`? Or should `dr_version` be bumped whenever scoring semantics change?

### 2. Evidence Bundle Privacy

Evidence bundles contain full conversation transcripts. In federated and internet tiers, this may expose proprietary reasoning, internal deliberation, or sensitive context. Should the spec define a "redacted evidence" format that proves convergence without revealing content?

### 3. Clock Trust

The `timestamp` field is self-reported. A malicious agent can backdate or future-date an attestation. At the internet tier, should timestamps be attested by a third party (e.g., RFC 3161 timestamping)?

### 4. Score Gaming

An agent can fabricate a high DR score by constructing a synthetic transcript that converges on demand. At the internet tier, `dr verify` can catch this by re-scoring — but only if the evidence is genuine. Should the spec require evidence bundles at the federated tier, not just the internet tier?

### 5. Revocation Discovery

The revocation mechanism (publish a new attestation with `supersedes` and `score: 0.0`) assumes the receiver will discover the revoking attestation. There is no push notification, no registry, and no guaranteed delivery. Is this acceptable, or does revocation need a side channel?

### 6. What Counts as a "Round"?

The spec assumes `rounds` is a well-defined integer. But in real agent interactions, a "round" might be a single exchange, a batch of parallel subagent calls, or a human review that spans days. Should the spec define what constitutes a round, or leave it to the attestor?

---

## Non-Goals (v0.1)

- **Correctness verification.** DR measures convergence, not truth. An attestation with score 1.0 means "fully converged," not "definitely correct."
- **Access control.** DR attestations are informational, not authorization tokens.
- **Consensus protocol.** DR does not define how agents reach agreement — only how they report their confidence in the result.

---

## Examples

### Local tier (markdown)

```markdown
# Campion → Rowan: Database connection pooling proposal

**Date:** 2026-02-08
**Audience:** Rowan (review + execute)
**DR:** 0.85 / 3 rounds / 2-subagent + DA
**DR-ID:** dr:550e8400-e29b-41d4-a716-446655440000

## Recommendation
Use PgBouncer for connection pooling...
```

### Federated tier (JSON)

```json
{
  "dr_version": "0.1",
  "id": "dr:550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-08T14:30:00Z",
  "origin": {
    "agent_id": "campion@clawd.local",
    "system": "claude-code/opus-4.6",
    "trust_domain": "clawd.spitfirecowboy.com"
  },
  "claim": "Use PgBouncer for connection pooling in the Rails app",
  "score": 0.85,
  "rounds": 3,
  "method": "2-subagent + DA",
  "refs": [],
  "evidence_uri": "https://clawd.spitfirecowboy.com/evidence/550e8400.json",
  "evidence_hash": "sha256:abc123...",
  "signature": "sigstore:..."
}
```

---

*"Two ideas enter. One decision leaves." — but the decision carries a receipt.*
