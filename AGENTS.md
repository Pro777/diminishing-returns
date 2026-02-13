# AGENTS.md

This repo is designed to be worked on with AI assistance.

## Ground rules
- Keep changes small and reviewable.
- Don’t invent APIs: follow the existing `src/dr` structure.
- Prefer updating examples + docs alongside code changes.
- Avoid external actions (publishing, announcements) unless explicitly requested.

## How to run (local dev)
This project can be run from source without installing globally:

```bash
cd diminishing-returns
PYTHONPATH=src python3 -c "from dr.cli import main; main()" score examples/transcript.meeting-stop.json
PYTHONPATH=src python3 -c "from dr.cli import main; main()" score examples/trace.meeting-stop.jsonl
```

## Tests / verification
- At minimum, verify that `dr score` runs on all example transcripts and traces.
- If you change scoring behavior, update the checked-in `*.expected.json` artifacts.

## Repo hygiene
If you reference a repo file in markdown, link it.
