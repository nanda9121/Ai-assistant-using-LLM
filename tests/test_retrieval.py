import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import retrieval


class RetrievalTests(unittest.TestCase):
    def test_ranks_relevant_lines_and_ignores_comments(self):
        with tempfile.TemporaryDirectory() as directory:
            knowledge_file = Path(directory) / "knowledge.txt"
            knowledge_file.write_text(
                "# ignored comment\nPython is a programming language.\n"
                "Python supports clear data structures.\nUnrelated travel note.\n",
                encoding="utf-8",
            )
            with patch.object(retrieval, "KNOWLEDGE_FILE", knowledge_file):
                context = retrieval.retrieve_context("python data structures")

        self.assertEqual(
            context.splitlines(),
            ["Python supports clear data structures.", "Python is a programming language."],
        )

    def test_empty_query_and_nonpositive_limit_return_empty_context(self):
        self.assertEqual(retrieval.retrieve_context("..."), "")
        self.assertEqual(retrieval.retrieve_context("python", top_k=0), "")


if __name__ == "__main__":
    unittest.main()
