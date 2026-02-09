import argparse
import json
import sys

from .io import load_transcript
from .score import score_transcript


def main() -> None:
    p = argparse.ArgumentParser(prog="dr", description="Diminishing returns meter (stop/ship signal, not confidence).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="Score a transcript JSON file")
    s.add_argument("path", help="Path to transcript JSON")

    args = p.parse_args()

    if args.cmd == "score":
        try:
            data = load_transcript(args.path)
        except (FileNotFoundError, ValueError) as exc:
            print(f"error: {args.path}: {exc}", file=sys.stderr)
            raise SystemExit(2)

        try:
            result = score_transcript(data)
            print(json.dumps(result, indent=2, sort_keys=True))
            return
        except ValueError as exc:
            print(f"error: {args.path}: {exc}", file=sys.stderr)
            raise SystemExit(2)

    raise SystemExit(2)
