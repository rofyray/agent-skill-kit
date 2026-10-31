from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT/"skills/build-and-maintain-a-second-brain/scripts"
sys.path.insert(0, str(SCRIPTS))
import second_brain_graph as graph
from second_brain import VaultError


class BrainGraphTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)/"vault"
        result = subprocess.run([sys.executable, str(SCRIPTS/"second_brain.py"), "init", str(self.root), "--name", "Test Brain"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        (self.root/"raw/source.txt").write_text("SECRET RAW CONTENT")
        subprocess.run([sys.executable, str(SCRIPTS/"second_brain.py"), "record-raw", str(self.root), "--all-new"], capture_output=True, check=True)

    def tearDown(self):
        self.temp.cleanup()

    def page(self, name, body="", title=None):
        path = self.root/"wiki"/f"{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'---\ntitle: "{title or name}"\nsummary: "A test page"\ntype: concept\nstatus: current\ncreated: 2026-10-30\nupdated: 2026-10-31\nsources:\n  - raw/source.txt#evidence\ntags:\n  - learning\n---\n{body}\n')
        return path

    def test_export_preserves_knowledge_and_excludes_raw_bodies(self):
        self.page("a", "[[b|Bee]] [[b#heading]]\n`[[fake]]`\n```\n[[also-fake]]\n```")
        self.page("b", "[A](a.md)")
        (self.root/"index.md").write_text("## Learning\n- [[a]]\n")
        paths = [p for p in self.root.rglob("*") if p.is_file()]
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        output, data = graph.export_viewer(self.root)
        self.assertEqual(before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
        self.assertNotIn("SECRET RAW CONTENT", (output/"graph.json").read_text())
        self.assertNotIn(str(self.root), (output/"graph.json").read_text())
        refs = [e for e in data["links"] if e["kind"] == "reference"]
        self.assertEqual([(e["source"], e["target"]) for e in refs], [("wiki/a.md", "wiki/b.md"), ("wiki/b.md", "wiki/a.md")])
        self.assertEqual(len(refs[0]["locators"]), 2)
        self.assertEqual(data["diagnostics"], [])
        self.assertEqual([n["indexed"] for n in data["nodes"] if n["kind"] == "page"], [True, False])
        self.assertEqual(graph.export_viewer(self.root)[1]["digest"], data["digest"])
        self.assertEqual(len([e for e in data["links"] if e["kind"] == "evidence"]), 2)

    def test_ambiguous_and_broken_links_do_not_invent_edges(self):
        self.page("one/topic")
        self.page("two/topic")
        self.page("index", "[[topic]] [[absent]] [[one/topic]] [[wrong/topic]]")
        data = graph.graph_snapshot(self.root)
        kinds = [d["kind"] for d in data["diagnostics"]]
        self.assertEqual(kinds.count("ambiguous-link"), 1)
        self.assertEqual(kinds.count("broken-link"), 2)
        self.assertEqual([(e["source"], e["target"]) for e in data["links"] if e["kind"] == "reference"], [("wiki/index.md", "wiki/one/topic.md")])

    def test_symlinks_are_skipped_and_output_cannot_overwrite_knowledge(self):
        outside = Path(self.temp.name)/"outside"
        outside.mkdir()
        (outside/"leak.md").write_text("private")
        (self.root/"wiki/linked").symlink_to(outside, target_is_directory=True)
        data = graph.graph_snapshot(self.root)
        self.assertFalse(any(n["id"].endswith("leak.md") for n in data["nodes"]))
        self.assertTrue(any(d["kind"] == "symlink" for d in data["diagnostics"]))
        for output in [self.root/"wiki/render", self.root, outside]:
            with self.assertRaises(VaultError):
                graph.export_viewer(self.root, output)
        (self.root/".second-brain/visualization").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(VaultError):
            graph.export_viewer(self.root)

    def test_untrusted_titles_remain_data_and_missing_sources_are_reported(self):
        self.page("hostile", "[[missing]]", "<img src=x onerror=alert(1)>")
        (self.root/"raw/source.txt").unlink()
        output, data = graph.export_viewer(self.root)
        self.assertEqual(data["nodes"][0]["title"], "<img src=x onerror=alert(1)>")
        self.assertNotIn("onerror=alert", (output/"index.html").read_text())
        self.assertTrue(any(d["kind"] == "missing-source" for d in data["diagnostics"]))

    def test_empty_vault_and_copied_helper_work_without_skill_assets(self):
        (self.root/"raw/source.txt").unlink()
        result = subprocess.run([sys.executable, str(self.root/"automation/second_brain.py"), "visualize", str(self.root), "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.root/".second-brain/visualization/graph.json").read_text())
        self.assertEqual(data["nodes"], [])
        self.assertEqual(data["links"], [])

    def test_server_exposes_only_generated_files(self):
        output, _ = graph.export_viewer(self.root)
        (output/"unrelated.txt").write_text("private")
        with graph.make_server(output) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            url = f"http://127.0.0.1:{server.server_port}"
            try:
                with urlopen(url + "/graph.json") as response:
                    self.assertEqual(response.status, 200)
                    self.assertIn("frame-ancestors 'none'", response.headers["Content-Security-Policy"])
                for path in ["/unrelated.txt", "/.viewer-owner", "/../raw/source.txt", "/%2e%2e/raw/source.txt"]:
                    with self.assertRaises(HTTPError) as error:
                        urlopen(url + path)
                    self.assertEqual(error.exception.code, 404)
                    error.exception.close()
                with self.assertRaises(HTTPError) as error:
                    urlopen(Request(url + "/graph.json", headers={"Host": "untrusted.example"}))
                self.assertEqual(error.exception.code, 403)
                error.exception.close()
                (output/"viewer.css").unlink()
                (output/"viewer.css").symlink_to(self.root/"raw/source.txt")
                with self.assertRaises(HTTPError) as error:
                    urlopen(url + "/viewer.css")
                error.exception.close()
            finally:
                server.shutdown()
                thread.join()


if __name__ == "__main__":
    unittest.main()
