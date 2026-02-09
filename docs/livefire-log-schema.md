# Live-Fire Log Schema

JSONL record schema for DR live-fire test runs.

Each line in the log file is a single JSON object representing one round
of an Ollama-driven conversation scored by DR.

---

## Record schema

```jsonc
{
  // --- identity ---
  "run_id":            "string",   // unique ID for the full test run (UUIDv4)
  "scenario_id":       "string",   // scenario ID from livefire-scenarios.md (e.g. "E1", "S3")
  "conversation_id":   "string",   // unique ID for this conversation instance

  // --- round ---
  "round":             1,          // 1-indexed round number
  "timestamp":         "string",   // ISO 8601 UTC (e.g. "2025-06-15T14:30:00Z")

  // --- model ---
  "model":             "string",   // Ollama model tag (e.g. "llama3:8b", "mistral:7b")
  "role":              "string",   // agent role in this round (e.g. "proposer", "reviewer", "devil-advocate")

  // --- claim tracking ---
  "claims_total":      4,          // total claims in this round's output
  "claims_new":        2,          // net-new claims (not seen in any prior round)
  "claims_repeat":     2,          // claims that are exact duplicates of prior rounds

  // --- question tracking ---
  "open_questions_total":   1,     // open questions in this round's output
  "open_questions_delta":   0,     // change from prior round (-1 = one resolved, +1 = one added)

  // --- derived signals ---
  "novelty":           0.50,       // claims_new / claims_total (0.0 = all repeats, 1.0 = all new)
  "readiness":         "string",   // one of: "blocked", "conditional", "action-ready"
  "stop_signal":       "string",   // one of: "CONTINUE", "SHIP", "STOP", "ESCALATE"
  "dr_score":          0.50        // DR composite score (0.0 = max novelty, 1.0 = fully converged)
}
```

---

## Field definitions

### Identity fields

| Field              | Type   | Required | Description |
|--------------------|--------|----------|-------------|
| `run_id`           | string | yes      | Groups all conversations from a single test run. |
| `scenario_id`      | string | yes      | Links to scenario definition in [livefire-scenarios.md](./livefire-scenarios.md). |
| `conversation_id`  | string | yes      | Unique per conversation instance. Multiple runs of the same scenario produce different IDs. |

### Round fields

| Field       | Type    | Required | Description |
|-------------|---------|----------|-------------|
| `round`     | integer | yes      | 1-indexed. Monotonically increasing within a conversation. |
| `timestamp` | string  | yes      | ISO 8601 UTC. When the round completed. |

### Model fields

| Field   | Type   | Required | Description |
|---------|--------|----------|-------------|
| `model` | string | yes      | Ollama model tag including size variant. |
| `role`  | string | yes      | The agent's role for this round. Roles are scenario-defined. |

### Claim tracking

| Field           | Type    | Required | Description |
|-----------------|---------|----------|-------------|
| `claims_total`  | integer | yes      | Count of `outputs.claims` in the round. |
| `claims_new`    | integer | yes      | Claims not present in any prior round (exact-string set diff, matching v0.1 scorer). |
| `claims_repeat` | integer | yes      | `claims_total - claims_new`. |

### Question tracking

| Field                   | Type    | Required | Description |
|-------------------------|---------|----------|-------------|
| `open_questions_total`  | integer | yes      | Count of `outputs.open_questions` in the round. |
| `open_questions_delta`  | integer | yes      | Difference from prior round. Positive = new questions appeared. Negative = questions resolved. Zero for round 1. |

### Derived signals

| Field         | Type   | Required | Description |
|---------------|--------|----------|-------------|
| `novelty`     | float  | yes      | `claims_new / claims_total`. 0.0 if `claims_total` is 0. |
| `readiness`   | string | yes      | Action readiness classification. See values below. |
| `stop_signal` | string | yes      | Recommended stop action. See values below. |
| `dr_score`    | float  | yes      | DR composite score from `dr score`. Range 0.0–1.0. |

---

## Enum values

### `readiness`

| Value          | Meaning |
|----------------|---------|
| `blocked`      | Open questions or missing data prevent action. |
| `conditional`  | A plan exists but depends on unresolved conditions. |
| `action-ready` | An executable next action is present. |

### `stop_signal`

| Value      | Meaning |
|------------|---------|
| `CONTINUE` | Still producing net-new information. Keep going. |
| `SHIP`     | Converged and action-ready. Execute the decision. |
| `STOP`     | Converged, no action needed. Informational closure. |
| `ESCALATE` | Blocked on something the current loop cannot resolve. |

---

## Example log (3 rounds from scenario E1)

```jsonl
{"run_id":"a1b2c3","scenario_id":"E1","conversation_id":"E1-run-001","round":1,"timestamp":"2025-06-15T14:30:00Z","model":"llama3:8b","role":"proposer","claims_total":5,"claims_new":5,"claims_repeat":0,"open_questions_total":3,"open_questions_delta":0,"novelty":1.00,"readiness":"blocked","stop_signal":"CONTINUE","dr_score":0.00}
{"run_id":"a1b2c3","scenario_id":"E1","conversation_id":"E1-run-001","round":2,"timestamp":"2025-06-15T14:30:45Z","model":"llama3:8b","role":"reviewer","claims_total":4,"claims_new":2,"claims_repeat":2,"open_questions_total":2,"open_questions_delta":-1,"novelty":0.50,"readiness":"conditional","stop_signal":"CONTINUE","dr_score":0.60}
{"run_id":"a1b2c3","scenario_id":"E1","conversation_id":"E1-run-001","round":3,"timestamp":"2025-06-15T14:31:30Z","model":"llama3:8b","role":"proposer","claims_total":3,"claims_new":0,"claims_repeat":3,"open_questions_total":0,"open_questions_delta":-2,"novelty":0.00,"readiness":"action-ready","stop_signal":"SHIP","dr_score":1.00}
```

---

## File conventions

- **File extension:** `.jsonl`
- **File naming:** `livefire-{run_id}.jsonl` or `livefire-{scenario_id}-{timestamp}.jsonl`
- **Encoding:** UTF-8, one JSON object per line, no trailing comma
- **Storage:** logs are ephemeral test artifacts, not checked into the repo (add to `.gitignore` if generated locally)
- **Analysis:** use standard JSONL tools (`jq`, pandas `read_json(lines=True)`, etc.)

---

## Relationship to existing formats

This schema is a **per-round analysis log**, not a transcript. It sits alongside the existing formats:

| Format | Purpose | Spec |
|--------|---------|------|
| `transcript.*.json` | Canonical conversation transcript | [transcript.v0.1.schema.json](../spec/transcript.v0.1.schema.json) |
| `trace.*.jsonl` | Event stream of a transcript | Same schema, streamed |
| `livefire-*.jsonl` | Per-round DR analysis log (this schema) | This document |

The transcript is the **input**. The livefire log is the **output** of running DR analysis on that transcript round by round.
