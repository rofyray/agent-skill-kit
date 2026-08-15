from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", SCRIPT)
assert SPEC and SPEC.loader
validate_skills = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_skills
SPEC.loader.exec_module(validate_skills)


class ValidateSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "skills").mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_skill(self, directory: str, name: str | None = None, extra: str = "") -> Path:
        skill_dir = self.root / "skills" / directory
        skill_dir.mkdir()
        skill_name = name or directory
        content = (
            "---\n"
            f"name: {skill_name}\n"
            "description: Perform a focused task. Use when the user asks for that task.\n"
            f"{extra}"
            "---\n\n"
            "# Focused Task\n\n"
            "1. Inspect the input.\n"
            "2. Produce and verify the result.\n"
        )
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
        return skill_dir

    def test_valid_skill(self) -> None:
        self.write_skill("focused-task")
        self.assertEqual(validate_skills.validate_root(self.root), [])

    def test_rejects_name_mismatch(self) -> None:
        self.write_skill("focused-task", name="other-task")
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("must match directory" in message for message in messages))

    def test_rejects_nonportable_frontmatter(self) -> None:
        self.write_skill("focused-task", extra="compatibility: Requires git\n")
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("may contain only name and description" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
