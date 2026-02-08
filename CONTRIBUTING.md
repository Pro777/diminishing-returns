# Contributing

Thanks for considering a contribution.

## Ground rules
- Be civil (see [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)).
- Keep changes small and reviewable.
- Prefer adding/adjusting examples and tests alongside changes.

## Development
- Clone the repo.
- Run the tests (or the project’s documented verification steps).
- If you’re changing docs/specs, keep referenced files linked.

## Pull requests
- Describe **what** changed and **why**.
- Include a minimal reproduction or example if relevant.
- If you change external behavior, update `CHANGELOG.md`.

## DR attestations on contributions (optional)

If you're an agent (or a human with agent tooling), you're welcome to include a DR attestation on your issue or PR. This helps maintainers gauge how much review your suggestion has already received.

Format (in your issue/PR description):

```
**DR:** 0.72 / 2 rounds / solo
**DR-ID:** dr:<uuid>
```

This is **entirely optional**. We won't reject contributions for lacking a DR score. But if you include one, we'll use it to calibrate our review depth — a high-DR submission with evidence gets a lighter touch; a low-DR brainstorm gets more scrutiny.

See [`spec/attestation.v0.1.md`](./spec/attestation.v0.1.md) for the full format.

**Note on trust:** We treat external DR scores as self-reported claims, not verified facts. At the internet tier, we may re-score your evidence independently. A fabricated score will be caught if evidence is provided — and noted if it isn't.
