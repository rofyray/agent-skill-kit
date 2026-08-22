from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1]/"skills"/"interview-coach"/"scripts"/"coach_state.py"


class InterviewCoachStateTests(unittest.TestCase):
    def run_helper(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_init_creates_complete_valid_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)/"candidate-workspace"
            result = self.run_helper(
                "init",
                str(workspace),
                "--name",
                "Avery Chen",
                "--target-role",
                "Senior Product Manager",
                "--timeline",
                "2026-09-12",
                "--directness",
                "4",
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            self.assertEqual(len(payload["created"]), 4)
            self.assertTrue((workspace/"materials").is_dir())
            core = (workspace/"coaching_state.md").read_text(encoding="utf-8")
            self.assertIn("Avery Chen", core)
            self.assertIn("Senior Product Manager", core)
            self.assertIn("Directness: 4", core)

            validation = self.run_helper("validate", str(workspace))
            self.assertEqual(validation.returncode, 0, validation.stderr + validation.stdout)

    def test_init_preserves_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)/"candidate-workspace"
            first = self.run_helper("init", str(workspace))
            self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
            core_path = workspace/"coaching_state.md"
            original = core_path.read_text(encoding="utf-8") + "\nUser note: preserve me\n"
            core_path.write_text(original, encoding="utf-8")

            second = self.run_helper("init", str(workspace), "--name", "Different Name")
            self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
            payload = json.loads(second.stdout)
            self.assertIn("coaching_state.md", payload["preserved"])
            self.assertEqual(core_path.read_text(encoding="utf-8"), original)

    def test_validate_detects_missing_heading_and_duplicate_story_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)/"candidate-workspace"
            created = self.run_helper("init", str(workspace))
            self.assertEqual(created.returncode, 0, created.stderr + created.stdout)

            core_path = workspace/"coaching_state.md"
            core_path.write_text(
                core_path.read_text(encoding="utf-8").replace("## Coaching Preferences", "## Preferences"),
                encoding="utf-8",
            )
            story_path = workspace/"coaching_state.storybank.md"
            with story_path.open("a", encoding="utf-8") as handle:
                handle.write("\n### S001 - First\n\n### S001 - Duplicate\n")

            validation = self.run_helper("validate", str(workspace))
            self.assertEqual(validation.returncode, 1)
            self.assertIn("missing heading '## Coaching Preferences'", validation.stdout)
            self.assertIn("duplicate story ID S001", validation.stdout)

    def test_status_reports_structured_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)/"candidate-workspace"
            created = self.run_helper("init", str(workspace))
            self.assertEqual(created.returncode, 0, created.stderr + created.stdout)

            story_path = workspace/"coaching_state.storybank.md"
            with story_path.open("a", encoding="utf-8") as handle:
                handle.write("\n### S001 - Migration\n")
            loops_path = workspace/"coaching_state.loops.md"
            loops_text = loops_path.read_text(encoding="utf-8").replace(
                "## Active Loops\n",
                "## Active Loops\n### Acme - Staff Engineer\n",
            )
            loops_path.write_text(loops_text, encoding="utf-8")

            status = self.run_helper("status", str(workspace))
            self.assertEqual(status.returncode, 0, status.stderr + status.stdout)
            payload = json.loads(status.stdout)
            self.assertEqual(payload["stories"], 1)
            self.assertEqual(payload["active_loops"], 1)

    def test_migration_plan_routes_and_hashes_complete_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)/"legacy-workspace"
            workspace.mkdir()
            (workspace/"coaching_state.md").write_text(
                """# Legacy Coaching State

## Current Truth
- Primary bottleneck: Relevance

## Profile
- Target: Senior PM

## Storybank
### S001 - Launch
- Result: 20% adoption increase

## Interview Loops
### Acme - Senior PM

## Score History
| Date | Score |

## Custom Notes
- Preserve this section
""",
                encoding="utf-8",
            )

            result = self.run_helper("migration-plan", str(workspace))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            destinations = {
                section["heading"]: section["destination"] for section in payload["sections"]
            }
            self.assertEqual(destinations["Current Truth"], "coaching_state.md")
            self.assertEqual(destinations["Storybank"], "coaching_state.storybank.md")
            self.assertEqual(destinations["Interview Loops"], "coaching_state.loops.md")
            self.assertEqual(destinations["Score History"], "coaching_state.history.md")
            self.assertEqual(destinations["Custom Notes"], "manual-review")
            self.assertEqual(payload["manual_review"], ["Custom Notes"])
            self.assertFalse(payload["ready_for_lossless_split"])
            self.assertEqual(payload["section_count"], 6)
            self.assertTrue(all(len(section["sha256"]) == 64 for section in payload["sections"]))

    def test_verify_migration_proves_exact_preservation_and_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)/"migrated-workspace"
            workspace.mkdir()
            preamble = "# Legacy Coaching State\n\n"
            current = "## Current Truth\n- Primary bottleneck: Relevance\n\n"
            profile = "## Profile\n- Target: Senior PM\n\n"
            story = "## Storybank\n### S001 - Launch\n- Result: 20% adoption increase\n\n"
            score = "## Score History\n| Date | Score |\n| --- | --- |\n"
            legacy = preamble + current + profile + story + score
            backup = workspace/"coaching_state.legacy-backup.md"
            backup.write_text(legacy, encoding="utf-8")

            (workspace/"coaching_state.md").write_text(
                preamble
                + "## Current Truth\n- Primary bottleneck: Structure\n\n"
                + profile
                + """## Active Coaching Strategy
- Directness: 3

## Coaching Preferences
- Helpful formats: Unknown

## State Files
- Storybank: coaching_state.storybank.md
- Loops and materials: coaching_state.loops.md
- History: coaching_state.history.md
""",
                encoding="utf-8",
            )
            (workspace/"coaching_state.storybank.md").write_text(
                """# Interview Coaching Storybank

## Story Index
| ID | Title | Competencies | Strength | Last used | Evidence status |
| --- | --- | --- | --- | --- | --- |

## Story Details

"""
                + story,
                encoding="utf-8",
            )
            (workspace/"coaching_state.loops.md").write_text(
                """# Interview Coaching Loops

## Active Loops

## Past Loops
| Company | Role | Outcome | Closed | Durable lesson |
| --- | --- | --- | --- | --- |

## Materials Index
| Company | Artifact | Path | Updated |
| --- | --- | --- | --- |
""",
                encoding="utf-8",
            )
            (workspace/"coaching_state.history.md").write_text(
                "# Interview Coaching History\n\n"
                + score
                + """
## Outcome Log
| Date | Company/role | Stage | Outcome | Evidence | Notes |
| --- | --- | --- | --- | --- | --- |

## Interview Intelligence

## Feedback Log
| Date | Source | Provenance | Feedback | Interpretation | State changes |
| --- | --- | --- | --- | --- | --- |

## Session Log
| Date | Operations | Durable changes | Recommended next |
| --- | --- | --- | --- |

## Meta-Check Log
| Date | Candidate feedback | Coaching adjustment |
| --- | --- | --- |

"""
                + current,
                encoding="utf-8",
            )
            (workspace/"materials").mkdir()
            source_hash = hashlib.sha256(legacy.encode("utf-8")).hexdigest()

            verification = self.run_helper(
                "verify-migration",
                str(workspace),
                "--backup",
                backup.name,
                "--expected-source-sha256",
                source_hash,
            )
            self.assertEqual(
                verification.returncode, 0, verification.stderr + verification.stdout
            )
            payload = json.loads(verification.stdout)
            self.assertTrue(payload["verified"])
            self.assertTrue(payload["source_hash_matches"])
            self.assertTrue(payload["preamble_preserved"])
            self.assertEqual(payload["missing_sections"], [])
            self.assertEqual(payload["missing_story_ids"], [])


if __name__ == "__main__":
    unittest.main()
