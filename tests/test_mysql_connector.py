import unittest
from final_movies import mysql_connector


class TestMySQLConnector(unittest.TestCase):
    def test_get_all_genres_returns_list(self):
        genres = mysql_connector.get_all_genres()
        self.assertIsInstance(genres, list)

    def test_get_min_max_years_for_genre(self):
        min_year, max_year = mysql_connector.get_min_max_years_for_genre(1)
        # Проверяем, что либо оба значения None, либо это int
        self.assertTrue((min_year is None and max_year is None) or (isinstance(min_year, int) and isinstance(max_year, int)))

    def test_search_movies_keyword(self):
        result = mysql_connector.search_movies(keyword="ACADEMY")
        self.assertIsInstance(result, list)
        for movie in result:
            self.assertIn("title", movie)

    def test_get_genre_movie_count(self):
        count = mysql_connector.get_genre_movie_count(1)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

