import unittest
from unittest.mock import patch

from commands import handle_command


class CommandTests(unittest.TestCase):
    def test_handles_exact_time_command(self):
        with patch("commands.datetime.datetime") as clock:
            clock.now.return_value.astimezone.return_value.strftime.return_value = "13:45"
            self.assertEqual(handle_command("what time is it"), "The current time is 13:45.")

    def test_search_query_is_url_encoded(self):
        with patch("commands.webbrowser.open", return_value=True) as open_browser:
            result = handle_command("search for coffee & tea")

        self.assertEqual(result, "Searching Google for coffee & tea")
        self.assertEqual(open_browser.call_args.args[0], "https://www.google.com/search?q=coffee+%26+tea")

    def test_arbitrary_shell_command_is_not_executed(self):
        with patch("commands.subprocess.Popen") as popen:
            result = handle_command("open notepad & echo unsafe")

        self.assertIn("only open these apps", result)
        popen.assert_not_called()

    def test_shutdown_requires_manual_os_action(self):
        with patch("commands.subprocess.Popen") as popen:
            result = handle_command("shutdown computer")

        self.assertIn("power menu", result)
        popen.assert_not_called()

    def test_unknown_command_is_left_for_the_llm(self):
        self.assertIsNone(handle_command("explain recursion"))


if __name__ == "__main__":
    unittest.main()
