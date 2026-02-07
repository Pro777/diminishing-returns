from __future__ import annotations

from typing import Any, Dict


def score_transcript(transcript: Dict[str, Any]) -> Dict[str, Any]:
    """Score a conversation transcript.

    v0.0.1-ish implementation: computes a crude novelty curve from structured round outputs.

    Expected shape (see spec/transcript.v0.1.schema.json):
      {
        "version": "0.1",
        "conversation_id": str,
        "rounds": [
          {"round": 1, "outputs": {"claims": [...], "decisions": [...], "open_questions": [...], "next_actions": [...]}},
          ...
        ]
      }

    This is intentionally conservative: we do NOT claim correctness.
    """

    rounds = transcript.get("rounds") or []
    seen_claims: set[str] = set()
    novelty_by_round: list[dict[str, Any]] = []

    for r in rounds:
        n = r.get("round")
        outputs = r.get("outputs") or {}
        claims = [c.strip() for c in (outputs.get("claims") or []) if isinstance(c, str) and c.strip()]
        new = [c for c in claims if c not in seen_claims]
        for c in claims:
            seen_claims.add(c)
        novelty_by_round.append({"round": n, "claims": len(claims), "new_claims": len(new)})

    # Simple diminishing-returns proxy: last-round new_claims normalized by peak.
    peak_new = max([x["new_claims"] for x in novelty_by_round], default=0)
    last_new = novelty_by_round[-1]["new_claims"] if novelty_by_round else 0
    novelty_rate = (last_new / peak_new) if peak_new else 0.0

    # Placeholder overall score: 1 - novelty_rate (higher score => more diminished returns)
    score = 1.0 - float(novelty_rate)

    hint = "Mostly converged; move to implementation and verification." if score >= 0.85 else "Still generating novel ideas; continue another round."

    return {
        "score": round(score, 4),
        "components": {
            "semantic_similarity": None,
            "novelty_rate": round(float(novelty_rate), 4),
            "structural_agreement": None,
            "action_readiness": None,
        },
        "novelty_by_round": novelty_by_round,
        "hint": hint,
    }
