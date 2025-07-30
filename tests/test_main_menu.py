import unittest
from unittest.mock import patch
from final_movies import main

class TestMainMenu(unittest.TestCase):
    @patch("builtins.input", side_effect=["5"])
    def test_main_exits_on_5(self, mock_input):
        try:
            main.main()
        except SystemExit:
            self.fail("main() raised SystemExit unexpectedly")

    @patch("builtins.input", side_effect=["1", "5"])
    @patch("final_movies.main.search_by_keyword_workflow")
    def test_main_calls_keyword_search(self, mock_search, mock_input):
        main.main()
        mock_search.assert_called_once()

