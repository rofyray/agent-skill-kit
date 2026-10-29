from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT/"evals"/"review-code-changes"/"fixtures"/"document-cache"
STATES = ("base", "candidate", "revision", "clean")


class ReviewCodeChangesFixtureTests(unittest.TestCase):
    """Establish fixture ground truth, not whether an agent follows instructions."""

    def probe(self, state: str, source: str):
        result = subprocess.run(
            [sys.executable, "-B", "-c", source],
            cwd=FIXTURE/state,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_existing_tests_pass_even_in_defective_snapshots(self):
        for state in STATES:
            with self.subTest(state=state):
                result = subprocess.run(
                    [sys.executable, "-B", "-m", "unittest", "-v", "test_service.py"],
                    cwd=FIXTURE/state,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Ran 4 tests", result.stderr)

    def test_cross_tenant_collision_is_introduced_and_then_fixed(self):
        source = '''
import json
from cache import Cache
from repository import Document, Repository
from service import Service
repo = Repository([Document("north", "inv-7", 1250), Document("south", "inv-7", 9900)])
service = Service(repo, Cache())
first = service.read({"tenant": "north", "role": "reader"}, "inv-7", 0)
second = service.read({"tenant": "south", "role": "reader"}, "inv-7", 1)
print(json.dumps({"tenant": second.tenant, "amount": second.amount_cents, "reads": repo.reads}))
'''
        for state in STATES:
            with self.subTest(state=state):
                observed = self.probe(state, source)
                expected = (
                    {"tenant": "north", "amount": 1250, "reads": 1}
                    if state == "candidate"
                    else {"tenant": "south", "amount": 9900, "reads": 2}
                )
                self.assertEqual(observed, expected)

    def test_revision_introduces_exact_expiry_regression(self):
        source = '''
import json
from cache import Cache
from repository import Document, Repository
from service import Service
repo = Repository([Document("north", "inv-7", 1250)])
service = Service(repo, Cache())
principal = {"tenant": "north", "role": "reader"}
service.read(principal, "inv-7", 0)
repo.put(Document("north", "inv-7", 9900))
at_boundary = service.read(principal, "inv-7", 30)
after_boundary = service.read(principal, "inv-7", 31)
print(json.dumps([at_boundary.amount_cents, after_boundary.amount_cents]))
'''
        for state in STATES:
            with self.subTest(state=state):
                self.assertEqual(
                    self.probe(state, source),
                    [1250, 9900] if state == "revision" else [9900, 9900],
                )

    def test_legacy_defect_exists_in_every_snapshot(self):
        for state in STATES:
            with self.subTest(state=state):
                self.assertEqual(
                    self.probe(state, "import json; from legacy import summarize_cents; print(json.dumps(summarize_cents([149, 151])))"),
                    200,
                )

    def test_cached_documents_are_immutable_and_denied_roles_do_not_touch_storage(self):
        source = '''
import json
from dataclasses import FrozenInstanceError
from cache import Cache
from repository import Document, Repository
from service import Service
repo = Repository([Document("north", "inv-7", 1250)])
service = Service(repo, Cache())
document = service.read({"tenant": "north", "role": "reader"}, "inv-7", 0)
immutable = False
try:
    document.amount_cents = 1
except FrozenInstanceError:
    immutable = True
denied = False
try:
    service.read({"tenant": "north", "role": "guest"}, "missing", 1)
except PermissionError:
    denied = True
print(json.dumps([immutable, denied, repo.reads]))
'''
        for state in STATES:
            with self.subTest(state=state):
                self.assertEqual(self.probe(state, source), [True, True, 1])

    def test_contract_and_existing_tests_are_consistent_across_snapshots(self):
        for name in ("CONTRACT.md", "test_service.py", "repository.py", "legacy.py"):
            expected = (FIXTURE/"base"/name).read_bytes()
            for state in STATES:
                with self.subTest(state=state, name=name):
                    self.assertEqual((FIXTURE/state/name).read_bytes(), expected)

    def test_consumer_migration_requires_following_unchanged_caller(self):
        fixture = ROOT/"evals"/"review-code-changes"/"fixtures"/"consumer-migration"
        source = '''
import json
from catalog import price_for
from checkout import total
price = price_for("pen")
amount = price["amount_cents"] if isinstance(price, dict) else price.amount_cents
try:
    outcome = total(["pen", "book"])
except TypeError:
    outcome = "TypeError"
print(json.dumps([amount, outcome]))
'''
        for state, expected in (("base", [150, 1050]), ("candidate", [150, "TypeError"])):
            with self.subTest(state=state):
                result = subprocess.run([sys.executable, "-B", "-c", source], cwd=fixture/state, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), expected)


if __name__ == "__main__":
    unittest.main()
