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
        # Тест функции fetch_movies — возврат данных из запроса

        # Настройка mock-курсор
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"title": "Matrix"}]
        mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            mock_cursor
        )

        result = fetch_movies("SELECT * FROM film")
        self.assertEqual(result, [{"title": "Matrix"}])
        mock_cursor.execute.assert_called_once()

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_get_all_genres(self, mock_fetch):
        # Тест получения всех жанров
        get_all_genres.cache_clear()  # Очистка кэша перед тестом

        mock_fetch.return_value = [
            {"genre_id": 1, "name": "Action"},
            {"genre_id": 2, "name": "Drama"},
        ]
        genres = get_all_genres()
        self.assertEqual(
            genres,
            [{"genre_id": 1, "name": "Action"}, {"genre_id": 2, "name": "Drama"}],
        )
        mock_fetch.assert_called_once()

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_get_min_max_years_for_genre(self, mock_fetch):
        # Тест получения минимального и максимального года по жанру

        # Ожидаемый результат
        mock_fetch.return_value = [{"min_year": 1990, "max_year": 2000}]
        result = get_min_max_years_for_genre(1)
        self.assertEqual(result, (1990, 2000))

        # Пустой результат — жанр не найден
        mock_fetch.return_value = []
        result = get_min_max_years_for_genre(999)
        self.assertEqual(result, (None, None))

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_get_genre_movie_count(self, mock_fetch):
        # Тест получения количества фильмов по жанру

        # Есть результат
        mock_fetch.return_value = [{"count": 42}]
        result = get_genre_movie_count(1)
        self.assertEqual(result, 42)

        # Нет результатов
        mock_fetch.return_value = []
        result = get_genre_movie_count(999)
        self.assertEqual(result, 0)

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_search_movies_builds_query(self, mock_fetch):
        # Тест построения SQL-запроса при поиске фильмов
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

        # Проверка, что параметр %inception% был передан в аргументах
        args, kwargs = mock_fetch.call_args
        self.assertIn("%inception%", args[1])

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_search_movies_only_keyword(self, mock_fetch):
        # Тест фильтрации только по ключевому слову
        search_movies(keyword="toy")

        query, params = mock_fetch.call_args[0]
        self.assertIn("LOWER(f.title) LIKE %s", query)
        self.assertNotIn("fc.category_id = %s", query)
        self.assertNotIn("release_year BETWEEN", query)
        self.assertNotIn("f.rating = %s", query)
        self.assertEqual(params, ("%toy%",))

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_search_movies_only_genre(self, mock_fetch):
        # Тест фильтрации только по жанру
        search_movies(genre_id=5)

        query, params = mock_fetch.call_args[0]
        self.assertIn("fc.category_id = %s", query)
        self.assertNotIn("LOWER(f.title) LIKE %s", query)
        self.assertEqual(params, (5,))

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_search_movies_only_rating(self, mock_fetch):
        # Тест фильтрации только по рейтингу
        search_movies(rating="PG")

        query, params = mock_fetch.call_args[0]
        self.assertIn("f.rating = %s", query)
        self.assertEqual(params, ("PG",))

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_search_movies_all_filters(self, mock_fetch):
        # Тест применения всех фильтров сразу
        search_movies(
            keyword="matrix", genre_id=3, year_from=1999, year_to=2003, rating="R"
        )

        query, params = mock_fetch.call_args[0]
        self.assertIn("LOWER(f.title) LIKE %s", query)
        self.assertIn("fc.category_id = %s", query)
        self.assertIn("f.release_year BETWEEN %s AND %s", query)
        self.assertIn("f.rating = %s", query)
        self.assertIn("ORDER BY f.release_year", query)
        self.assertEqual(params, ("%matrix%", 3, 1999, 2003, "R"))

    @patch("final_movies.mysql_connector.fetch_movies")
    def test_search_movies_incomplete_year_range(self, mock_fetch):
        # Тест: передан только один год — фильтр по году не должен применяться
        search_movies(year_from=2000)

        query, params = mock_fetch.call_args[0]
        self.assertNotIn("release_year BETWEEN", query)
        self.assertNotIn(2000, params)


if __name__ == "__main__":
    unittest.main()
