import unittest
from unittest.mock import patch, MagicMock
from final_movies import log_writer


class TestLogWriter(unittest.TestCase):

    @patch("final_movies.log_writer.collection")
    @patch("builtins.print")
    def test_log_search_success(self, mock_print, mock_collection):
        """
        Тест успешного логирования запроса:
        проверяет, что insert_one вызывается и ID записи печатается.
        """
        mock_insert_result = MagicMock(inserted_id="abc123")
        mock_collection.insert_one.return_value = mock_insert_result

        log_writer.log_search(
            search_type="keyword",
            params={"q": "matrix"},
            results_count=1,
        )

        mock_collection.insert_one.assert_called_once()
        mock_print.assert_called_with("✅ Log entry inserted: abc123")

    @patch("final_movies.log_writer.collection")
    @patch("builtins.print")
    def test_log_search_failure(self, mock_print, mock_collection):
        """
        Тест неудачного логирования (исключение при insert_one):
        проверяет, что ошибка обрабатывается и выводится сообщение.
        """
        mock_collection.insert_one.side_effect = Exception("DB error")

        log_writer.log_search(
            search_type="genre",
            params={"genre_id": 5},
            results_count=0,
        )

        mock_collection.insert_one.assert_called_once()
        mock_print.assert_called_with("❌ Log insert failed: DB error")


if __name__ == "__main__":
    unittest.main()
