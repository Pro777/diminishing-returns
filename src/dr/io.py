from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def _sort_rounds(rounds: List[Dict[str, Any]]) -> None:
    rounds.sort(key=lambda r: (0, r["round"]) if isinstance(r.get("round"), int) else (1, 0))


def load_transcript(path: str | Path) -> Dict[str, Any]:
    """Load either a transcript JSON object or a JSONL trace into the canonical transcript dict.

    - `.json` is expected to already be in transcript v0.1 shape.
    - `.jsonl` is expected to be an event stream with at least:
        {"type":"transcript_header", ...}
        {"type":"round", "round": N, "outputs": {...}}
      Optionally:
        {"type":"diminishing_returns_note", ...}

    We keep this permissive: the scorer only needs `rounds[*].outputs.claims`.
    """

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Transcript not found: {p}")

    if p.suffix.lower() == ".jsonl":
        events: List[Dict[str, Any]] = []
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {p}:{i}: {exc.msg}") from exc
            if not isinstance(parsed, dict):
                raise ValueError(f"Invalid JSONL event at {p}:{i}: expected an object.")
            events.append(parsed)

        header = next((e for e in events if e.get("type") == "transcript_header"), {})
        rounds = [
            {"round": e.get("round"), "outputs": e.get("outputs") or {}}
            for e in events
            if e.get("type") == "round"
        ]
        _sort_rounds(rounds)

        note = next((e for e in events if e.get("type") == "diminishing_returns_note"), None)
        out: Dict[str, Any] = {
            "version": header.get("version") or "0.1",
            "conversation_id": header.get("conversation_id"),
            "topic": header.get("topic"),
            "rounds": rounds,
        }
        if note:
            out["diminishing_returns_note"] = {k: v for k, v in note.items() if k != "type"}
        return out

    # default: JSON transcript
    text = p.read_text(encoding="utf-8")
    try:
        transcript = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON at {p}:{exc.lineno}: {exc.msg}") from exc
    if not isinstance(transcript, dict):
        raise ValueError(f"Invalid JSON transcript at {p}: expected a top-level object.")

    rounds = transcript.get("rounds")
    if isinstance(rounds, list):
        sortable_rounds = [r for r in rounds if isinstance(r, dict)]
        if len(sortable_rounds) == len(rounds):
            _sort_rounds(sortable_rounds)
            transcript["rounds"] = sortable_rounds

    return transcript
