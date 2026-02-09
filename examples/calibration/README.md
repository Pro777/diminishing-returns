# Calibration Examples

Adversarial and boundary-case transcripts for testing the novelty detection and action readiness spec.

Each JSON file is a valid v0.1 transcript with an additional `_expected` section documenting the expected scoring output. The `_expected` section is **not** part of the transcript schema — it is test metadata for implementation validation.

## Examples

| File | Scenario | Expected signal |
|---|---|---|
| `paraphrase-rounds.json` | Paraphrased claims (L0 misses, L1 catches) | SHIP |
| `exact-repeat.json` | Exact-repeat rounds (baseline) | SHIP |
| `low-novelty-high-readiness.json` | Converged with clear next actions | SHIP |
| `low-novelty-low-readiness.json` | Converged but stuck/blocked | ESCALATE |
| `high-novelty-low-readiness.json` | Active exploration, not ready | CONTINUE |
| `high-novelty-high-readiness.json` | Productive with specific actions | CONTINUE |
| `blocker-present.json` | Low novelty, blocker detected | ESCALATE |
| `question-accumulation.json` | Questions growing, moderate novelty | CONTINUE |

## How to use

These examples serve two purposes:

1. **Implementation testing:** Assert that `score_transcript()` produces the expected novelty classification, readiness classification, and stop recommendation for each example.
2. **Threshold calibration:** If thresholds change, re-run all calibration examples and verify the expected signals still hold.

## Schema

Each `_expected` section contains:

```json
{
  "novelty_classification": "LOW | MEDIUM | HIGH",
  "novelty_rate_L0": 0.0,
  "novelty_rate_L1": 0.0,
  "readiness_classification": "LOW | MEDIUM | HIGH",
  "stop_recommendation": "SHIP | CONTINUE | ESCALATE",
  "notes": "Why this example matters."
}
```

Fields suffixed with `_approximate` indicate values that depend on fuzzy matching and may vary slightly with implementation details.

See [../../docs/novelty-and-readiness-spec.md](../../docs/novelty-and-readiness-spec.md) for the full spec.
