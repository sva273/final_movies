import unittest
from unittest.mock import patch
from final_movies import formatter
import io
import contextlib


class TestFormatter(unittest.TestCase):

    def test_print_pretty_table(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            formatter.print_pretty_table(["Col1"], [[1]])
        output = f.getvalue()
        self.assertIn("Col1", output)
        self.assertIn("1", output)

    @patch("builtins.input", side_effect=["q"])
    def test_paginate_results_quit_immediately(self, mock_input):
        data = [{"title": "Movie1", "release_year": 2000, "rating": "PG"}]
        formatter.paginate_results(data, page_size=1)
        # Проверяем, что без ошибок завершается сразу

    def test_display_genre_table(self):
        formatter.get_min_max_years_for_genre = lambda genre_id: (1990, 2000)
        formatter.get_genre_movie_count = lambda genre_id: 5

        genres = [{"genre_id": 1, "name": "Action"}]
        result = formatter.display_genre_table(genres)
        self.assertIn(1, result)

    def test_display_ratings_table(self):
        ratings = {"G": "General Audience"}
        result = formatter.display_ratings_table(ratings)
        self.assertIn(1, result)
        self.assertEqual(result[1], "G")
