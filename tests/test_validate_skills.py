from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1]/"scripts"/"validate_skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", SCRIPT)
assert SPEC and SPEC.loader
validate_skills = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_skills
SPEC.loader.exec_module(validate_skills)


class ValidateSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root/"skills").mkdir()
        (self.root/"evals").mkdir()
        (self.root/"README.md").write_text(
            "[focused-task](skills/focused-task/)\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_skill(self, directory: str, name: str | None = None, extra: str = "") -> Path:
        skill_dir = self.root/"skills"/directory
        skill_dir.mkdir()
        skill_name = name or directory
        content = (
            "---\n"
            f"name: {skill_name}\n"
            "description: Perform a focused task. Use when the user asks for that task.\n"
            f"{extra}"
            "---\n\n"
            "# Focused Task\n\n"
            "## Help mode\n\n"
            "When the user asks for help mode, read references/help.md and return its guide.\n\n"
            "1. Inspect the input.\n"
            "2. Produce and verify the result.\n"
        )
        (skill_dir/"SKILL.md").write_text(content, encoding="utf-8")
        references_dir = skill_dir/"references"
        references_dir.mkdir()
        (references_dir/"help.md").write_text(
            "# Focused Task Help\n\n"
            "## What this skill does\n\nExplains the task.\n\n"
            "## Modes\n\n- `run`: Perform the task.\n\n"
            "## Start here\n\nProvide the input.\n\n"
            "## Examples\n\n- `Run the focused task on this input.`\n",
            encoding="utf-8",
        )
        agents_dir = skill_dir/"agents"
        agents_dir.mkdir()
        (agents_dir/"openai.yaml").write_text(
            'interface:\n'
            '  display_name: "Focused Task"\n'
            '  short_description: "Perform and verify a focused task"\n'
            '  default_prompt: "Perform this focused task and verify the result."\n',
            encoding="utf-8",
        )
        eval_dir = self.root/"evals"/directory
        eval_dir.mkdir()
        (eval_dir/"cases.json").write_text(
            '{"skill": "' + directory + '", "cases": '
            '[{"request": "Do the task", "expect": ["Verified result"]}, '
            '{"request": "help", "mode": "help", '
            '"expect": ["Explains modes and examples without execution"]}]}\n',
            encoding="utf-8",
        )
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

    def test_rejects_description_over_claude_desktop_limit(self) -> None:
        skill_dir = self.write_skill("focused-task")
        long_description = "Use when " + "x" * 193
        (skill_dir/"SKILL.md").write_text(
            f"---\nname: focused-task\ndescription: {long_description}\n---\n\n# Focused Task\n",
            encoding="utf-8",
        )
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("at most 200 characters" in message for message in messages))

    def test_requires_openai_metadata(self) -> None:
        skill_dir = self.write_skill("focused-task")
        (skill_dir/"agents"/"openai.yaml").unlink()
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("missing agents/openai.yaml" in message for message in messages))

    def test_rejects_client_specific_default_prompt(self) -> None:
        skill_dir = self.write_skill("focused-task")
        (skill_dir/"agents"/"openai.yaml").write_text(
            'interface:\n'
            '  display_name: "Focused Task"\n'
            '  short_description: "Perform and verify a focused task"\n'
            '  default_prompt: "Use $focused-task to do this work."\n',
            encoding="utf-8",
        )
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("invocation-neutral" in message for message in messages))

    def test_requires_matching_eval_cases(self) -> None:
        self.write_skill("focused-task")
        (self.root/"evals"/"focused-task"/"cases.json").unlink()
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("missing evaluation cases" in message for message in messages))

    def test_requires_help_reference(self) -> None:
        skill_dir = self.write_skill("focused-task")
        (skill_dir/"references"/"help.md").unlink()
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("missing references/help.md" in message for message in messages))

    def test_requires_help_route(self) -> None:
        skill_dir = self.write_skill("focused-task")
        skill_path = skill_dir/"SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "When the user asks for help mode, read references/help.md and return its guide.\n\n",
                "",
            ),
            encoding="utf-8",
        )
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("must route help mode" in message for message in messages))

    def test_requires_help_eval_case(self) -> None:
        self.write_skill("focused-task")
        eval_path = self.root/"evals"/"focused-task"/"cases.json"
        eval_path.write_text(
            '{"skill": "focused-task", "cases": '
            '[{"request": "Do the task", "expect": ["Verified result"]}]}\n',
            encoding="utf-8",
        )
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("mode 'help'" in message for message in messages))

    def test_requires_bare_help_eval_request(self) -> None:
        self.write_skill("focused-task")
        eval_path = self.root/"evals"/"focused-task"/"cases.json"
        eval_path.write_text(
            '{"skill": "focused-task", "cases": '
            '[{"request": "Do the task", "expect": ["Verified result"]}, '
            '{"request": "Show the guide", "mode": "help", '
            '"expect": ["Explains modes and examples without execution"]}]}\n',
            encoding="utf-8",
        )
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("bare request 'help'" in message for message in messages))

    def test_requires_readme_catalog_entry(self) -> None:
        self.write_skill("focused-task")
        (self.root/"README.md").write_text("# Catalog\n", encoding="utf-8")
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("missing skill directory entry" in message for message in messages))

    def test_rejects_em_dash(self) -> None:
        skill_dir = self.write_skill("focused-task")
        skill_path = skill_dir/"SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8") + "\nForbidden \u2014 dash.\n",
            encoding="utf-8",
        )
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("forbidden em dash" in message for message in messages))

    def test_rejects_whitespace_adjacent_to_forward_slash(self) -> None:
        skill_dir = self.write_skill("focused-task")
        skill_path = skill_dir/"SKILL.md"
        forbidden = "Codex " + "/" + " IDE"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8") + f"\n{forbidden}\n",
            encoding="utf-8",
        )
        messages = [issue.message for issue in validate_skills.validate_root(self.root)]
        self.assertTrue(any("whitespace adjacent to a forward slash" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
