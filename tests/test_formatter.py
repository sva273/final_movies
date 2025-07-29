import unittest
from unittest.mock import patch
from final_movies import formatter


class TestPaginateResults(unittest.TestCase):
    def setUp(self):
        # Подготовка тестовых данных — список из 15 фильмов
        self.sample_data = [
            {"title": f"Movie {i}", "release_year": 2000 + i, "rating": "PG"}
            for i in range(15)
        ]

    def test_invalid_input_type(self):
        # Тест на случай, если в функцию передан не список
        with patch("builtins.print") as mock_print:
            formatter.paginate_results("not_a_list")
            mock_print.assert_any_call(
                "⚠️ Invalid data passed to paginate_results: expected a list."
            )

    def test_empty_list(self):
        # Тест обработки пустого списка
        with patch("builtins.print") as mock_print:
            formatter.paginate_results([])
            mock_print.assert_any_call("⚠️ No data to display.")

    @patch("builtins.input", side_effect=["q"])
    def test_quit_command(self, mock_input):
        # Тест выхода при вводе команды 'q'
        with patch("builtins.print") as mock_print:
            formatter.paginate_results(self.sample_data[:5], page_size=10)
            mock_print.assert_any_call("\n=== Found 5 movies | Page 1 of 1 ===")

    @patch("builtins.input", side_effect=["n", "q"])
    def test_next_page_command(self, mock_input):
        # Тест перехода на следующую страницу
        with patch("builtins.print") as mock_print:
            formatter.paginate_results(self.sample_data, page_size=5)
            mock_print.assert_any_call("\n=== Found 15 movies | Page 2 of 3 ===")

    @patch("builtins.input", side_effect=["p", "q"])
    def test_prev_command_on_first_page(self, mock_input):
        # Тест команды 'p' на первой странице (нельзя перейти назад)
        with patch("builtins.print") as mock_print:
            formatter.paginate_results(self.sample_data, page_size=5)
            mock_print.assert_any_call("✅ Already on the first page.")

    @patch("builtins.input", side_effect=["g 2", "q"])
    def test_go_to_valid_page(self, mock_input):
        # Тест перехода на корректную страницу по команде 'g'
        with patch("builtins.print") as mock_print:
            formatter.paginate_results(self.sample_data, page_size=5)
            mock_print.assert_any_call("\n=== Found 15 movies | Page 2 of 3 ===")

    @patch("builtins.input", side_effect=["g x", "q"])
    def test_go_to_invalid_page_string(self, mock_input):
        # Тест некорректного ввода номера страницы (не число)
        with patch("builtins.print") as mock_print:
            formatter.paginate_results(self.sample_data, page_size=5)
            mock_print.assert_any_call("⚠️ Please enter a valid page number after 'g'.")

    @patch("builtins.input", side_effect=["g 999", "q"])
    def test_go_to_invalid_page_number(self, mock_input):
        # Тест перехода на несуществующую страницу
        with patch("builtins.print") as mock_print:
            formatter.paginate_results(self.sample_data, page_size=5)
            mock_print.assert_any_call("⚠️ Invalid page number.")

    @patch("builtins.input", side_effect=["unknown", "q"])
    def test_invalid_command(self, mock_input):
        # Тест обработки неизвестной команды
        with patch("builtins.print") as mock_print:
            formatter.paginate_results(self.sample_data, page_size=5)
            mock_print.assert_any_call("⚠️ Invalid command.")


if __name__ == "__main__":
    unittest.main()
