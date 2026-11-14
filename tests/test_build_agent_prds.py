from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/"skills"/"build-agent-prds"/"scripts"/"package_prd.py"
SPEC = importlib.util.spec_from_file_location("package_prd", SCRIPT)
assert SPEC and SPEC.loader
packager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(packager)


class PrdPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root/"Project handoff"
        self.source.mkdir()
        (self.source/"PRD.md").write_text(
            "# Product\n[Feature](features/account.md)\n![Mark](assets/mark.svg)\n",
            encoding="utf-8",
        )
        (self.source/"features").mkdir()
        (self.source/"features"/"account.md").write_text(
            "# Account\n[Driver](../PRD.md)\n", encoding="utf-8"
        )
        (self.source/"assets").mkdir()
        (self.source/"assets"/"mark.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"><title>Approved</title></svg>',
            encoding="utf-8",
        )
        self.output = self.root/"handoff.zip"

    def test_roundtrip_preserves_every_file_and_relative_layout(self):
        (self.source/"assets"/"résumé.bin").write_bytes(bytes(range(256)) * 8192)
        before = {p.relative_to(self.source): p.read_bytes()
                  for p in self.source.rglob("*") if p.is_file()}
        result = packager.package(self.source, self.output)
        self.assertEqual(result["files"], len(before))
        self.assertEqual(result["entry_point"], "Project handoff/PRD.md")
        self.assertEqual(len(result["sha256"]), 64)
        with zipfile.ZipFile(self.output) as archive:
            self.assertIsNone(archive.testzip())
            self.assertTrue(all(name.startswith("Project handoff/") for name in archive.namelist()))
            archive.extractall(self.root/"extracted")
        extracted = self.root/"extracted"/"Project handoff"
        for relative, data in before.items():
            self.assertEqual((extracted/relative).read_bytes(), data)
            self.assertEqual((self.source/relative).read_bytes(), data)
        self.assertTrue((extracted/"features"/".."/"PRD.md").is_file())

    def test_deterministic_archive_ignores_os_metadata(self):
        (self.source/".DS_Store").write_bytes(b"metadata")
        packager.package(self.source, self.output)
        second = self.root/"second.zip"
        packager.package(self.source, second)
        self.assertEqual(self.output.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(self.output) as archive:
            self.assertFalse(any(".DS_Store" in name for name in archive.namelist()))

    def test_missing_driver_rejected_without_output(self):
        (self.source/"PRD.md").unlink()
        with self.assertRaisesRegex(ValueError, "PRD.md"):
            packager.package(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_existing_output_is_not_overwritten(self):
        self.output.write_bytes(b"existing delivery")
        with self.assertRaisesRegex(ValueError, "already exists"):
            packager.package(self.source, self.output)
        self.assertEqual(self.output.read_bytes(), b"existing delivery")

    def test_output_inside_source_is_rejected(self):
        nested = self.source/"archive.zip"
        with self.assertRaisesRegex(ValueError, "outside"):
            packager.package(self.source, nested)
        self.assertFalse(nested.exists())

    def test_hidden_credentials_rejected_instead_of_silently_bundled(self):
        (self.source/".env").write_text("synthetic fixture only", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "non-delivery"):
            packager.package(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_dependency_directory_rejected(self):
        (self.source/"node_modules").mkdir()
        with self.assertRaisesRegex(ValueError, "non-delivery"):
            packager.package(self.source, self.output)

    def test_symlink_asset_cannot_pull_in_external_content(self):
        external = self.root/"outside.txt"
        external.write_text("not authorized for bundle", encoding="utf-8")
        (self.source/"assets"/"outside.txt").symlink_to(external)
        with self.assertRaisesRegex(ValueError, "symlink"):
            packager.package(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_symlink_directory_is_not_followed(self):
        (self.source/"assets"/"loop").symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            packager.package(self.source, self.output)

    def test_symlink_root_is_rejected(self):
        link = self.root/"linked-source"
        link.symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            packager.package(link, self.output)

    def test_windows_separator_in_filename_is_rejected(self):
        (self.source/"assets\\escape.txt").write_text("fixture", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "portable"):
            packager.package(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_failed_final_copy_removes_partial_download(self):
        original = packager.shutil.copyfileobj

        def fail_final(source, target, *args, **kwargs):
            if getattr(target, "name", None) == str(self.output):
                target.write(b"partial")
                raise OSError("simulated disk failure")
            return original(source, target, *args, **kwargs)

        with patch.object(packager.shutil, "copyfileobj", side_effect=fail_final):
            with self.assertRaisesRegex(OSError, "simulated disk failure"):
                packager.package(self.source, self.output)
        self.assertFalse(self.output.exists())
        self.assertTrue((self.source/"PRD.md").is_file())

    def test_invalid_output_suffix(self):
        with self.assertRaisesRegex(ValueError, ".zip"):
            packager.package(self.source, self.root/"handoff.tar")

    def test_cli_handles_spaces_and_returns_real_download_path(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.source), str(self.output)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(json.loads(result.stdout)["archive"]), self.output)
        duplicate = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.source), str(self.output)],
            capture_output=True, text=True,
        )
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn("already exists", duplicate.stderr)


if __name__ == "__main__":
    unittest.main()
