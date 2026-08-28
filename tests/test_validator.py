from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_ref2va_prompt.py"

VALID_PROMPT = """subject_definitions:
<Subject 1> is the adult runner in <Picture 1>, preserving her face and blue jacket.

summary:
[reference generation] The target video shows <Subject 1> completing one controlled sprint.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - her facial identity and blue jacket remain intact.

detailed_description:
The target video is a 4-second realistic sports clip with restrained daylight and a stable neutral grade.
[Shot 1] <Subject 1> stands in a low starting stance. From 00:00.000-00:01.000, she shifts her weight forward while the locked eye-level camera holds a medium-wide composition. From 00:01.000-00:03.000, she accelerates through frame with one readable running action and natural arm drive. From 00:03.000-00:04.000, she slows into a balanced stop while the camera remains fixed and her jacket settles.

overall_soundscape:
Soft shoe impacts, controlled breathing, and light fabric movement remain synchronized to the sprint.

non_diegetic_music:
N/A
"""


class ValidatorTests(unittest.TestCase):
    def run_validator(self, prompt: str, *extra: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            prompt_path = Path(directory) / "prompt.txt"
            prompt_path.write_text(prompt, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(prompt_path), *extra],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

    def test_valid_prompt_passes(self) -> None:
        result = self.run_validator(
            VALID_PROMPT,
            "--duration",
            "4",
            "--picture-count",
            "1",
            "--video-count",
            "0",
            "--audio-count",
            "0",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)

    def test_provenance_only_picture_needs_no_retention_line(self) -> None:
        result = self.run_validator(VALID_PROMPT, "--duration", "4")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("RETENTION_COUNT", result.stdout)

    def test_provenance_only_picture_cannot_be_used_later(self) -> None:
        prompt = VALID_PROMPT.replace(
            "The target video shows <Subject 1>",
            "The target video shows <Subject 1> beginning from <Picture 1>",
        )
        result = self.run_validator(prompt, "--duration", "4")
        self.assertEqual(result.returncode, 1)
        self.assertIn("UNDEFINED_LABEL", result.stdout)

    def test_wrong_marker_family_fails(self) -> None:
        prompt = VALID_PROMPT.replace("fully_preserved", "fully_copy")
        result = self.run_validator(prompt, "--duration", "4")
        self.assertEqual(result.returncode, 1)
        self.assertIn("RETENTION_MARKER", result.stdout)

    def test_undefined_label_fails(self) -> None:
        prompt = VALID_PROMPT.replace(
            "The target video shows <Subject 1>",
            "The target video shows <Subject 1> beside <Subject 2>",
        )
        result = self.run_validator(prompt, "--duration", "4")
        self.assertEqual(result.returncode, 1)
        self.assertIn("UNDEFINED_LABEL", result.stdout)

    def test_shot_and_time_errors_fail(self) -> None:
        prompt = VALID_PROMPT.replace(
            "[Shot 1] <Subject 1>",
            "[Shot 1] At 00:00.000, <Subject 1>",
        ).replace("00:04.000", "00:05.000")
        result = self.run_validator(prompt, "--duration", "4")
        self.assertEqual(result.returncode, 1)
        self.assertIn("SHOT1_TIMESTAMP", result.stdout)
        self.assertIn("RANGE_BOUNDS", result.stdout)

    def test_api_role_and_asset_limits_fail(self) -> None:
        result = self.run_validator(
            VALID_PROMPT,
            "--duration",
            "4",
            "--picture-count",
            "10",
            "--video-count",
            "3",
            "--audio-count",
            "1",
            "--uses-first-frame",
            "--uses-reference-role",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("ASSET_LIMIT", result.stdout)
        self.assertIn("MIXED_ASSET_LIMIT", result.stdout)
        self.assertIn("API_ROLE_CONFLICT", result.stdout)

    def test_no_reference_asset_fails(self) -> None:
        prompt = VALID_PROMPT.replace(" in <Picture 1>", " from the user's description")
        result = self.run_validator(
            prompt,
            "--duration",
            "4",
            "--picture-count",
            "0",
            "--video-count",
            "0",
            "--audio-count",
            "0",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("NO_REFERENCE_ASSET", result.stdout)

    def test_unmapped_attachment_warns(self) -> None:
        result = self.run_validator(
            VALID_PROMPT,
            "--duration",
            "4",
            "--picture-count",
            "2",
            "--video-count",
            "0",
            "--audio-count",
            "0",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("UNMAPPED_ATTACHMENT", result.stdout)

    def test_missing_attachment_fails(self) -> None:
        result = self.run_validator(
            VALID_PROMPT,
            "--duration",
            "4",
            "--picture-count",
            "0",
            "--video-count",
            "0",
            "--audio-count",
            "0",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("MISSING_ATTACHMENT", result.stdout)


if __name__ == "__main__":
    unittest.main()
