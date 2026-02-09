from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from dr.io import load_transcript
from dr.score import score_transcript


class ScoreTranscriptTests(unittest.TestCase):
    def test_rejects_empty_rounds(self) -> None:
        with self.assertRaises(ValueError):
            score_transcript({"version": "0.1", "conversation_id": "x", "rounds": []})

    def test_dedupes_duplicate_claims_within_round(self) -> None:
        result = score_transcript(
            {
                "version": "0.1",
                "conversation_id": "dup",
                "rounds": [
                    {"round": 1, "outputs": {"claims": ["A", "A", "  a  "], "next_actions": ["Do thing"]}},
                    {"round": 2, "outputs": {"claims": ["A"], "next_actions": ["Do thing"]}},
                ],
            }
        )
        self.assertEqual(result["novelty_by_round"][0]["claims"], 1)
        self.assertEqual(result["novelty_by_round"][0]["new_claims"], 1)

    def test_single_low_tail_round_does_not_auto_stop(self) -> None:
        result = score_transcript(
            {
                "version": "0.1",
                "conversation_id": "tail-game",
                "rounds": [
                    {"round": 1, "outputs": {"claims": ["A", "B", "C"], "next_actions": ["x"]}},
                    {"round": 2, "outputs": {"claims": ["D", "E", "F"], "next_actions": ["x"]}},
                    {"round": 3, "outputs": {"claims": ["A", "B", "C"], "next_actions": ["x"]}},
                ],
            }
        )
        self.assertFalse(result["stop_recommendation"]["recommended"])


class JsonlLoadTests(unittest.TestCase):
    def test_sorts_round_events_by_round_number(self) -> None:
        events = [
            {"type": "transcript_header", "version": "0.1", "conversation_id": "ordered"},
            {"type": "round", "round": 2, "outputs": {"claims": ["B"]}},
            {"type": "round", "round": 1, "outputs": {"claims": ["A"]}},
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "trace.jsonl"
            path.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
            transcript = load_transcript(path)

        self.assertEqual([r["round"] for r in transcript["rounds"]], [1, 2])

    def test_reports_jsonl_parse_errors_with_line_number(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "trace.jsonl"
            path.write_text('{"type":"round","round":1,"outputs":{"claims":["A"]}}\nnot-json\n', encoding="utf-8")
            with self.assertRaises(ValueError) as ctx:
                load_transcript(path)

        self.assertIn("trace.jsonl:2", str(ctx.exception))

    def test_sorts_json_rounds_by_round_number(self) -> None:
        transcript = {
            "version": "0.1",
            "conversation_id": "ordered-json",
            "rounds": [
                {"round": 3, "outputs": {"claims": ["C"]}},
                {"round": 1, "outputs": {"claims": ["A"]}},
                {"round": 2, "outputs": {"claims": ["B"]}},
            ],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "transcript.json"
            path.write_text(json.dumps(transcript), encoding="utf-8")
            loaded = load_transcript(path)

        self.assertEqual([r["round"] for r in loaded["rounds"]], [1, 2, 3])

    def test_reports_json_parse_errors_with_file_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.json"
            path.write_text('{"version":"0.1"\n', encoding="utf-8")
            with self.assertRaises(ValueError) as ctx:
                load_transcript(path)

        self.assertIn("bad.json:2", str(ctx.exception))


class CliScoreTests(unittest.TestCase):
    def test_cli_exits_non_zero_for_invalid_json_with_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.json"
            path.write_text('{"rounds":[}\n', encoding="utf-8")
            env = dict(os.environ)
            env["PYTHONPATH"] = "src"
            proc = subprocess.run(
                [sys.executable, "-c", "from dr.cli import main; main()", "score", str(path)],
                cwd=Path(__file__).resolve().parents[1],
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(proc.returncode, 2)
        self.assertIn("error:", proc.stderr)
        self.assertIn("bad.json:1", proc.stderr)


if __name__ == "__main__":
    unittest.main()
