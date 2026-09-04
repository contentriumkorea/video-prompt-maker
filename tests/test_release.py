"""Exercise the actual release artifacts, including their runnable validator."""
import hashlib
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "video-prompt-maker"
BUILDER = ROOT / "tools" / "build_release.py"
STAMP = "2026-09-05 12'00"


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "release with spaces"

    def build(self):
        self.assertTrue(BUILDER.is_file(), "A reproducible release builder is missing")
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--output-dir", str(self.output),
             "--timestamp", STAMP], capture_output=True, text=True,
            cwd=self.temp.name,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.output / f"{STAMP} Video Prompt Maker.zip"

    def test_archive_contains_only_portable_skill_and_preserves_source_bytes(self):
        archive = self.build()
        expected = {
            "SKILL.md", "agents/openai.yaml", "scripts/validate_prompt.py",
            "references/prompt-architecture.md", "references/acting-performance.md",
            "references/visual-continuity.md", "references/spatial-physics.md",
            "references/quality-check.md",
        }
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(set(bundle.namelist()),
                             {f"video-prompt-maker/{name}" for name in expected})
            for name in expected:
                self.assertEqual(bundle.read(f"video-prompt-maker/{name}"),
                                 (SOURCE / name).read_bytes())

    def test_archive_description_fits_claude_web_upload(self):
        archive = self.build()
        with zipfile.ZipFile(archive) as bundle:
            skill = bundle.read("video-prompt-maker/SKILL.md").decode("utf-8")
        metadata = skill.split("---", 2)[1]
        description = next(line.removeprefix("description: ") for line in metadata.splitlines()
                           if line.startswith("description: "))
        self.assertGreater(len(description), 0)
        self.assertLessEqual(len(description), 200)

    def test_gemini_archive_is_same_payload_with_skill_extension(self):
        archive = self.build()
        self.assertEqual(archive.read_bytes(), archive.with_suffix(".skill").read_bytes())

    def test_web_export_keeps_every_instruction_and_validator_without_truncation(self):
        self.build()
        export = (self.output / f"{STAMP} Video Prompt Maker Web Instructions.md").read_text(encoding="utf-8")
        for source in [SOURCE / "SKILL.md", *sorted((SOURCE / "references").glob("*.md")),
                       SOURCE / "scripts" / "validate_prompt.py"]:
            with self.subTest(source=source.name):
                self.assertIn(source.read_text(encoding="utf-8").strip(), export)

    def test_extracted_validator_runs_from_an_unrelated_directory(self):
        archive = self.build()
        extracted = Path(self.temp.name) / "설치 경로 with spaces"
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(extracted)
        validator = extracted / "video-prompt-maker/scripts/validate_prompt.py"
        for extra, wanted, model in [("", 0, "seedance-2.0"), (" background music", 1, "seedance-2.0")]:
            prompt = Path(self.temp.name) / "프롬프트.txt"
            prompt.write_text('A door reads "발송완료". [Sound] no music' + extra, encoding="utf-8")
            result = subprocess.run([sys.executable, str(validator), str(prompt)],
                                    cwd=self.temp.name, capture_output=True)
            self.assertEqual(result.returncode, wanted, result.stderr)
            self.assertIn(f"model={model}".encode(), result.stdout)

    def test_checksums_match_all_downloads(self):
        self.build()
        lines = (self.output / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 3)
        for line in lines:
            digest, filename = line.split("  ", 1)
            self.assertRegex(digest, r"^[a-f0-9]{64}$")
            self.assertEqual(hashlib.sha256((self.output / filename).read_bytes()).hexdigest(), digest)

    def test_existing_release_is_not_overwritten(self):
        archive = self.build()
        before = archive.read_bytes()
        result = subprocess.run([sys.executable, str(BUILDER), "--output-dir", str(self.output),
                                 "--timestamp", STAMP], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(archive.read_bytes(), before)

    def test_timestamp_cannot_escape_output_directory(self):
        self.assertTrue(BUILDER.is_file(), "A reproducible release builder is missing")
        result = subprocess.run([sys.executable, str(BUILDER), "--output-dir", str(self.output),
                                 "--timestamp", "../../outside"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
