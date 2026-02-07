from __future__ import annotations

from typing import Any, Dict


def score_transcript(transcript: Dict[str, Any]) -> Dict[str, Any]:
    """Score a conversation transcript.

    v0.0.0 placeholder implementation: always returns a stub.

    Transcript shape (expected future):
      {"conversation_id": str, "turns": [{"speaker": str, "text": str, ...}, ...]}
    """

    return {
        "score": 0.0,
        "components": {
            "semantic_similarity": None,
            "novelty_rate": None,
            "structural_agreement": None,
            "action_readiness": None,
        },
        "hint": "Not implemented yet (stub).",
    }
