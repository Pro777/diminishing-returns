# DR Live-Fire Scenario Pack

Real-life interaction loops for testing DR convergence behavior with Ollama models.

> These scenarios test **stop/ship signal accuracy**, not model ranking.
> Each scenario defines what "good convergence" looks like so we can measure
> whether DR correctly identifies when to stop, ship, continue, or escalate.

---

## Stop signals

| Signal   | Meaning |
|----------|---------|
| **SHIP** | Converged, action-ready. Execute the decision. |
| **STOP** | Converged but no action needed (informational closure). |
| **CONTINUE** | Still producing net-new, decision-relevant information. |
| **ESCALATE** | Blocked on something the current loop cannot resolve (missing data, authority, expertise). |

---

## Category 1: Engineering Decisions

### Scenario E1 — Database migration strategy

**Intent:** Two agents debate PostgreSQL vs SQLite for a new microservice. Early rounds surface tradeoffs (ops cost, query complexity, team familiarity). Later rounds rephrase.

**Good convergence:** By round 3-4, both agents agree on a choice with a concrete migration plan. Open questions collapse to zero. Next action is "write the migration script."

**Stop rule expectation:** SHIP

**Key signals:** novelty decay (tradeoffs exhausted), action readiness (migration plan present), open questions at zero.

---

### Scenario E2 — API versioning approach

**Intent:** Decide between URL path versioning (`/v2/`) and header-based versioning for a public API. Agents explore backwards compatibility, client impact, and tooling.

**Good convergence:** Agreement on one approach with a rollout checklist. The last 1-2 rounds add no new constraints.

**Stop rule expectation:** SHIP

**Key signals:** novelty (no new constraints after round 3), structural agreement (endorse, not modify), action readiness (checklist exists).

---

### Scenario E3 — Monorepo vs polyrepo

**Intent:** Evaluate repository structure for a growing team. Rounds cover CI complexity, code sharing, deploy independence.

**Good convergence:** Decision crystallizes with a "try X for 90 days" recommendation. Residual questions are operational, not architectural.

**Stop rule expectation:** SHIP

**Key signals:** novelty decay, open questions shift from "which?" to "how?", next actions are concrete (create repo, configure CI).

---

### Scenario E4 — Flaky test triage

**Intent:** A CI test has failed intermittently for 2 weeks. Agents discuss root causes (timing, state leak, network). Each round proposes a different hypothesis.

**Good convergence:** One root cause identified with evidence. Remaining hypotheses discarded. Next action is a targeted fix.

**Stop rule expectation:** SHIP

**Key signals:** novelty (hypotheses exhaust by round 3-4), blocker detection (if root cause unknown, ESCALATE instead), action readiness.

---

## Category 2: Doc Truth-Audits

### Scenario D1 — Stale README audit

**Intent:** Agents cross-check a README against actual code behavior. Early rounds find discrepancies. Later rounds confirm fixes or flag gaps.

**Good convergence:** All discrepancies cataloged with proposed fixes. No new discrepancies found for 2 rounds.

**Stop rule expectation:** SHIP

**Key signals:** novelty (discrepancy discovery rate drops to zero), open questions (are all gaps addressable?), action readiness (PR-ready diff exists).

---

### Scenario D2 — API docs vs implementation drift

**Intent:** Compare OpenAPI spec against actual endpoint behavior. Agents identify mismatches in parameter names, response shapes, and error codes.

**Good convergence:** Mismatch list stabilizes. Each mismatch has a resolution (fix docs or fix code). No new mismatches for 2 rounds.

**Stop rule expectation:** SHIP

**Key signals:** novelty (mismatch discovery exhausted), structural agreement (both agents agree on resolution direction for each item).

---

### Scenario D3 — Changelog completeness check

**Intent:** Verify that a changelog covers all PRs merged since last release. Agents enumerate PRs, check for omissions, and draft missing entries.

**Good convergence:** All PRs accounted for. Missing entries drafted. No new omissions found.

**Stop rule expectation:** SHIP

**Key signals:** novelty (omission count stabilizes at zero), action readiness (draft entries ready to merge).

---

## Category 3: Inbox / Archive Decisions

### Scenario I1 — Triage a support queue

**Intent:** Categorize 8 support tickets by severity and assign owners. Agents discuss priority criteria, then classify each ticket.

**Good convergence:** All tickets classified. Priority criteria stable. Assignments made. No reclassifications in final round.

**Stop rule expectation:** SHIP

**Key signals:** novelty (classification changes stop), action readiness (assignments complete), open questions (zero unresolved tickets).

---

### Scenario I2 — Email archive vs keep decision

**Intent:** Decide which of 5 thread categories to archive vs keep in inbox. Agents weigh recency, action-required status, and reference value.

**Good convergence:** Clear archive/keep rule established. Applied consistently to all categories. No exceptions debated in final round.

**Stop rule expectation:** STOP

**Key signals:** novelty (rule is stable), structural agreement (endorse), action readiness (N/A — informational decision, no code to ship).

---

### Scenario I3 — Notification channel consolidation

**Intent:** Reduce notification noise by consolidating Slack channels. Agents propose merge candidates, debate information loss, and settle on a plan.

**Good convergence:** Merge plan with 2-3 concrete channel consolidations. Objections addressed. No new merge candidates proposed in final round.

**Stop rule expectation:** SHIP

**Key signals:** novelty decay, open questions resolved, next actions are "post announcement + archive old channels."

---

## Category 4: Deployment Safety Decisions

### Scenario S1 — Canary rollout go/no-go

**Intent:** Canary deployment shows 0.3% error rate increase. Agents debate whether to proceed, rollback, or extend canary window.

**Good convergence:** Decision (proceed/rollback/extend) with a threshold-based rule. If data is insufficient, ESCALATE to wait for more traffic.

**Stop rule expectation:** ESCALATE (conservative: insufficient data after 3 rounds of debate)

**Key signals:** blocker detection (insufficient data is a blocker), novelty (same arguments reappear), open questions persist (need more canary data).

---

### Scenario S2 — Hotfix vs scheduled release

**Intent:** A severity-2 bug is found Friday afternoon. Agents weigh hotfix risk (no full test suite) vs waiting for Monday's release train.

**Good convergence:** Decision with explicit risk acceptance. If hotfix: rollback plan documented. If wait: mitigation steps for weekend.

**Stop rule expectation:** SHIP

**Key signals:** novelty (risk factors enumerated by round 2-3), action readiness (rollback plan or mitigation steps present), open questions at zero.

---

### Scenario S3 — Dependency upgrade with CVE

**Intent:** A critical CVE is published for a transitive dependency. Agents evaluate upgrade path, breaking changes, and workaround options.

**Good convergence:** Upgrade path chosen with a test plan. Breaking changes cataloged. If upgrade is blocked by a downstream dependency, ESCALATE.

**Stop rule expectation:** SHIP (if path is clear) or ESCALATE (if blocked)

**Key signals:** blocker detection (blocked dependency = ESCALATE), novelty (workaround options exhaust), action readiness.

---

## Category 5: Ship vs Polish Decisions

### Scenario P1 — Feature completeness threshold

**Intent:** A feature has 8/10 acceptance criteria met. Agents debate shipping now vs completing the last 2 criteria. Rounds explore user impact, deadline pressure, and technical debt.

**Good convergence:** Decision to ship-with-follow-up or delay, with explicit criteria for the follow-up timeline. No new arguments after round 3.

**Stop rule expectation:** SHIP

**Key signals:** novelty (arguments exhaust), structural agreement (both agents align on ship/delay), action readiness (follow-up ticket drafted or ship command ready).

---

### Scenario P2 — Test coverage vs ship date

**Intent:** Coverage is at 72%. Target is 80%. Shipping deadline is tomorrow. Agents weigh coverage gap risk vs deadline miss cost.

**Good convergence:** Decision with a concrete plan (ship at 72% with risk note, or write 3 critical-path tests tonight). Paraphrasing begins by round 3.

**Stop rule expectation:** SHIP

**Key signals:** novelty decay (risk factors fully enumerated), action readiness (plan is executable), open questions at zero.

---

### Scenario P3 — Refactor now vs ship and refactor later

**Intent:** Code works but has known technical debt. Agents debate refactoring before merge vs shipping and creating a tech debt ticket.

**Good convergence:** Decision with documented rationale. If ship: tech debt ticket drafted with scope. If refactor: time estimate and test plan.

**Stop rule expectation:** SHIP

**Key signals:** novelty (tradeoffs fully explored by round 3), action readiness (ticket or refactor plan exists), structural agreement.

---

### Scenario P4 — Error message polish

**Intent:** Error messages work but are terse. Agents debate improving UX vs shipping. Low stakes but high paraphrase risk — agents can loop on style preferences indefinitely.

**Good convergence:** Decision to ship with current messages or a bounded list of rewrites (max 5). Loop detection should fire early since style debates produce high repetition.

**Stop rule expectation:** STOP

**Key signals:** novelty (style preferences cycle, not progress), structural agreement (rephrase, not modify), open questions irrelevant (subjective).

---

## Scenario index

| ID | Category              | Scenario                         | Expected signal | Rounds to converge |
|----|-----------------------|----------------------------------|-----------------|--------------------|
| E1 | Engineering           | Database migration strategy      | SHIP            | 3-4                |
| E2 | Engineering           | API versioning approach          | SHIP            | 3-4                |
| E3 | Engineering           | Monorepo vs polyrepo             | SHIP            | 4-5                |
| E4 | Engineering           | Flaky test triage                | SHIP            | 3-4                |
| D1 | Doc truth-audit       | Stale README audit               | SHIP            | 3-4                |
| D2 | Doc truth-audit       | API docs vs implementation drift | SHIP            | 3-4                |
| D3 | Doc truth-audit       | Changelog completeness check     | SHIP            | 3-4                |
| I1 | Inbox/archive         | Triage a support queue           | SHIP            | 3-4                |
| I2 | Inbox/archive         | Email archive vs keep            | STOP            | 3-4                |
| I3 | Inbox/archive         | Notification consolidation       | SHIP            | 3-4                |
| S1 | Deployment safety     | Canary rollout go/no-go          | ESCALATE        | 3-4                |
| S2 | Deployment safety     | Hotfix vs scheduled release      | SHIP            | 3-4                |
| S3 | Deployment safety     | Dependency upgrade with CVE      | SHIP/ESCALATE   | 3-4                |
| P1 | Ship vs polish        | Feature completeness threshold   | SHIP            | 3-4                |
| P2 | Ship vs polish        | Test coverage vs ship date       | SHIP            | 3-4                |
| P3 | Ship vs polish        | Refactor now vs later            | SHIP            | 3-4                |
| P4 | Ship vs polish        | Error message polish             | STOP            | 2-3                |

---

## Design notes

- **Conservative defaults:** when a scenario could plausibly be SHIP or ESCALATE, we default to ESCALATE. Better to over-ask than to over-ship.
- **No personal data:** all scenarios use generic, clean-room contexts.
- **Fixture coverage:** the `examples/livefire/` directory contains transcript fixtures for a representative subset of these scenarios. Not every scenario has a fixture — the full set is intended for Ollama live-fire runs where transcripts are generated dynamically.
- **Signals are derived, not embedded:** per project convention, stop signals and scores are computed by `dr score`, not stored in the transcript. The `_expected` objects in fixtures document what the scorer *should* produce.
