import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import memory


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory_file = Path(self.temp_dir.name) / "memory.json"
        self.memory_patch = patch.object(memory, "MEMORY_FILE", self.memory_file)
        self.memory_patch.start()

    def tearDown(self):
        self.memory_patch.stop()
        self.temp_dir.cleanup()

    def test_adds_and_deduplicates_facts_case_insensitively(self):
        self.assertTrue(memory.add_fact("  likes coffee  "))
        self.assertFalse(memory.add_fact("LIKES COFFEE"))
        self.assertEqual(memory.load_memory()["facts"], ["likes coffee"])

    def test_missing_memory_returns_independent_default_lists(self):
        first = memory.load_memory()
        first["facts"].append("temporary")
        self.assertEqual(memory.load_memory()["facts"], [])

    def test_clear_memory_restores_defaults(self):
        memory.add_fact("Likes coffee")
        memory.clear_memory()
        self.assertEqual(memory.load_memory(), memory.DEFAULT_MEMORY)

    def test_corrupt_memory_is_reported_instead_of_silently_reset(self):
        self.memory_file.write_text("{invalid", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Could not read assistant memory"):
            memory.load_memory()

    def test_saved_json_is_valid_and_has_newline(self):
        memory.add_fact("Uses Python")
        content = self.memory_file.read_text(encoding="utf-8")
        self.assertTrue(content.endswith("\n"))
        self.assertEqual(json.loads(content)["facts"], ["Uses Python"])


if __name__ == "__main__":
    unittest.main()
