import unittest
from unittest.mock import patch, MagicMock
from final_movies import all_searches

class TestAllSearches(unittest.TestCase):

    @patch("final_movies.all_searches.get_all_genres")
    @patch("final_movies.all_searches.display_genre_table")
    @patch("final_movies.all_searches.get_user_input", side_effect=["1"])
    def test_select_genre_valid(self, mock_input, mock_display, mock_get_all_genres):
        # Мокаем возвращаемые данные display_genre_table (словари с жанрами)
        mock_get_all_genres.return_value = [{"genre_id": 1, "name": "Comedy"}]
        mock_display.return_value = {1: (1980, 2020, "Comedy")}

        genre_id, years, name = all_searches.select_genre()

        self.assertEqual(genre_id, 1)
        self.assertEqual(years, (1980, 2020))
        self.assertEqual(name, "Comedy")

    @patch("final_movies.all_searches.get_user_input", side_effect=["1995", "2000"])
    def test_get_year_range_valid(self, mock_input):
        result = all_searches.get_year_range(1990, 2025)
        self.assertEqual(result, (1995, 2000))

    @patch("final_movies.all_searches.get_user_input", side_effect=["1800", "2020", "1990", "2020"])
    def test_get_year_range_invalid_then_valid(self, mock_input):
        # Первый ввод невалидный (1800 < 1990), второй ввод валидный
        result = all_searches.get_year_range(1990, 2025)
        self.assertEqual(result, (1990, 2020))

    @patch("final_movies.all_searches.get_user_input", side_effect=[""])
    @patch("final_movies.all_searches.search_movies", return_value=[])
    def test_search_by_keyword_workflow_empty_keyword(self, mock_search, mock_input):
        with patch("builtins.print") as mock_print:
            all_searches.search_by_keyword_workflow()
            mock_print.assert_any_call("⚠️ Keyword cannot be empty.")

    @patch("final_movies.all_searches.get_user_input", side_effect=["star"])
    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "Star Movie"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    def test_search_by_keyword_workflow_found(self, mock_paginate, mock_log, mock_search, mock_input):
        all_searches.search_by_keyword_workflow()
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()

    @patch("final_movies.all_searches.select_genre", return_value=(1, (1990, 2025), "Action"))
    @patch("final_movies.all_searches.get_year_range", return_value=(1995, 2000))
    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "Action Movie"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    def test_search_by_genre_and_year_workflow_found(self, mock_paginate, mock_log, mock_search, mock_year_range, mock_select):
        all_searches.search_by_genre_and_year_workflow()
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()

    @patch("final_movies.all_searches.display_ratings_table", return_value={1: "PG"})
    @patch("final_movies.all_searches.get_user_input", side_effect=["1"])
    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "PG Movie"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    def test_search_by_rating_workflow_found(self, mock_paginate, mock_log, mock_search, mock_input, mock_display_ratings):
        all_searches.search_by_rating_workflow()
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()

    @patch("final_movies.all_searches.display_ratings_table", return_value={1: "PG"})
    @patch("final_movies.all_searches.get_user_input", side_effect=["a", "5", "1"])
    @patch("final_movies.all_searches.search_movies", return_value=[{"title": "PG Movie"}])
    @patch("final_movies.all_searches.log_search")
    @patch("final_movies.all_searches.paginate_results")
    def test_search_by_rating_workflow_invalid_then_valid(self, mock_paginate, mock_log, mock_search, mock_input, mock_display_ratings):
        with patch("builtins.print") as mock_print:
            all_searches.search_by_rating_workflow()
            # Проверяем, что выводятся сообщения об ошибках при неправильном вводе
            mock_print.assert_any_call("❌ Only numbers are allowed. Please try again.")
            mock_print.assert_any_call("Invalid selection. Please enter a number between 1 and 1.")
        mock_log.assert_called_once()
        mock_paginate.assert_called_once()

if __name__ == "__main__":
    unittest.main()
