import unittest
from unittest.mock import patch, MagicMock
from final_movies import log_stats


class TestLogStats(unittest.TestCase):
    @patch("final_movies.log_stats.collection")
    @patch("builtins.print")
    def test_display_top_searches_keyword(self, mock_print, mock_collection):
        mock_collection.aggregate.return_value = [
            {"_id": {"keyword": "Matrix"}, "count": 3},
            {"_id": {"keyword": "Inception"}, "count": 2},
        ]

        log_stats.display_top_searches()

        assert mock_collection.aggregate.called
        mock_print.assert_any_call("\n=== Top 5 Keyword Searches ===")
        mock_print.assert_any_call("1. matrix, count: 3")
        mock_print.assert_any_call("2. inception, count: 2")

    @patch("final_movies.log_stats.collection")
    @patch("builtins.print")
    def test_display_last_unique_searches_keyword(self, mock_print, mock_collection):
        mock_collection.aggregate.return_value = [
            {
                "_id": {"search_type": "keyword", "params": {"keyword": "Matrix"}},
                "latest_timestamp": "2024-06-01T00:00:00",
                "results_count": 5,
            }
        ]

        log_stats.display_last_unique_searches()

        mock_print.assert_any_call("\n=== Last 5 Unique Searches ===")
        mock_print.assert_any_call("1. keyword | Matrix, 5 results")

    @patch("final_movies.log_stats.collection")
    @patch("builtins.print")
    def test_display_last_rating_searches(self, mock_print, mock_collection):
        mock_collection.find.return_value.sort.return_value.limit.return_value = [
            {
                "params": {"rating": "PG-13"},
                "results_count": 4,
            }
        ]

        log_stats.display_last_rating_searches()

        mock_print.assert_any_call("\n=== Last 5 Rating Searches ===")
        mock_print.assert_any_call("1. Rating: PG-13 | 4 results")

    @patch("final_movies.log_stats.collection.aggregate", side_effect=Exception("DB error"))
    @patch("builtins.print")
    def test_error_handling_aggregate(self, mock_print, _):
        log_stats.display_top_searches()
        mock_print.assert_any_call("❌ Error fetching logs: DB error")

    @patch("final_movies.log_stats.collection.find", side_effect=Exception("DB fail"))
    @patch("builtins.print")
    def test_error_handling_find(self, mock_print, _):
        log_stats.display_last_rating_searches()
        mock_print.assert_any_call("❌ Error fetching logs: DB fail")


if __name__ == "__main__":
    unittest.main()