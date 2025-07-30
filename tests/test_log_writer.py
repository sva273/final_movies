import unittest
from unittest.mock import patch
from final_movies import log_writer


class TestLogWriter(unittest.TestCase):
    @patch("final_movies.log_writer.collection.insert_one")
    def test_log_search_success(self, mock_insert):
        mock_insert.return_value.inserted_id = "mocked_id"

        log_writer.log_search(
            search_type="keyword",
            params={"keyword": "test"},
            results_count=3,
        )
        mock_insert.assert_called_once()

    @patch("final_movies.log_writer.collection.insert_one", side_effect=Exception("Mongo error"))
    def test_log_search_failure(self, mock_insert):
        try:
            log_writer.log_search(
                search_type="genre_year",
                params={"genre_id": 1},
                results_count=5,
            )
        except Exception:
            self.fail("log_search() raised Exception unexpectedly")

