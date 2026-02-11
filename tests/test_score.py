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


ROOT = Path(__file__).resolve().parents[1]
CALIBRATION_DIR = ROOT / "examples" / "calibration"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


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
        self.assertEqual(result["novelty_by_round"][0]["new_claims_L0"], 1)

    def test_single_low_round_reports_k_consecutive_depth(self) -> None:
        result = score_transcript(
            {
                "version": "0.1",
                "conversation_id": "tail-game",
                "rounds": [
                    {"round": 1, "outputs": {"claims": ["A", "B", "C"], "next_actions": ["write plan"]}},
                    {"round": 2, "outputs": {"claims": ["D", "E", "F"], "next_actions": ["write plan"]}},
                    {"round": 3, "outputs": {"claims": ["A", "B", "C"], "next_actions": ["write plan"]}},
                ],
            }
        )
        self.assertEqual(result["stop_recommendation"]["k_consecutive_low_novelty"], 1)

    def test_paraphrase_l1_catches_what_l0_misses(self) -> None:
        transcript = load_transcript(CALIBRATION_DIR / "paraphrase-rounds.json")
        result = score_transcript(transcript)

        self.assertEqual(result["stop_recommendation"]["signal"], "SHIP")
        self.assertEqual(result["stop_recommendation"]["novelty_classification"], "LOW")
        self.assertGreater(result["components"]["novelty_rate_L0"], 0.9)
        self.assertLess(result["components"]["novelty_rate_L1"], 0.15)


class GoldenJsonTests(unittest.TestCase):
    def test_golden_output_shape_and_values(self) -> None:
        transcript = json.loads((FIXTURES_DIR / "golden.simple.transcript.json").read_text(encoding="utf-8"))
        expected = json.loads((FIXTURES_DIR / "golden.simple.expected.json").read_text(encoding="utf-8"))

        result = score_transcript(transcript)
        self.assertEqual(result, expected)


class CalibrationExamplesTests(unittest.TestCase):
    def _run_calibration_case(self, name: str) -> dict:
        fixture_path = CALIBRATION_DIR / f"{name}.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        transcript = {k: v for k, v in fixture.items() if k != "_expected"}
        expected = fixture["_expected"]

        result = score_transcript(transcript)
        self.assertEqual(result["stop_recommendation"]["signal"], expected["stop_recommendation"])
        self.assertIn(result["stop_recommendation"]["novelty_classification"], {"LOW", "MEDIUM", "HIGH"})
        self.assertIn(result["stop_recommendation"]["readiness_classification"], {"LOW", "MEDIUM", "HIGH"})

        return result

    def test_low_novelty_high_readiness_ships(self) -> None:
        result = self._run_calibration_case("low-novelty-high-readiness")
        self.assertEqual(result["stop_recommendation"]["signal"], "SHIP")

    def test_blocker_override_prevents_ship(self) -> None:
        result = self._run_calibration_case("low-novelty-high-readiness-blocked")
        self.assertNotEqual(result["stop_recommendation"]["signal"], "SHIP")
        self.assertEqual(result["stop_recommendation"]["signal"], "ESCALATE")

    def test_low_novelty_low_readiness_escalates(self) -> None:
        result = self._run_calibration_case("low-novelty-low-readiness")
        self.assertEqual(result["stop_recommendation"]["signal"], "ESCALATE")

    def test_high_novelty_regimes_continue(self) -> None:
        self.assertEqual(self._run_calibration_case("high-novelty-low-readiness")["stop_recommendation"]["signal"], "CONTINUE")
        self.assertEqual(
            self._run_calibration_case("high-novelty-high-readiness")["stop_recommendation"]["signal"], "CONTINUE"
        )

    def test_all_calibration_examples_match_expected(self) -> None:
        for fixture in sorted(CALIBRATION_DIR.glob("*.json")):
            self._run_calibration_case(fixture.stem)


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
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(proc.returncode, 2)
        self.assertIn("error:", proc.stderr)
        self.assertIn("bad.json:1", proc.stderr)


class CliStopTests(unittest.TestCase):
    def test_cli_stop_prints_minimal_stop_ship_format(self) -> None:
        env = dict(os.environ)
        env["PYTHONPATH"] = "src"
        proc = subprocess.run(
            [sys.executable, "-c", "from dr.cli import main; main()", "stop", "examples/transcript.meeting-stop.json"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stderr, "")

        lines = proc.stdout.strip().splitlines()
        self.assertGreaterEqual(len(lines), 7)
        self.assertRegex(lines[0], r"^Signal: (CONTINUE|SHIP|ESCALATE)$")
        self.assertEqual(lines[1], "Why:")
        self.assertTrue(lines[2].startswith("- "))
        self.assertTrue(lines[3].startswith("- "))
        self.assertTrue(lines[4].startswith("- "))
        self.assertEqual(lines[5], "Next action:")
        self.assertTrue(lines[6].startswith("- "))


if __name__ == "__main__":
    unittest.main()
