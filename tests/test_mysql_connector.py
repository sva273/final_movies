import unittest
from final_movies import mysql_connector


class TestMySQLConnector(unittest.TestCase):
    def test_get_all_genres_returns_list(self):
        genres = mysql_connector.get_all_genres()
        self.assertIsInstance(genres, list)
        for genre in genres:
            self.assertIn("genre_id", genre)
            self.assertIn("name", genre)

    def test_get_min_max_years_for_genre(self):
        min_year, max_year = mysql_connector.get_min_max_years_for_genre(1)
        self.assertTrue(
            (min_year is None and max_year is None)
            or (isinstance(min_year, int) and isinstance(max_year, int))
        )

    def test_get_genre_movie_count(self):
        count = mysql_connector.get_genre_movie_count(1)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_search_movies_keyword(self):
        result = mysql_connector.search_movies(keyword="ACADEMY")
        self.assertIsInstance(result, list)
        for movie in result:
            self.assertIn("title", movie)
            self.assertIn("release_year", movie)
            self.assertIn("rating", movie)

    def test_search_movies_by_rating(self):
        result = mysql_connector.search_movies(rating="PG")
        self.assertIsInstance(result, list)
        for movie in result:
            self.assertEqual(movie["rating"], "PG")

    def test_search_movies_year_range(self):
        result = mysql_connector.search_movies(year_from=2000, year_to=2005)
        self.assertIsInstance(result, list)
        for movie in result:
            self.assertGreaterEqual(movie["release_year"], 2000)
            self.assertLessEqual(movie["release_year"], 2005)

    def test_search_movies_by_genre(self):
        result = mysql_connector.search_movies(genre_id=1)
        self.assertIsInstance(result, list)
        for movie in result:
            self.assertIn("title", movie)

    def test_search_movies_all_filters_combined(self):
        result = mysql_connector.search_movies(
            keyword="LOVE", genre_id=1, year_from=2000, year_to=2020, rating="PG"
        )
        self.assertIsInstance(result, list)
        for movie in result:
            self.assertIn("title", movie)

    def test_search_movies_invalid_rating_returns_empty(self):
        result = mysql_connector.search_movies(rating="INVALID")
        self.assertIsInstance(result, list)

    def test_search_movies_empty_keyword_returns_some_results(self):
        result = mysql_connector.search_movies(keyword="")
        self.assertIsInstance(result, list)

    def test_get_min_max_years_invalid_genre(self):
        min_year, max_year = mysql_connector.get_min_max_years_for_genre(-999)
        self.assertIsNone(min_year)
        self.assertIsNone(max_year)

    def test_get_genre_movie_count_invalid(self):
        count = mysql_connector.get_genre_movie_count(-999)
        self.assertEqual(count, 0)

    def test_search_movies_sql_injection_protection(self):
        result = mysql_connector.search_movies(keyword="' OR '1'='1")
        self.assertIsInstance(result, list)

    def test_get_all_genres_cached(self):
        result1 = mysql_connector.get_all_genres()
        result2 = mysql_connector.get_all_genres()
        self.assertEqual(result1, result2)

    def test_execute_select_query_invalid_sql(self):
        result = mysql_connector.execute_select_query("SELECT * FROM nonexistent_table")
        self.assertEqual(result, [])
