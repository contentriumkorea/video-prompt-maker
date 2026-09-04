import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "skills" / "video-prompt-maker"
    / "scripts"
    / "validate_prompt.py"
)
DIRECTIVE = "[Sound] no music"
MODEL_LIMITS = {
    "Seedance 2.0": 3800,
    "Seedance 2.5": 14000,
    "MiniMax H3": 6500,
    "Kling 3.0": 8000,
}


def load_validator():
    spec = importlib.util.spec_from_file_location("video_prompt_validator", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load validator from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidatePromptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_accepts_valid_non_musical_prompt(self):
        result = self.validator.validate_prompt(
            "A courier opens a wet cardboard box. "
            "[Sound] no music, rain, distant traffic."
        )
        self.assertTrue(result.ok, result.violations)

    def test_accepts_exact_3800_ascii_characters(self):
        prompt = DIRECTIVE + ("x" * (3800 - len(DIRECTIVE)))
        result = self.validator.validate_prompt(prompt)
        self.assertTrue(result.ok, result.violations)
        self.assertEqual(result.unicode_chars, 3800)
        self.assertEqual(result.utf16_units, 3800)

    def test_applies_each_models_exact_boundary_and_rejects_one_over(self):
        for model, limit in MODEL_LIMITS.items():
            with self.subTest(model=model, boundary="exact"):
                prompt = DIRECTIVE + ("x" * (limit - len(DIRECTIVE)))
                result = self.validator.validate_prompt(prompt, model=model)
                self.assertTrue(result.ok, result.violations)
                self.assertEqual(result.model, model)
                self.assertEqual(result.max_chars, limit)
                self.assertEqual(result.unicode_chars, limit)
                self.assertEqual(result.utf16_units, limit)

            with self.subTest(model=model, boundary="one-over"):
                prompt = DIRECTIVE + ("x" * (limit + 1 - len(DIRECTIVE)))
                result = self.validator.validate_prompt(prompt, model=model)
                self.assertFalse(result.ok)
                self.assertEqual(result.model, model)
                self.assertEqual(result.max_chars, limit)
                self.assertIn("unicode-length", result.violations)
                self.assertIn("utf16-length", result.violations)

    def test_resolves_supported_model_aliases(self):
        aliases = {
            "seedance-2.0": ("Seedance 2.0", 3800),
            "시댄스 2.0": ("Seedance 2.0", 3800),
            "SEEDANCE_2_5": ("Seedance 2.5", 14000),
            "시댄스-2.5": ("Seedance 2.5", 14000),
            "minimax-h3": ("MiniMax H3", 6500),
            "미니맥스 H3": ("MiniMax H3", 6500),
            "KLING 3": ("Kling 3.0", 8000),
            "클링-3.0": ("Kling 3.0", 8000),
        }
        for alias, expected in aliases.items():
            with self.subTest(alias=alias):
                policy = self.validator.resolve_model_policy(alias)
                self.assertEqual((policy.model, policy.max_chars), expected)

    def test_does_not_partially_match_unsupported_versions(self):
        for model in ("Seedance 2.50", "Kling 3.1", "MiniMax H30"):
            with self.subTest(model=model):
                policy = self.validator.resolve_model_policy(model)
                self.assertEqual(policy.model, "Seedance 2.0")
                self.assertEqual(policy.max_chars, 3800)

    def test_omitted_or_unknown_model_uses_seedance_20_default(self):
        prompt = DIRECTIVE + ("x" * (3801 - len(DIRECTIVE)))
        for model in (None, "", "Veo 4", "Runway Gen-5"):
            with self.subTest(model=model):
                result = self.validator.validate_prompt(prompt, model=model)
                self.assertFalse(result.ok)
                self.assertEqual(result.model, "Seedance 2.0")
                self.assertEqual(result.max_chars, 3800)
                self.assertIn("unicode-length", result.violations)

    def test_shared_prompt_uses_smallest_named_model_limit(self):
        prompt = DIRECTIVE + ("x" * (8001 - len(DIRECTIVE)))
        result = self.validator.validate_prompt(
            prompt,
            model="Seedance 2.5, Kling 3.0",
        )
        self.assertFalse(result.ok)
        self.assertEqual(result.model, "Kling 3.0")
        self.assertEqual(result.max_chars, 8000)
        self.assertIn("unicode-length", result.violations)

        reversed_policy = self.validator.resolve_model_policy(
            "Kling 3.0 / Seedance 2.5"
        )
        self.assertEqual(reversed_policy.model, "Kling 3.0")
        self.assertEqual(reversed_policy.max_chars, 8000)

        mixed_policy = self.validator.resolve_model_policy(
            "Seedance 2.5 / unsupported future model"
        )
        self.assertEqual(mixed_policy.model, "Seedance 2.0")
        self.assertEqual(mixed_policy.max_chars, 3800)

    def test_rejects_3801_ascii_characters(self):
        prompt = DIRECTIVE + ("x" * (3801 - len(DIRECTIVE)))
        result = self.validator.validate_prompt(prompt)
        self.assertFalse(result.ok)
        self.assertIn("unicode-length", result.violations)
        self.assertIn("utf16-length", result.violations)

    def test_rejects_utf16_overflow_from_emoji(self):
        prompt = DIRECTIVE + "😀" + ("x" * (3800 - len(DIRECTIVE) - 1))
        result = self.validator.validate_prompt(prompt)
        self.assertEqual(result.unicode_chars, 3800)
        self.assertEqual(result.utf16_units, 3801)
        self.assertFalse(result.ok)
        self.assertIn("utf16-length", result.violations)

    def test_applies_selected_models_limit_to_utf16_units(self):
        for model, limit in MODEL_LIMITS.items():
            with self.subTest(model=model):
                prompt = DIRECTIVE + "😀" + ("x" * (limit - len(DIRECTIVE) - 1))
                result = self.validator.validate_prompt(prompt, model=model)
                self.assertEqual(result.unicode_chars, limit)
                self.assertEqual(result.utf16_units, limit + 1)
                self.assertEqual(result.max_chars, limit)
                self.assertFalse(result.ok)
                self.assertIn("utf16-length", result.violations)

    def test_non_length_contract_is_unchanged_for_other_models(self):
        result = self.validator.validate_prompt(
            "A singer performs while background music swells.",
            model="Seedance 2.5",
        )
        self.assertFalse(result.ok)
        self.assertIn("sound-directive-count", result.violations)
        self.assertIn("music-language", result.violations)

    def test_requires_exact_directive_once(self):
        missing = self.validator.validate_prompt("A silent corridor.")
        lowercase = self.validator.validate_prompt("[sound] no music, wind.")
        repeated = self.validator.validate_prompt(f"{DIRECTIVE}\n{DIRECTIVE}")
        self.assertFalse(missing.ok)
        self.assertFalse(lowercase.ok)
        self.assertFalse(repeated.ok)
        self.assertIn("sound-directive-count", missing.violations)
        self.assertIn("sound-directive-count", lowercase.violations)
        self.assertIn("sound-directive-count", repeated.violations)

    def test_rejects_music_generation_terms(self):
        forbidden = (
            "BGM", "OST", "cinematic soundtrack", "a song begins",
            "she is singing", "he hums", "melodic whistling",
            "a rising melody", "orchestral accompaniment",
            "instrumental track", "instrumental score",
            "dramatic musical score", "beat-sync",
            "A band performs onstage while the audience moves to the tempo.",
            "배경음악 시작",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                result = self.validator.validate_prompt(f"{DIRECTIVE}. {phrase}.")
                self.assertFalse(result.ok)
                self.assertIn("music-language", result.violations)

    def test_does_not_false_positive_non_musical_words(self):
        allowed = (
            "The sports score reads two to one.",
            "A slow tracking shot follows her.",
            "His heartbeat becomes audible.",
            "On the next narrative beat, she turns.",
            "A pitch-black room surrounds them.",
            "A guide discusses the Song dynasty.",
            "Color harmony shapes the room.",
            "Rows of choir stalls line the cathedral."
        )
        for phrase in allowed:
            with self.subTest(phrase=phrase):
                result = self.validator.validate_prompt(f"{phrase} {DIRECTIVE}.")
                self.assertTrue(result.ok, result.violations)

    def test_rejects_code_fence_markers_and_empty_body(self):
        fenced = self.validator.validate_prompt(f"```text\n{DIRECTIVE}\n```")
        empty = self.validator.validate_prompt("")
        self.assertFalse(fenced.ok)
        self.assertFalse(empty.ok)
        self.assertIn("code-fence", fenced.violations)
        self.assertIn("empty", empty.violations)

    def test_counts_crlf_as_two_code_points(self):
        prompt = f"{DIRECTIVE}\r\nFootsteps."
        result = self.validator.validate_prompt(prompt)
        self.assertEqual(result.unicode_chars, len(prompt))
        self.assertEqual(result.utf16_units, len(prompt.encode("utf-16-le")) // 2)

    def test_cli_uses_distinct_exit_codes_for_validation_and_read_errors(self):
        invalid_prompt = subprocess.run(
            [sys.executable, str(MODULE_PATH)],
            input=b"A corridor with background music. [Sound] no music",
            capture_output=True,
            check=False,
        )
        self.assertEqual(invalid_prompt.returncode, 1, invalid_prompt.stderr)
        self.assertIn(b"violations=music-language", invalid_prompt.stdout)

        missing = MODULE_PATH.parent / "does-not-exist.txt"
        missing_file = subprocess.run(
            [sys.executable, str(MODULE_PATH), str(missing)],
            capture_output=True,
            check=False,
        )
        self.assertEqual(missing_file.returncode, 2, missing_file.stderr)
        self.assertEqual(missing_file.stdout, b"")
        self.assertIn(b"error: cannot read prompt:", missing_file.stderr)

        with tempfile.TemporaryDirectory() as directory:
            undecodable = Path(directory) / "invalid-utf8.txt"
            undecodable.write_bytes(b"\xff\xfe\xfa")
            decode_error = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(undecodable)],
                capture_output=True,
                check=False,
            )
        self.assertEqual(decode_error.returncode, 2, decode_error.stderr)
        self.assertEqual(decode_error.stdout, b"")
        self.assertIn(b"error: cannot read prompt:", decode_error.stderr)

    def test_cli_accepts_model_and_reports_resolved_policy(self):
        seedance_25_prompt = DIRECTIVE + ("x" * (3801 - len(DIRECTIVE)))
        accepted = subprocess.run(
            [sys.executable, str(MODULE_PATH), "--model", "Seedance 2.5"],
            input=seedance_25_prompt.encode("utf-8"),
            capture_output=True,
            check=False,
        )
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        self.assertTrue(
            accepted.stdout.startswith(
                b"ok=true unicode_chars=3801 utf16_units=3801 violations=none "
            ),
            accepted.stdout,
        )
        self.assertIn(b"model=seedance-2.5", accepted.stdout)
        self.assertIn(b"max_chars=14000", accepted.stdout)

        overflow = DIRECTIVE + ("x" * (14001 - len(DIRECTIVE)))
        rejected = subprocess.run(
            [sys.executable, str(MODULE_PATH), "--model", "Seedance 2.5"],
            input=overflow.encode("utf-8"),
            capture_output=True,
            check=False,
        )
        self.assertEqual(rejected.returncode, 1, rejected.stderr)
        self.assertIn(b"model=seedance-2.5", rejected.stdout)
        self.assertIn(b"max_chars=14000", rejected.stdout)
        self.assertIn(b"unicode-length", rejected.stdout)


if __name__ == "__main__":
    unittest.main()
