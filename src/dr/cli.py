import argparse
import json
import re
import sys

from .io import load_transcript
from .score import score_transcript


def _score_path(path: str) -> dict:
    data = load_transcript(path)
    return score_transcript(data)


def _why_bullets(result: dict) -> list[str]:
    stop = result.get("stop_recommendation") if isinstance(result, dict) else {}
    stop = stop if isinstance(stop, dict) else {}

    rationale = stop.get("rationale", "")
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\\s+", str(rationale)) if s.strip()]

    novelty_class = str(stop.get("novelty_classification", "UNKNOWN"))
    readiness_class = str(stop.get("readiness_classification", "UNKNOWN"))

    bullets: list[str] = []
    if sentences:
        bullets.append(sentences[0])
    if len(sentences) > 1:
        bullets.append(sentences[1])

    bullets.append(f"Classifications: novelty={novelty_class}, readiness={readiness_class}.")

    while len(bullets) < 3:
        bullets.append("See score details for full component context.")

    return bullets[:3]


def _next_action(signal: str) -> str:
    if signal == "SHIP":
        return "Ship the decision and run verification (tests, repro, or evidence checks)."
    if signal == "ESCALATE":
        return "Escalate to the responsible owner to unblock dependencies or adjust scope."
    return "Run one focused round to resolve the highest-impact open question."


def _print_stop_output(result: dict) -> None:
    stop = result.get("stop_recommendation") if isinstance(result, dict) else {}
    stop = stop if isinstance(stop, dict) else {}

    signal = str(stop.get("signal", "CONTINUE"))
    print(f"Signal: {signal}")
    print("Why:")
    for bullet in _why_bullets(result):
        print(f"- {bullet}")
    print("Next action:")
    print(f"- {_next_action(signal)}")


def main() -> None:
    p = argparse.ArgumentParser(prog="dr", description="Diminishing returns meter (stop/ship signal, not confidence).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="Score a transcript JSON file")
    s.add_argument("path", help="Path to transcript JSON")

    stop = sub.add_parser("stop", help="Print a minimal stop/ship verdict")
    stop.add_argument("path", help="Path to transcript JSON")

    args = p.parse_args()

    if args.cmd == "score":
        try:
            result = _score_path(args.path)
            print(json.dumps(result, indent=2, sort_keys=True))
            return
        except (FileNotFoundError, ValueError) as exc:
            print(f"error: {args.path}: {exc}", file=sys.stderr)
            raise SystemExit(2)

    if args.cmd == "stop":
        try:
            result = _score_path(args.path)
            _print_stop_output(result)
            return
        except (FileNotFoundError, ValueError) as exc:
            print(f"error: {args.path}: {exc}", file=sys.stderr)
            raise SystemExit(2)

    raise SystemExit(2)


if __name__ == "__main__":
    main()
