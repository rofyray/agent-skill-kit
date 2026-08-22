from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "package_skills.py"
SPEC = importlib.util.spec_from_file_location("package_skills", SCRIPT)
assert SPEC and SPEC.loader
package_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package_skills)


class PackageSkillsTests(unittest.TestCase):
    def test_archive_is_clean_rooted_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_dir = root / "example-skill"
            (skill_dir / "references").mkdir(parents=True)
            (skill_dir / "agents").mkdir()
            (skill_dir / "assets").mkdir()
            (skill_dir / "scripts" / "__pycache__").mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (skill_dir / "references" / "guide.md").write_text("guide\n", encoding="utf-8")
            (skill_dir / "agents" / "openai.yaml").write_text("interface:\n", encoding="utf-8")
            (skill_dir / "assets" / "CREDITS.txt").write_text("credits\n", encoding="utf-8")
            (skill_dir / ".DS_Store").write_text("ignored\n", encoding="utf-8")
            (skill_dir / "scripts" / "helper.pyc").write_bytes(b"bytecode")
            (skill_dir / "scripts" / "__pycache__" / "helper.pyc").write_bytes(b"bytecode")

            first = package_skills.package_skill(skill_dir, root / "first")
            second = package_skills.package_skill(skill_dir, root / "second")

            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(
                    archive.namelist(),
                    [
                        "example-skill/SKILL.md",
                        "example-skill/agents/openai.yaml",
                        "example-skill/assets/CREDITS.txt",
                        "example-skill/references/guide.md",
                    ],
                )
                self.assertNotIn(".DS_Store", "\n".join(archive.namelist()))
                self.assertNotIn(".pyc", "\n".join(archive.namelist()))


if __name__ == "__main__":
    unittest.main()
