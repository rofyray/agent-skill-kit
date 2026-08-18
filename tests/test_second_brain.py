from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "build-and-maintain-a-second-brain" / "scripts" / "second_brain.py"


class SecondBrainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault = Path(self.temp_dir.name) / "vault"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_helper(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def init(self, *arguments: str) -> None:
        result = self.run_helper(
            "init",
            str(self.vault),
            "--name",
            "Test Brain",
            "--scope",
            "Research and projects",
            *arguments,
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_init_uses_distinct_user_domains(self) -> None:
        self.init("--domain", "AI creative production", "--domain", "Work & projects", "--domain", "work   & projects")

        index = (self.vault / "index.md").read_text(encoding="utf-8")
        self.assertIn("## AI creative production", index)
        self.assertEqual(index.count("## Work & projects"), 1)
        self.assertIn("## Cross-domain syntheses", index)
        config = json.loads((self.vault / ".second-brain/config.json").read_text(encoding="utf-8"))
        self.assertEqual(config["domains"], ["AI creative production", "Work & projects"])

    def test_single_real_page_is_not_reported_as_orphan(self) -> None:
        self.init()
        raw = self.vault / "raw" / "source.txt"
        raw.write_text("Evidence", encoding="utf-8")
        recorded = self.run_helper("record-raw", str(self.vault), str(raw))
        self.assertEqual(recorded.returncode, 0, recorded.stderr or recorded.stdout)
        page = self.vault / "wiki" / "first-page.md"
        page.write_text(
            "---\n"
            'title: "First page"\n'
            'summary: "The first grounded page."\n'
            "type: concept\n"
            "created: 2026-08-18\n"
            "updated: 2026-08-18\n"
            "status: current\n"
            "sources:\n"
            "  - raw/source.txt\n"
            "---\n\n"
            "A grounded claim from [the source](../raw/source.txt).\n",
            encoding="utf-8",
        )
        (self.vault / "index.md").write_text("# Wiki Index\n\n- [[first-page]]\n", encoding="utf-8")

        result = self.run_helper("scan", str(self.vault), "--json")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["orphan_pages"], [])

    def test_scan_ignores_example_links_inside_code(self) -> None:
        self.init()
        raw = self.vault / "raw" / "source.txt"
        raw.write_text("Evidence", encoding="utf-8")
        self.assertEqual(self.run_helper("record-raw", str(self.vault), str(raw)).returncode, 0)
        page = self.vault / "wiki" / "example-aware.md"
        page.write_text(
            "---\n"
            'title: "Example aware"\n'
            'summary: "Separates examples from links."\n'
            "type: concept\n"
            "created: 2026-08-18\n"
            "updated: 2026-08-18\n"
            "status: current\n"
            "sources:\n"
            "  - raw/source.txt\n"
            "---\n\n"
            "Grounded in [the source](../raw/source.txt).\n\n"
            "```markdown\n[[not-a-real-page]]\n```\n",
            encoding="utf-8",
        )
        (self.vault / "index.md").write_text("# Wiki Index\n\n- [[example-aware]]\n", encoding="utf-8")

        result = self.run_helper("scan", str(self.vault), "--json")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(json.loads(result.stdout)["broken_wikilinks"], [])

    def test_scan_rejects_invalid_frontmatter_values(self) -> None:
        self.init()
        page = self.vault / "wiki" / "invalid-page.md"
        page.write_text(
            "---\n"
            'title: "Invalid page"\n'
            'title: "Duplicate title"\n'
            'summary: "Exercises value validation."\n'
            "type: made-up\n"
            "created: yesterday\n"
            "updated: 2026-08-18\n"
            "status: active\n"
            "sources: raw/source.txt\n"
            "---\n",
            encoding="utf-8",
        )

        result = self.run_helper("scan", str(self.vault), "--json")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        findings = json.loads(result.stdout)["pages_invalid_fields"]["wiki/invalid-page.md"]
        syntax = json.loads(result.stdout)["pages_frontmatter_syntax"]["wiki/invalid-page.md"]
        self.assertTrue(any("duplicate key" in finding for finding in syntax))
        self.assertTrue(any("type" in finding for finding in findings))
        self.assertTrue(any("status" in finding for finding in findings))
        self.assertTrue(any("created" in finding for finding in findings))
        self.assertTrue(any("sources" in finding for finding in findings))

    def test_scan_validates_recurring_ingest_definitions(self) -> None:
        self.init()
        schedule_path = self.vault / ".second-brain" / "ingest-schedules.json"
        schedule_path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "sources": [
                        {
                            "id": "Research Inbox",
                            "kind": "folder",
                            "locator": "",
                            "cadence": "weekdays at 18:00",
                            "timezone": "America/Chicago",
                            "enabled": "yes",
                            "max_items_per_run": 0,
                            "max_bytes_per_run": 1000,
                            "checkpoint": [],
                            "api_key": "do-not-store-this",
                        }
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        result = self.run_helper("scan", str(self.vault), "--json")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        issues = json.loads(result.stdout)["ingest_schedule_issues"]
        self.assertTrue(any("id" in issue for issue in issues))
        self.assertTrue(any("kind" in issue for issue in issues))
        self.assertTrue(any("enabled" in issue for issue in issues))
        self.assertTrue(any("max_items_per_run" in issue for issue in issues))
        self.assertTrue(any("checkpoint" in issue for issue in issues))
        self.assertTrue(any("credential-like" in issue or "unknown fields" in issue for issue in issues))

    def test_scan_accepts_versioned_url_normalization(self) -> None:
        self.init()
        schedule_path = self.vault / ".second-brain" / "ingest-schedules.json"
        schedule_path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "sources": [
                        {
                            "id": "weekly-briefing",
                            "kind": "url",
                            "locator": "https://example.com/briefing",
                            "cadence": "Mondays at 08:00",
                            "timezone": "America/Chicago",
                            "enabled": True,
                            "max_items_per_run": 1,
                            "max_bytes_per_run": 5000000,
                            "normalization": {"strategy": "readable-main-content", "version": "1"},
                            "checkpoint": {},
                        }
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        result = self.run_helper("scan", str(self.vault), "--json")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(json.loads(result.stdout)["ingest_schedule_issues"], [])

    def test_checkpoint_update_is_compare_and_set(self) -> None:
        self.init()
        schedule_path = self.vault / ".second-brain" / "ingest-schedules.json"
        schedule_path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "sources": [
                        {
                            "id": "research-inbox",
                            "kind": "directory",
                            "locator": str(self.vault.parent / "research-inbox"),
                            "cadence": "weekdays at 18:00",
                            "timezone": "America/Chicago",
                            "enabled": True,
                            "max_items_per_run": 20,
                            "max_bytes_per_run": 50000000,
                            "normalization": None,
                            "checkpoint": {},
                        }
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        shown = self.run_helper(
            "ingest-checkpoint", "show", str(self.vault), "research-inbox", "--json"
        )
        self.assertEqual(shown.returncode, 0, shown.stderr or shown.stdout)
        digest = json.loads(shown.stdout)["checkpoint_sha256"]
        replacement = json.dumps({"last_identity": "research-inbox:abc123"})

        updated = self.run_helper(
            "ingest-checkpoint",
            "update",
            str(self.vault),
            "research-inbox",
            "--expected-sha256",
            digest,
            "--checkpoint-json",
            replacement,
            "--json",
        )
        self.assertEqual(updated.returncode, 0, updated.stderr or updated.stdout)
        stale = self.run_helper(
            "ingest-checkpoint",
            "update",
            str(self.vault),
            "research-inbox",
            "--expected-sha256",
            digest,
            "--checkpoint-json",
            json.dumps({"last_identity": "research-inbox:def456"}),
            "--json",
        )
        self.assertEqual(stale.returncode, 3, stale.stderr or stale.stdout)
        current = json.loads(schedule_path.read_text(encoding="utf-8"))["sources"][0]["checkpoint"]
        self.assertEqual(current, {"last_identity": "research-inbox:abc123"})


if __name__ == "__main__":
    unittest.main()
