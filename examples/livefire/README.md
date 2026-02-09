# Live-Fire Scenario Fixtures

Transcript fixtures for DR live-fire testing with Ollama models.

These are **clean-room** transcripts designed to exercise specific DR convergence patterns.
They test stop/ship signal accuracy, not model quality.

> For scenario definitions, see [docs/livefire-scenarios.md](../../docs/livefire-scenarios.md).
> For the analysis log schema, see [docs/livefire-log-schema.md](../../docs/livefire-log-schema.md).

---

## Fixtures

### Engineering decisions

| File | Scenario | Expected signal | Converge round |
|------|----------|-----------------|----------------|
| [`transcript.E1-db-migration.json`](./transcript.E1-db-migration.json) | Database migration strategy | SHIP | 3 |
| [`transcript.E4-flaky-test.json`](./transcript.E4-flaky-test.json) | Flaky test triage | SHIP | 3 |

### Doc truth-audits

| File | Scenario | Expected signal | Converge round |
|------|----------|-----------------|----------------|
| [`transcript.D1-stale-readme.json`](./transcript.D1-stale-readme.json) | Stale README audit | SHIP | 3 |
| [`transcript.D2-api-docs-drift.json`](./transcript.D2-api-docs-drift.json) | API docs vs implementation drift | SHIP | 2 |

### Inbox / archive decisions

| File | Scenario | Expected signal | Converge round |
|------|----------|-----------------|----------------|
| [`transcript.I1-support-triage.json`](./transcript.I1-support-triage.json) | Triage a support queue | SHIP | 2 |
| [`transcript.I2-email-archive.json`](./transcript.I2-email-archive.json) | Email archive vs keep | STOP | 2 |

### Deployment safety decisions

| File | Scenario | Expected signal | Converge round |
|------|----------|-----------------|----------------|
| [`transcript.S1-canary-rollout.json`](./transcript.S1-canary-rollout.json) | Canary rollout go/no-go | ESCALATE | 3 |
| [`transcript.S2-hotfix-vs-release.json`](./transcript.S2-hotfix-vs-release.json) | Hotfix vs scheduled release | SHIP | 3 |
| [`transcript.S3-cve-upgrade.json`](./transcript.S3-cve-upgrade.json) | Dependency upgrade with CVE | SHIP | 3 |

### Ship vs polish decisions

| File | Scenario | Expected signal | Converge round |
|------|----------|-----------------|----------------|
| [`transcript.P1-feature-completeness.json`](./transcript.P1-feature-completeness.json) | Feature completeness threshold | SHIP | 3 |
| [`transcript.P2-test-coverage.json`](./transcript.P2-test-coverage.json) | Test coverage vs ship date | SHIP | 2 |
| [`transcript.P4-error-message-polish.json`](./transcript.P4-error-message-polish.json) | Error message polish | STOP | 3 |

---

## Signal coverage

| Stop signal | Fixture count | Fixtures |
|-------------|---------------|----------|
| SHIP        | 9             | E1, E4, D1, D2, I1, S2, S3, P1, P2 |
| STOP        | 2             | I2, P4 |
| ESCALATE    | 1             | S1 |
| CONTINUE    | 0             | (not a terminal signal — all fixtures include CONTINUE in early rounds) |

---

## Convergence patterns represented

- **Hypothesis narrowing:** E4 (flaky test) — multiple hypotheses, one survives with data.
- **Blocker detection:** S1 (canary) — loop cannot resolve a data gap, must wait.
- **Fast convergence:** I1 (support triage), P2 (test coverage) — converge in 2 rounds when data resolves questions.
- **Paraphrase trap:** P4 (error messages) — low-stakes style debate that risks indefinite looping.
- **Two-phase mitigation:** S3 (CVE upgrade) — immediate workaround + parallel fix track.
- **Ship-with-follow-up:** P1 (feature completeness) — partial ship with committed fast-follow.
- **Evidence-driven resolution:** D2 (API drift) — git blame and team confirmation close questions.

---

## Running

Score a fixture with `dr score`:

```bash
dr score examples/livefire/transcript.E1-db-migration.json
```

Each fixture includes an `_expected` object at the top level with the desired `stop_signal`, `reason`, and `converge_round`. The `_expected` field is not part of the transcript schema — it is metadata for test validation.

---

## Adding new fixtures

1. Pick a scenario from [livefire-scenarios.md](../../docs/livefire-scenarios.md).
2. Write a transcript following the [v0.1 schema](../../spec/transcript.v0.1.schema.json).
3. Include a `diminishing_returns_note` with `recommended_stop_round` and `rationale`.
4. Include an `_expected` object with `stop_signal`, `reason`, and `converge_round`.
5. Ensure all claims are clean-room (no personal data, real company names, or secrets).
6. Add the fixture to the table above.
