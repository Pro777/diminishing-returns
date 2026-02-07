from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


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
    if p.suffix.lower() == ".jsonl":
        events: List[Dict[str, Any]] = []
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))

        header = next((e for e in events if e.get("type") == "transcript_header"), {})
        rounds = [
            {"round": e.get("round"), "outputs": e.get("outputs") or {}}
            for e in events
            if e.get("type") == "round"
        ]

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
    return json.loads(p.read_text(encoding="utf-8"))
