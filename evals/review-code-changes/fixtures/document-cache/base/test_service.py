import unittest

from cache import Cache
from repository import Document, Repository
from service import Service


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.document = Document("north", "inv-7", 1250)
        self.repository = Repository([self.document])
        self.service = Service(self.repository, Cache())
        self.principal = {"tenant": "north", "role": "reader"}

    def test_repeated_reads_use_cache(self):
        self.assertEqual(self.service.read(self.principal, "inv-7", 0), self.document)
        self.assertEqual(self.service.read(self.principal, "inv-7", 10), self.document)
        self.assertEqual(self.repository.reads, 1)

    def test_expired_entry_reads_updated_record(self):
        self.service.read(self.principal, "inv-7", 0)
        replacement = Document("north", "inv-7", 2000)
        self.repository.put(replacement)
        self.assertEqual(self.service.read(self.principal, "inv-7", 31), replacement)

    def test_role_denied_before_storage(self):
        with self.assertRaises(PermissionError):
            self.service.read({"tenant": "north", "role": "guest"}, "inv-7", 0)
        self.assertEqual(self.repository.reads, 0)

    def test_missing_document(self):
        with self.assertRaises(LookupError):
            self.service.read(self.principal, "missing", 0)


if __name__ == "__main__":
    unittest.main()
