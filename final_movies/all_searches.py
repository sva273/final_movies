from typing import Dict, Tuple
from dotenv import load_dotenv
from final_movies.mysql_connector import (
    search_movies,  # Основная функция поиска фильмов
    get_all_genres,  # Получение всех жанров из базы данных
)

# Логирование поискового запроса
from final_movies.log_writer import log_search

# Функция постраничного вывода результатов
from final_movies.formatter import paginate_results, display_ratings_table, display_genre_table

# Загружаем переменные окружения
load_dotenv()

# Словарь с расшифровкой кодов MPAA
available_ratings: Dict[str, str] = {
     "G": "👶 General Audiences – All ages admitted",
    "PG": "👪 Parental Guidance Suggested",
    "PG-13": "⚠️ Parents Strongly Cautioned",
    "R": "🔞 Restricted – Under 17 requires accompanying parent or adult guardian",
    "NC-17": "🚫 Adults Only – No one 17 and under admitted"
}


def get_user_input(prompt: str) -> str:
    """
    Унифицированный ввод от пользователя с обрезкой пробелов.

    :param prompt: Текст запроса
    :return: Строка ввода без пробелов по краям
    """
    return input(prompt).strip()


def select_genre() -> Tuple[int, Tuple[int, int], str]:
    """
    Запрашивает у пользователя выбор жанра из списка доступных жанров.

    Сначала отображает таблицу жанров с их идентификаторами (ID), диапазоном годов выпуска
    и количеством фильмов, используя вспомогательную функцию display_genre_table().
    Затем ожидает корректный ввод от пользователя — ID жанра, присутствующий в таблице.

    После успешного ввода возвращает кортеж, содержащий:
        - идентификатор жанра (genre_id)
        - кортеж из минимального и максимального годов (min_year, max_year)
        - название жанра (genre_name)

    :return: Кортеж вида (genre_id, (min_year, max_year), genre_name)
    :rtype: Tuple[int, Tuple[int, int], str]

    """
    # Получаем список всех жанров из базы данных
    genres = get_all_genres()

    # Формируем и отображаем таблицу жанров, а также получаем вспомогательные данные
    # Возвращаемый словарь: {genre_id: (min_year, max_year, genre_name)}
    genre_data = display_genre_table(genres)  # вынесено всё отображение и подсчёты

    # Извлекаем список допустимых идентификаторов жанров
    valid_ids = genre_data.keys()

    while True:
        # Запрашиваем ID жанра у пользователя
        genre_id_input = get_user_input("Enter genre ID: ")

        # Проверяем, что ввод состоит только из цифр
        if genre_id_input.isdigit():
            genre_id = int(genre_id_input)

            # Проверяем, что введённый ID присутствует среди доступных жанров
            if genre_id in genre_data:
                min_year, max_year, genre_name = genre_data[genre_id]

                # Возвращаем выбранный жанр и соответствующие данные
                return genre_id, (min_year, max_year), genre_name

        # В случае некорректного ввода — уведомляем пользователя и повторяем запрос
        print(
            f"Invalid genre ID. Please enter one of: {', '.join(map(str, valid_ids))}"
        )


def get_year_range(min_year: int, max_year: int) -> Tuple[int, int]:
    """
    Запрашивает у пользователя диапазон лет и проверяет корректность ввода.

    Требует, чтобы оба года были четырёхзначными числами
    и входили в допустимый диапазон min_year - max_year.

    :param min_year: Минимально возможный год
    :param max_year: максимально возможный год
    :return: кортеж (год_начала, год_окончания)
    """
    while True:
        year_from_input = get_user_input(f"Enter start year ({min_year}-{max_year}): ")
        year_to_input = get_user_input(f"Enter end year ({min_year}-{max_year}): ")
        if year_from_input.isdigit() and year_to_input.isdigit():
            year_from = int(year_from_input)
            year_to = int(year_to_input)
            if len(year_from_input) == 4 and len(year_to_input) == 4:
                if min_year <= year_from <= year_to <= max_year:
                    return year_from, year_to
        print("Invalid year range. Try again.")


def search_by_keyword_workflow() -> None:
    """
    Запрашивает ключевое слово у пользователя и выполняет поиск фильмов.

    После поиска записывает запрос и отображает результаты с пагинацией.
    Если ничего не найдено — выводит соответствующее сообщение.
    """
    keyword = get_user_input("Enter keyword to search for movies: ")

    # Проверка: если пользователь не ввёл ничего (или только пробелы), завершаем функцию
    if not keyword:
        print("⚠️ Keyword cannot be empty.")
        return

    # Поиск по ключевому слову
    movies = search_movies(keyword=keyword)

    # Логирование поискового запроса
    log_search("keyword", {"keyword": keyword.lower()}, len(movies))

    if not movies:
        print("🔍 Nothing found for your request.")
        return

    # Отображение результатов с постраничной навигацией
    paginate_results(movies)


def search_by_genre_and_year_workflow() -> None:
    """
    Запрашивает у пользователя жанр и диапазон годов, затем ищет фильмы.

    После поиска записывает параметры и выводит результаты.
    Если ничего не найдено — сообщает об этом пользователю.
    """
    # Выбор жанра
    genre_id, (min_year, max_year), genre_name = select_genre()

    # Выбор диапазона годов в рамках выбранного жанра
    year_from, year_to = get_year_range(min_year, max_year)

    # Поиск фильмов по параметрам
    movies = search_movies(genre_id=genre_id, year_from=year_from, year_to=year_to)

    # Логирование запроса
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

    # Отображение результатов с постраничной навигацией
    paginate_results(movies)


def search_by_rating_workflow() -> None:
    """
    Обрабатывает сценарий поиска фильмов по рейтингу MPAA (например: G, PG, PG-13, R, NC-17).

    Шаги:
    1. Показывает пользователю список доступных рейтингов.
    2. Принимает числовой ввод от пользователя.
    3. Проверяет корректность выбора.
    4. Выполняет поиск фильмов по выбранному рейтингу.
    5. Записывает информацию о поиске.
    6. Показывает результаты поиска (если найдены).

    Возвращает:
        None
    """
    # Отображаем таблицу с возможными рейтингами и получаем соответствие номеров и кодов рейтинга
    index_to_code = display_ratings_table(available_ratings)

    selected_rating = None  # Инициализация переменной

    while True:
        choice = get_user_input("Select a rating by number: ")

        # Разрешаем только целые числа
        if not choice.isdigit():
            print("❌ Only numbers are allowed. Please try again.")
            continue

        index = int(choice)    # Преобразуем ввод в целое число

        # Проверяем, что введённый индекс присутствует в списке доступных рейтингов
        if index in index_to_code:
            selected_rating = index_to_code[index]
            break

        print(f"Invalid selection. Please enter a number between 1 and {len(index_to_code)}.")

    if selected_rating is None:
        print("No valid rating selected. Exiting.")
        return

    # Выполняем поиск фильмов с выбранным рейтингом
    movies = search_movies(rating=selected_rating)

    # Записываем информацию о поиске в лог-файл
    log_search("rating", {"rating": selected_rating}, len(movies))

    if not movies:
        print("🔍 No movies found for the selected rating.")
        return

    # Если фильмы найдены — выводим их с разбивкой на страницы
    paginate_results(movies)