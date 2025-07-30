import unittest
from unittest.mock import patch, MagicMock
from final_movies import log_stats


class TestLogStats(unittest.TestCase):

    def test_format_search_label_keyword(self):
        label = log_stats.format_search_label("keyword", {"keyword": "Star Wars"})
        self.assertEqual(label, "Keyword: star wars")

    def test_format_search_label_genre_year(self):
        params = {"genre_name": "Action", "year_from": 1990, "year_to": 2000}
        label = log_stats.format_search_label("genre_year", params)
        self.assertEqual(label, "Genre: Action (1990-2000)")

    def test_format_search_label_rating(self):
        # Переопределяем доступные рейтинги для теста
        log_stats.available_ratings = {"R": "Restricted"}
        label = log_stats.format_search_label("rating", {"rating": "R"})
        self.assertEqual(label, "Rating: Restricted")

    @patch("final_movies.log_stats.collection.aggregate")
    def test_display_top_searches(self, mock_aggregate):
        mock_aggregate.return_value = [
            {"_id": {"search_type": "keyword", "params": {"keyword": "test"}}, "count": 3}
        ]
        with patch('builtins.print') as mock_print:
            log_stats.display_top_searches(limit=1)
            # Выведем все вызовы print для отладки
            print_calls = [call.args[0] for call in mock_print.call_args_list]
            print("PRINT CALLS:", print_calls)
            # Теперь assert (на основе реального вывода)
            self.assertTrue(any("Keyword: test" in call for call in print_calls))

    @patch("final_movies.log_stats.collection.aggregate")
    def test_display_last_unique_searches(self, mock_aggregate):
        mock_aggregate.return_value = [
            {
                "_id": {"search_type": "keyword", "params": {"keyword": "test"}},
                "latest_timestamp": 123456789,
                "results_count": 10,
            }
        ]
        with patch('builtins.print') as mock_print:
            log_stats.display_last_unique_searches(limit=1)
            mock_print.assert_any_call("1. Keyword: test, 10 results")


if __name__ == "__main__":
    unittest.main()
