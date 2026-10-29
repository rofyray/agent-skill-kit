from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


FIXTURES = Path(__file__).resolve().parents[1]/"evals"/"review-code-changes"/"fixtures"/"remaining"


class RemainingReviewFixturesTests(unittest.TestCase):
    """Check ground truth independently of model review outputs."""

    def probe(self, relative: str, code: str):
        result = subprocess.run(
            [sys.executable, "-B", "-c", code], cwd=FIXTURES/relative,
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_old_reader_compatibility_breaks_despite_new_reader_success(self):
        code = '''
import json
from writer import encode_amount
from old_reader import read_amount
try:
    value = read_amount(encode_amount(149))
except KeyError:
    value = "missing field"
print(json.dumps(value))
'''
        self.assertEqual(self.probe("disagreement/base", code), 149)
        self.assertEqual(self.probe("disagreement/candidate", code), "missing field")
        new_reader = code.replace("from old_reader import", "from new_reader import")
        self.assertEqual(self.probe("disagreement/candidate", new_reader), 149)

    def test_public_resource_limit_is_removed(self):
        code = '''
import json
from endpoint import render
try:
    value = len(render(65))
except ValueError:
    value = "rejected"
print(json.dumps(value))
'''
        self.assertEqual(self.probe("security/base", code), "rejected")
        self.assertEqual(self.probe("security/candidate", code), 65)

    def test_paired_corpus_has_one_regression_and_one_clean_change(self):
        code = '''
import json
from invoice import subtotal
print(json.dumps([subtotal([]), subtotal([149]), subtotal([149, 151])]))
'''
        for target in ("amber", "cobalt"):
            self.assertEqual(self.probe(f"evaluate/reviewer-inputs/{target}/base", code), [0, 149, 300])
        self.assertEqual(self.probe("evaluate/reviewer-inputs/amber/candidate", code), [0, 0, 149])
        self.assertEqual(self.probe("evaluate/reviewer-inputs/cobalt/candidate", code), [0, 149, 300])

    def test_rename_preserves_intentional_staleness_and_exact_expiry(self):
        code = '''
import json
from cache import read
print(json.dumps([read((149, 30), t, lambda: 151) for t in (0, 29, 30, 31)]))
'''
        for state in ("base", "previous", "current"):
            self.assertEqual(self.probe(f"rejected/{state}", code), [149, 149, 151, 151])


if __name__ == "__main__":
    unittest.main()
