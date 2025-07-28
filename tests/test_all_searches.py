import unittest
from unittest.mock import patch, MagicMock
from final_movies.all_searches import (
    select_genre,
    get_year_range,
    search_by_keyword_workflow,
    search_by_genre_and_year_workflow,
    search_by_rating_workflow,
)


class TestAllSearches(unittest.TestCase):

    @patch("builtins.input", side_effect=["1"])
    @patch("final_movies.all_searches.get_genre_movie_count", return_value=10)
    @patch("final_movies.all_searches.get_min_max_years_for_genre", return_value=(2000, 2010))
    @patch("final_movies.all_searches.get_all_genres", return_value=[{"genre_id": 1, "name": "Action"}])
    def test_select_genre(self, mock_genres, mock_years, mock_count, mock_input):
        result = select_genre()
        self.assertEqual(result, (1, (2000, 2010), "Action"))

    @patch("builtins.input", side_effect=["2001", "2005"])
    def test_get_year_range_valid(self, mock_input):
        result = get_year_range(2000, 2010)
        self.assertEqual(result, (2001, 2005))

    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "Matrix"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    @patch("builtins.input", return_value="matrix")
    def test_search_by_keyword_workflow(self, mock_input, mock_paginate, mock_log, mock_search):
        search_by_keyword_workflow()
        mock_search.assert_called_once()
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()

    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "Inception"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    @patch("final_movies.all_searches.get_year_range", return_value=(2001, 2005))
    @patch("final_movies.all_searches.select_genre", return_value=(2, (2000, 2010), "Drama"))
    def test_search_by_genre_and_year_workflow(self, mock_select, mock_years, mock_paginate, mock_log, mock_search):
        search_by_genre_and_year_workflow()
        mock_search.assert_called_once()
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()

    @patch("builtins.input", return_value="1")
    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "Toy Story"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    def test_search_by_rating_workflow(self, mock_paginate, mock_log, mock_search, mock_input):
        search_by_rating_workflow()
        mock_search.assert_called_once()
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()


if __name__ == "__main__":
    unittest.main()