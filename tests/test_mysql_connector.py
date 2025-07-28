import unittest
from unittest.mock import patch, MagicMock
from final_movies.mysql_connector import (
    fetch_movies,
    get_all_genres,
    get_min_max_years_for_genre,
    get_genre_movie_count,
    search_movies,
)


class TestMySQLConnector(unittest.TestCase):

    @patch("final_movies.mysql_connector.get_mysql_connection")
    def test_fetch_movies_returns_data(self, mock_conn):
        # Настройка mock-курсор
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"title": "Matrix"}]
        mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        result = fetch_movies("SELECT * FROM film")
        self.assertEqual(result, [{"title": "Matrix"}])
        mock_cursor.execute.assert_called_once()

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_get_all_genres(self, mock_fetch):
        get_all_genres.cache_clear()  # Сброс кеша перед тестом

        mock_fetch.return_value = [
            {"genre_id": 1, "name": "Action"},
            {"genre_id": 2, "name": "Drama"}
        ]
        genres = get_all_genres()
        self.assertEqual(genres, [
            {"genre_id": 1, "name": "Action"},
            {"genre_id": 2, "name": "Drama"}
        ])
        mock_fetch.assert_called_once()

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_get_min_max_years_for_genre(self, mock_fetch):
        mock_fetch.return_value = [{"min_year": 1990, "max_year": 2000}]
        result = get_min_max_years_for_genre(1)
        self.assertEqual(result, (1990, 2000))

        # Пустой результат
        mock_fetch.return_value = []
        result = get_min_max_years_for_genre(999)
        self.assertEqual(result, (None, None))

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_get_genre_movie_count(self, mock_fetch):
        mock_fetch.return_value = [{"count": 42}]
        result = get_genre_movie_count(1)
        self.assertEqual(result, 42)

        mock_fetch.return_value = []
        result = get_genre_movie_count(999)
        self.assertEqual(result, 0)

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_search_movies_builds_query(self, mock_fetch):
        mock_fetch.return_value = [
            {"title": "Inception", "release_year": 2010, "rating": "PG-13"}
        ]
        result = search_movies(
            keyword="inception",
            genre_id=1,
            year_from=2000,
            year_to=2020,
            rating="PG-13",
        )
        self.assertEqual(result[0]["title"], "Inception")
        mock_fetch.assert_called_once()
        args, kwargs = mock_fetch.call_args
        self.assertIn("%inception%", args[1])  # параметры для LIKE


if __name__ == "__main__":
    unittest.main()