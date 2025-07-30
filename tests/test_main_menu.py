import unittest
from unittest.mock import patch
from final_movies import main

class TestMainMenu(unittest.TestCase):
    @patch("builtins.input", side_effect=["5"])
    def test_main_exits_on_5(self, mock_input):
        # Проверяем, что программа корректно завершилась на выборе 5
        try:
            main.main()
        except SystemExit:
            self.fail("main() raised SystemExit unexpectedly")

    @patch("builtins.input", side_effect=["1", "5"])
    @patch("final_movies.main.search_by_keyword_workflow")
    def test_main_calls_keyword_search(self, mock_search, mock_input):
        main.main()
        mock_search.assert_called_once()

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_main_handles_keyboard_interrupt(self, mock_input):
        # Проверяем, что прерывание клавиатурой обрабатывается без исключений
        try:
            main.main()
        except KeyboardInterrupt:
            self.fail("main() did not handle KeyboardInterrupt")

    @patch("builtins.input", side_effect=EOFError)
    def test_main_handles_eof_error(self, mock_input):
        # Проверяем, что EOFError тоже корректно обрабатывается
        try:
            main.main()
        except EOFError:
            self.fail("main() did not handle EOFError")

