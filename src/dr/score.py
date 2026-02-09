from __future__ import annotations

import re
from typing import Any, Dict


def _normalize_claim(claim: str) -> str:
    # Keep novelty matching robust to superficial formatting differences.
    return re.sub(r"\s+", " ", claim.strip().lower())


def _round_float(value: float) -> float:
    return round(float(value), 4)


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

    rounds = transcript.get("rounds")
    if not isinstance(rounds, list) or not rounds:
        raise ValueError("Transcript must contain a non-empty 'rounds' array.")

    seen_claims: set[str] = set()
    novelty_by_round: list[dict[str, Any]] = []
    last_outputs: dict[str, Any] = {}

    for r in rounds:
        if not isinstance(r, dict):
            raise ValueError("Each transcript round must be an object.")

        n = r.get("round")
        outputs = r.get("outputs") or {}
        if not isinstance(outputs, dict):
            raise ValueError("Each transcript round must contain an object at 'outputs'.")

        raw_claims = outputs.get("claims")
        if not isinstance(raw_claims, list):
            raise ValueError("Each transcript round must contain an array at 'outputs.claims'.")

        claims: list[str] = []
        round_seen: set[str] = set()
        for claim in raw_claims:
            if not isinstance(claim, str):
                continue
            normalized = _normalize_claim(claim)
            if not normalized or normalized in round_seen:
                continue
            round_seen.add(normalized)
            claims.append(normalized)

        new = [c for c in claims if c not in seen_claims]
        seen_claims.update(claims)
        novelty_by_round.append({"round": n, "claims": len(claims), "new_claims": len(new)})
        last_outputs = outputs

    peak_new = max([x["new_claims"] for x in novelty_by_round], default=0)
    tail_window = 2
    tail_slice = novelty_by_round[-tail_window:]
    tail_new_avg = (sum(x["new_claims"] for x in tail_slice) / len(tail_slice)) if tail_slice else 0.0
    novelty_rate = (tail_new_avg / peak_new) if peak_new else 0.0

    score = 1.0 - float(novelty_rate)
    novelty_low_threshold = 0.2
    low_novelty_rounds = [
        ((x["new_claims"] / peak_new) if peak_new else 0.0) <= novelty_low_threshold for x in novelty_by_round
    ]

    consecutive_low = 0
    max_consecutive_low = 0
    for is_low in low_novelty_rounds:
        if is_low:
            consecutive_low += 1
            max_consecutive_low = max(max_consecutive_low, consecutive_low)
        else:
            consecutive_low = 0

    k_required = 2
    open_questions = last_outputs.get("open_questions") or []
    next_actions = last_outputs.get("next_actions") or []
    blocked_by_questions = isinstance(open_questions, list) and any(
        isinstance(q, str) and q.strip() for q in open_questions
    )
    has_next_action = isinstance(next_actions, list) and any(isinstance(a, str) and a.strip() for a in next_actions)
    action_readiness = 1.0 if (not blocked_by_questions and has_next_action) else 0.0
    evidence_low = (sum(x["claims"] for x in tail_slice) / len(tail_slice)) < 2.0 if tail_slice else True
    blockers: list[str] = []
    warnings: list[str] = []
    if blocked_by_questions:
        blockers.append("open_questions_in_latest_round")
    if evidence_low:
        warnings.append("low_claim_volume_recent_rounds")

    recommended_stop = (max_consecutive_low >= k_required) and not blockers

    if recommended_stop:
        hint = "Diminishing returns detected for consecutive rounds; move to implementation and verification."
    elif blocked_by_questions:
        hint = "Novelty is tapering, but unresolved questions remain; run one focused clarification round."
    else:
        hint = "Still generating novel ideas; continue another round."

    return {
        "score": _round_float(score),
        "components": {
            "semantic_similarity": None,
            "novelty_rate": _round_float(novelty_rate),
            "structural_agreement": None,
            "action_readiness": _round_float(action_readiness),
        },
        "novelty_by_round": novelty_by_round,
        "stop_recommendation": {
            "recommended": recommended_stop,
            "reason": "k_consecutive_low_novelty" if recommended_stop else "continue_or_clarify",
            "k_required": k_required,
            "max_consecutive_low_novelty_rounds": max_consecutive_low,
            "blockers": blockers,
            "warnings": warnings,
            "confidence": _round_float(
                max(
                    0.0,
                    min(
                        1.0,
                        (max_consecutive_low / max(k_required, 1))
                        * (0.5 + 0.5 * (1.0 - novelty_rate))
                        * (1.0 if not blockers else 0.5)
                        * (0.75 if evidence_low else 1.0),
                    ),
                )
            ),
        },
        "hint": hint,
    }
