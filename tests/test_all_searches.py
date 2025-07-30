import unittest
from unittest.mock import patch
from final_movies import all_searches


class TestAllSearches(unittest.TestCase):

    @patch("final_movies.all_searches.get_all_genres")
    @patch("final_movies.all_searches.get_min_max_years_for_genre")
    @patch("final_movies.all_searches.get_genre_movie_count")
    @patch("builtins.input", side_effect=["1"])
    def test_select_genre(self, mock_input, mock_count, mock_years, mock_genres):
        mock_genres.return_value = [{"genre_id": 1, "name": "Comedy"}]
        mock_years.return_value = (1980, 2020)
        mock_count.return_value = 10

        genre_id, years, name = all_searches.select_genre()
        self.assertEqual(genre_id, 1)
        self.assertEqual(years, (1980, 2020))
        self.assertEqual(name, "Comedy")

    @patch("builtins.input", side_effect=["2000", "2010"])
    def test_get_year_range_valid_input(self, mock_input):
        result = all_searches.get_year_range(1990, 2020)
        self.assertEqual(result, (2000, 2010))

    @patch("final_movies.all_searches.search_movies", return_value=[])
    @patch("builtins.input", side_effect=[""])
    def test_search_by_keyword_workflow_empty_keyword(self, mock_input, mock_search):
        # Должен обработать пустой ввод
        all_searches.search_by_keyword_workflow()

    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "Movie"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    @patch("builtins.input", side_effect=["star"])
    def test_search_by_keyword_workflow_found(self, mock_input, mock_paginate, mock_log, mock_search):
        all_searches.search_by_keyword_workflow()
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()

    @patch("final_movies.all_searches.select_genre", return_value=(1, (1990, 2000), "Action"))
    @patch("final_movies.all_searches.get_year_range", return_value=(1995, 1998))
    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "Movie"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    def test_search_by_genre_and_year_workflow_found(self, mock_paginate, mock_log, mock_search, mock_year_range, mock_select):
        all_searches.search_by_genre_and_year_workflow()
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()

    @patch("final_movies.all_searches.display_ratings_table", return_value={1: "G"})
    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "Movie"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    @patch("builtins.input", side_effect=["1"])
    def test_search_by_rating_workflow_found(self, mock_input, mock_paginate, mock_log, mock_search, mock_display):
        all_searches.search_by_rating_workflow()
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
