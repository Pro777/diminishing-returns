from __future__ import annotations

import re
import string
from typing import Any, Dict, Iterable

# Spec reference: docs/novelty-and-readiness-spec.md
# L1 paraphrase-ish matching threshold.
# In live-fire runs, 0.6 was too strict and let near-rephrases count as “novel”.
JACCARD_THRESHOLD = 0.5
LOW_NOVELTY_THRESHOLD = 0.15
HIGH_NOVELTY_THRESHOLD = 0.5
K_LOW_NOVELTY_REQUIRED = 2
K_LOW_NOVELTY_ESCALATE = 3

# Minimal L0 readiness heuristics from the spec.
IMPERATIVE_VERBS = {
    "run",
    "write",
    "create",
    "open",
    "deploy",
    "send",
    "test",
    "build",
    "merge",
    "ship",
    "implement",
    "add",
    "remove",
    "update",
    "fix",
    "configure",
}
VAGUE_PREFIXES = (
    "consider",
    "think about",
    "explore",
    "look into",
    "investigate",
)
VAGUE_MARKERS = (
    "maybe",
    "possibly",
    "might",
    "could potentially",
)
BLOCKER_KEYWORDS = (
    "blocked",
    "blocker",
    "waiting on",
    "depends on",
    "need access",
    "need permission",
    "can't proceed",
    "prerequisite",
    "missing",
)
OWNERSHIP_MARKERS = (
    "i will",
    "we will",
    "owner",
    "owned by",
    "assign to",
    "assigned to",
    "@",
)
JACCARD_STOPWORDS = {
    "a",
    "about",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "being",
    "by",
    "can",
    "column",
    "could",
    "creat",
    "did",
    "do",
    "does",
    "for",
    "from",
    "frequently",
    "he",
    "her",
    "his",
    "i",
    "in",
    "into",
    "is",
    "it",
    "its",
    "layer",
    "more",
    "most",
    "might",
    "of",
    "often",
    "on",
    "or",
    "performance",
    "recommend",
    "our",
    "she",
    "should",
    "significantly",
    "that",
    "the",
    "their",
    "them",
    "they",
    "this",
    "to",
    "up",
    "use",
    "very",
    "was",
    "we",
    "were",
    "will",
    "with",
    "would",
    "you",
    "your",
    "add",
    "hot",
    "improv",
    "faster",
}
JACCARD_TOKEN_CANONICAL_MAP = {
    "accessed": "access",
    "accessing": "access",
    "app": "application",
    "apps": "application",
    "cach": "cache",
    "caching": "cache",
    "cut": "reduce",
    "down": "reduce",
    "lookups": "lookup",
    "faster": "fast",
    "pooler": "pool",
    "pooling": "pool",
    "queri": "query",
    "queries": "query",
    "query": "query",
    "spe": "fast",
    "speed": "fast",
    "speeds": "fast",
    "used": "use",
    "us": "use",
}


def _round_float(value: float) -> float:
    return round(float(value), 4)


def _normalize_claim(claim: str) -> str:
    """L0 normalization from docs/novelty-and-readiness-spec.md section 2.1."""

    text = claim.strip().lower()
    # Strip common bullet prefixes and leading punctuation noise.
    text = re.sub(r"^[\s\-\*\u2022\d\)\(\.:;,_]+", "", text)
    text = re.sub(r"\s+", " ", text)
    # Spec explicitly calls out trailing punctuation trimming.
    text = re.sub(r"[.!?]+$", "", text).strip(string.whitespace + string.punctuation)
    return text


def _normalized_round_claims(raw_claims: Iterable[Any]) -> list[str]:
    """Normalize, dedupe per-round, and return deterministic ordering."""

    deduped: set[str] = set()
    for claim in raw_claims:
        if not isinstance(claim, str):
            continue
        normalized = _normalize_claim(claim)
        if normalized:
            deduped.add(normalized)
    return sorted(deduped)


def _canonicalize_jaccard_token(token: str) -> str:
    if len(token) > 4 and token.endswith("ing"):
        token = token[:-3]
    elif len(token) > 3 and token.endswith("ed"):
        token = token[:-2]
    elif len(token) > 3 and token.endswith("es"):
        token = token[:-2]
    elif len(token) > 3 and token.endswith("s"):
        token = token[:-1]
    token = JACCARD_TOKEN_CANONICAL_MAP.get(token, token)
    return token


def _token_set(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9_]+", text.lower())
    canonical_tokens: set[str] = set()
    for token in tokens:
        canonical = _canonicalize_jaccard_token(token)
        if canonical and canonical not in JACCARD_STOPWORDS:
            canonical_tokens.add(canonical)
    return canonical_tokens


def _jaccard_similarity(a: str, b: str) -> float:
    ta = _token_set(a)
    tb = _token_set(b)
    if not ta and not tb:
        return 1.0
    union = ta | tb
    if not union:
        return 0.0
    return len(ta & tb) / len(union)


def _is_specific_action(action: str) -> bool:
    lowered = action.strip().lower()
    if not lowered:
        return False

    if any(lowered.startswith(prefix) for prefix in VAGUE_PREFIXES):
        return False
    if any(marker in lowered for marker in VAGUE_MARKERS):
        return False

    words = lowered.split()
    has_verb = any(word.strip(string.punctuation) in IMPERATIVE_VERBS for word in words)
    has_concrete_artifact = bool(
        re.search(r"https?://|\b(pr|branch|file|url|command|tool)\b|\b\w+\.\w+\b|[/`$]", lowered)
    )
    if len(words) < 5 and not has_verb:
        return False

    return has_verb or has_concrete_artifact


def _next_actions_score(next_actions: Any) -> float:
    if not isinstance(next_actions, list):
        return 0.0

    actions = [a for a in next_actions if isinstance(a, str) and a.strip()]
    if not actions:
        return 0.0

    specific_actions = [a for a in actions if _is_specific_action(a)]
    if not specific_actions:
        return 0.3

    has_ownership_language = any(marker in a.lower() for a in actions for marker in OWNERSHIP_MARKERS)
    if len(specific_actions) >= 2 and has_ownership_language:
        return 1.0
    return 0.7


def _open_questions_score(current: Any, previous: Any | None) -> float:
    current_questions = [q for q in current if isinstance(q, str) and q.strip()] if isinstance(current, list) else []
    if not current_questions:
        return 1.0

    if previous is None:
        return 0.3

    previous_questions = [q for q in previous if isinstance(q, str) and q.strip()] if isinstance(previous, list) else []
    if len(current_questions) < len(previous_questions):
        return 0.7
    if len(current_questions) == len(previous_questions):
        return 0.4
    return 0.1


def _blocker_score(open_questions: Any, next_actions: Any) -> float:
    texts: list[str] = []
    if isinstance(open_questions, list):
        texts.extend(q for q in open_questions if isinstance(q, str))
    if isinstance(next_actions, list):
        texts.extend(a for a in next_actions if isinstance(a, str))
    haystack = "\n".join(texts).lower()
    return 0.0 if any(keyword in haystack for keyword in BLOCKER_KEYWORDS) else 1.0


def _readiness_classification(action_readiness: float) -> str:
    if action_readiness >= 0.7:
        return "HIGH"
    if action_readiness >= 0.4:
        return "MEDIUM"
    return "LOW"


def _classify_novelty_rate(rate: float) -> str:
    if rate > HIGH_NOVELTY_THRESHOLD:
        return "HIGH"
    if rate < LOW_NOVELTY_THRESHOLD:
        return "LOW"
    return "MEDIUM"


def _compute_readiness(outputs: dict[str, Any], previous_outputs: dict[str, Any] | None) -> dict[str, float | str]:
    next_score = _next_actions_score(outputs.get("next_actions"))
    oq_score = _open_questions_score(
        outputs.get("open_questions"),
        previous_outputs.get("open_questions") if previous_outputs else None,
    )
    blocker_score = _blocker_score(outputs.get("open_questions"), outputs.get("next_actions"))
    readiness = (0.5 * next_score) + (0.3 * oq_score) + (0.2 * blocker_score)
    return {
        "next_actions_score": next_score,
        "open_questions_score": oq_score,
        "blocker_score": blocker_score,
        "action_readiness": readiness,
        "readiness_classification": _readiness_classification(readiness),
    }


def score_transcript(transcript: Dict[str, Any]) -> Dict[str, Any]:
    rounds = transcript.get("rounds")
    if not isinstance(rounds, list) or not rounds:
        raise ValueError("Transcript must contain a non-empty 'rounds' array.")

    seen_claims_l0: set[str] = set()
    seen_claims_l1: set[str] = set()
    novelty_by_round: list[dict[str, Any]] = []
    readiness_by_round: list[dict[str, Any]] = []
    per_round_novelty_rates: list[float] = []

    peak_new_l0 = 0
    peak_new_l1 = 0

    previous_outputs: dict[str, Any] | None = None
    last_outputs: dict[str, Any] = {}
    latest_readiness: dict[str, float | str] = {
        "next_actions_score": 0.0,
        "open_questions_score": 0.0,
        "blocker_score": 1.0,
        "action_readiness": 0.0,
        "readiness_classification": "LOW",
    }

    for r in rounds:
        if not isinstance(r, dict):
            raise ValueError("Each transcript round must be an object.")

        round_number = r.get("round")
        outputs = r.get("outputs") or {}
        if not isinstance(outputs, dict):
            raise ValueError("Each transcript round must contain an object at 'outputs'.")

        raw_claims = outputs.get("claims")
        if not isinstance(raw_claims, list):
            raise ValueError("Each transcript round must contain an array at 'outputs.claims'.")

        claims = _normalized_round_claims(raw_claims)

        new_l0_claims = [claim for claim in claims if claim not in seen_claims_l0]

        new_l1_claims: list[str] = []
        for claim in claims:
            if not seen_claims_l1:
                new_l1_claims.append(claim)
                continue
            max_similarity = max(_jaccard_similarity(claim, seen) for seen in seen_claims_l1)
            if max_similarity < JACCARD_THRESHOLD:
                new_l1_claims.append(claim)

        seen_claims_l0.update(claims)
        seen_claims_l1.update(claims)

        peak_new_l0 = max(peak_new_l0, len(new_l0_claims))
        peak_new_l1 = max(peak_new_l1, len(new_l1_claims))

        novelty_rate_l0 = len(new_l0_claims) / max(peak_new_l0, 1)
        novelty_rate_l1 = len(new_l1_claims) / max(peak_new_l1, 1)
        novelty_rate_round = min(novelty_rate_l0, novelty_rate_l1)
        per_round_novelty_rates.append(novelty_rate_round)

        readiness = _compute_readiness(outputs, previous_outputs)
        readiness_by_round.append(
            {
                "round": round_number,
                "action_readiness": _round_float(readiness["action_readiness"]),
                "readiness_classification": readiness["readiness_classification"],
                "next_actions_score": _round_float(readiness["next_actions_score"]),
                "open_questions_score": _round_float(readiness["open_questions_score"]),
                "blocker_score": _round_float(readiness["blocker_score"]),
            }
        )

        novelty_by_round.append(
            {
                "round": round_number,
                "claims": len(claims),
                "new_claims": min(len(new_l0_claims), len(new_l1_claims)),
                "new_claims_L0": len(new_l0_claims),
                "new_claims_L1": len(new_l1_claims),
                "novelty_rate": _round_float(novelty_rate_round),
                "novelty_rate_L0": _round_float(novelty_rate_l0),
                "novelty_rate_L1": _round_float(novelty_rate_l1),
            }
        )

        previous_outputs = outputs
        last_outputs = outputs
        latest_readiness = readiness

    novelty_rate_l0 = novelty_by_round[-1]["novelty_rate_L0"]
    novelty_rate_l1 = novelty_by_round[-1]["novelty_rate_L1"]
    novelty_rate = _round_float(min(novelty_rate_l0, novelty_rate_l1))

    trailing_low = 0
    for rate in reversed(per_round_novelty_rates):
        if rate < LOW_NOVELTY_THRESHOLD:
            trailing_low += 1
        else:
            break

    raw_novelty_class = _classify_novelty_rate(novelty_rate)
    novelty_classification = raw_novelty_class

    readiness_classification = str(latest_readiness["readiness_classification"])

    # Decision matrix from docs/novelty-and-readiness-spec.md section 4.
    blocker_present = float(latest_readiness["blocker_score"]) == 0.0
    if novelty_classification in {"HIGH", "MEDIUM"}:
        signal = "CONTINUE"
    elif readiness_classification == "LOW":
        signal = "ESCALATE"
    elif blocker_present:
        signal = "ESCALATE"
    else:
        signal = "SHIP"

    if trailing_low >= K_LOW_NOVELTY_ESCALATE:
        low_window = readiness_by_round[-trailing_low:]
        had_high_readiness = any(entry["readiness_classification"] == "HIGH" for entry in low_window)
        if not had_high_readiness:
            signal = "ESCALATE"

    # Spec intent: blockers are decisive and must prevent SHIP.
    if blocker_present and signal == "SHIP":
        signal = "ESCALATE"

    if signal == "SHIP":
        hint = "Converged. Ship the decision and verify."
    elif signal == "ESCALATE":
        hint = "Converged but blocked or not actionable. Escalate: change scope/owner or unblock dependencies."
    else:
        hint = "Still producing useful novelty. Continue the loop."

    rationale_parts: list[str] = [
        f"Novelty is {novelty_classification} (k-consecutive low rounds: {trailing_low}).",
        f"Action readiness is {readiness_classification}.",
    ]
    if blocker_present:
        rationale_parts.append("Blocker keywords detected in latest open questions/next actions.")
        if signal == "ESCALATE":
            rationale_parts.append("Blocker override applied: cannot SHIP while blocked.")

    return {
        "score": _round_float(1.0 - novelty_rate),
        "components": {
            "semantic_similarity": None,
            "novelty_rate": novelty_rate,
            "novelty_rate_L0": _round_float(float(novelty_rate_l0)),
            "novelty_rate_L1": _round_float(float(novelty_rate_l1)),
            "structural_agreement": None,
            "action_readiness": _round_float(float(latest_readiness["action_readiness"])),
            "action_readiness_detail": {
                "next_actions_score": _round_float(float(latest_readiness["next_actions_score"])),
                "open_questions_score": _round_float(float(latest_readiness["open_questions_score"])),
                "blocker_score": _round_float(float(latest_readiness["blocker_score"])),
            },
        },
        "novelty_by_round": novelty_by_round,
        "readiness_by_round": readiness_by_round,
        "stop_recommendation": {
            "signal": signal,
            "novelty_classification": novelty_classification,
            "readiness_classification": readiness_classification,
            "k_consecutive_low_novelty": trailing_low,
            "rationale": " ".join(rationale_parts),
        },
        "hint": hint,
    }
