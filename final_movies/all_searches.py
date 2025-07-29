from typing import Dict, Tuple
from dotenv import load_dotenv
from prettytable import PrettyTable
from final_movies.mysql_connector import (
    search_movies,
    get_min_max_years_for_genre,
    get_all_genres,
    get_genre_movie_count,
)
from .log_writer import log_search
from .formatter import paginate_results

# Загружаем переменные окружения
load_dotenv()

# Словарь с расшифровкой кодов MPAA
available_ratings: Dict[str, str] = {
    "G": "General Audiences – All ages admitted",
    "PG": "Parental Guidance Suggested",
    "PG-13": "Parents Strongly Cautioned",
    "R": "Restricted",
    "NC-17": "Adults Only",
}


def select_genre() -> Tuple[int, Tuple[int, int], str]:
    """
    Выбор жанра пользователем с выводом таблицы через PrettyTable.
    :return: genre_id, genre_name, (min_year, max_year), count
    """
    genres = get_all_genres()
    table = PrettyTable(["ID", "Genre", "Years", "Count"])
    genre_data = {}

    for g in genres:
        genre_id = g["genre_id"]
        name = g["name"]
        min_year, max_year = get_min_max_years_for_genre(genre_id)
        count = get_genre_movie_count(genre_id)
        genre_data[genre_id] = (min_year, max_year, name)
        table.add_row([genre_id, name, f"{min_year}-{max_year}", count])

    print("\n🎬 Available genres:")
    print(table)

    valid_ids = genre_data.keys()

    while True:
        genre_id_input = input("Enter genre ID: ").strip()
        if genre_id_input.isdigit():
            genre_id = int(genre_id_input)
            if genre_id in genre_data:
                min_year, max_year, genre_name = genre_data[genre_id]
                return genre_id, (min_year, max_year), genre_name

        print(
            f"Invalid genre ID. Please enter one of: {', '.join(map(str, valid_ids))}"
        )


def get_year_range(min_year: int, max_year: int) -> Tuple[int, int]:
    """
    Запрашивает у пользователя корректный диапазон годов.
    """
    while True:
        year_from_input = input(f"Enter start year ({min_year}-{max_year}): ").strip()
        year_to_input = input(f"Enter end year ({min_year}-{max_year}): ").strip()
        if year_from_input.isdigit() and year_to_input.isdigit():
            year_from = int(year_from_input)
            year_to = int(year_to_input)
            if len(year_from_input) == 4 and len(year_to_input) == 4:
                if min_year <= year_from <= year_to <= max_year:
                    return year_from, year_to
        print("Invalid year range. Try again.")


def search_by_keyword_workflow() -> None:
    """
    Поиск фильмов по ключевому слову.
    """
    keyword = input("Enter keyword to search for movies: ").strip()
    if not keyword:
        print("⚠️ Keyword cannot be empty.")
        return

    movies = search_movies(keyword=keyword)
    log_search("keyword", {"keyword": keyword.lower()}, len(movies))

    if not movies:
        print("🔍 Nothing found for your request.")
        return

    paginate_results(movies)


def search_by_genre_and_year_workflow() -> None:
    """
    Поиск по жанру и диапазону годов.
    """
    genre_id, (min_year, max_year), genre_name = select_genre()
    year_from, year_to = get_year_range(min_year, max_year)
    movies = search_movies(genre_id=genre_id, year_from=year_from, year_to=year_to)

    log_search(
        "genre_year",
        {
            "genre_name": genre_name,
            "genre_id": genre_id,
            "year_from": year_from,
            "year_to": year_to,
        },
        len(movies),
    )

    if not movies:
        print("🔍 No movies found for this genre and year range.")
        return
    paginate_results(movies)


def search_by_rating_workflow() -> None:
    """
    Поиск фильмов по рейтингу MPAA.
    """
    print("\nAvailable MPAA Ratings:")
    ratings_list = list(available_ratings.items())
    for idx, (code, desc) in enumerate(available_ratings.items(), 1):
        print(f"{idx}. {code} - {desc}")

    while True:
        choice = input("Select a rating by number: ").strip()
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(available_ratings):
                selected_rating = list(available_ratings.keys())[index - 1]
                break

        print(
            f"Invalid selection. Please enter a number between 1 and {len(ratings_list)}."
        )

    movies = search_movies(rating=selected_rating)
    log_search("rating", {"rating": selected_rating}, len(movies))

    if not movies:
        print("🔍 No movies found for the selected rating.")
        return

    paginate_results(movies)
