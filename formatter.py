from typing import List, Dict, Any, Optional, Tuple
from prettytable import PrettyTable
from mysql_connector import get_min_max_years_for_genre, get_genre_movie_count

def paginate_results(
    results: List[Dict[str, Any]],
    page_size: int = 10,
    columns: Optional[List[str]] = None,
) -> None:
    """
    Постраничный вывод результатов поиска через PrettyTable.

    Позволяет пользователю переключаться между страницами через консольные команды:
    - 'n': следующая страница
    - 'p': предыдущая страница
    - 'g <номер>': переход к указанной странице
    - 'q': выход из режима просмотра

    :param results: Список фильмов (каждый — словарь с полями title, release_year, rating и т.п.)
    :param page_size: Количество фильмов, выводимых на одной странице (по умолчанию 10)
    :param columns: Названия колонок таблицы (если не указаны — используются стандартные)
    :return: None
    """
    # Проверка, что входные данные — список
    if not isinstance(results, list):
        print("⚠️ Invalid data passed to paginate_results: expected a list.")
        return

    total_pages = (len(results) + page_size - 1) // page_size
    if total_pages == 0:
        print("⚠️ No data to display.")
        return

    page = 0

    while True:
        # Определение границ текущей страницы
        start = page * page_size
        end = start + page_size
        page_results = results[start:end]

        # Создание таблицы
        table = PrettyTable()
        # Названия колонок: либо пользовательские, либо стандартные
        table.field_names = columns or ["#", "Title", "Release Year", "Rating"]

        # Добавление строк в таблицу с учётом глобального индекса
        for idx, movie in enumerate(page_results, start=1 + start):
            row = [
                idx,
                movie.get("title", "N/A"),
                movie.get("release_year", "N/A"),
                movie.get("rating", "N/A"),
            ]
            table.add_row(row)

        # Вывод информации о текущей странице и самой таблицы
        print(f"\n=== Found {len(results)} movies | Page {page + 1} of {total_pages} ===")
        print(table)
        try:
            command = (
                input("Enter command (n = next, p = prev, g <number> = go to, q = quit): ")
                .strip()
                .lower()
            )
        except KeyboardInterrupt:
            print("\n❌ Interrupted by user. Exiting pagination.")
            break

        # Обработка пользовательского ввода команд управления страницами
        # Если пользователь просто нажал Enter — предупреждаем и продолжаем цикл
        if not command:
            print("⚠️ Please enter a command (n, p, g <number>, or q).")
            continue

        elif command == "n":
            # Следующая страница
            if page + 1 < total_pages:
                page += 1
            else:
                print("✅ Already on the last page.")
        elif command == "p":
            # Предыдущая страница
            if page > 0:
                page -= 1
            else:
                print("✅ Already on the first page.")
        elif command.startswith("g "):
            # Перейти к введенной странице
            try:
                target = int(command.split()[1]) - 1
                if 0 <= target < total_pages:
                    page = target
                else:
                    print("⚠️ Invalid page number.")
            except ValueError:
                print("⚠️ Please enter a valid page number after 'g'.")
        elif command == "q":
            # Завершить просмотр
            break
        else:
            # Неверная команда
            print("⚠️ Invalid command.")

def display_genre_table(genres: List[Dict[str, Any]]) -> Dict[int, Tuple[int, int, str]]:
    """
    Отображает таблицу жанров с количеством фильмов и годами выпуска.
    Также возвращает словарь с подробной информацией по каждому жанру.

    :param genres: Список жанров (каждый жанр — словарь с genre_id и name)
    :return: Словарь: genre_id → (min_year, max_year, name)
    """
    table = PrettyTable(["ID", "Genre", "Years", "Count"])
    genre_data = Dict[int, Tuple[int, int, str]] = {}

    for g in genres:
        genre_id = g["genre_id"]
        name = g["name"]
        min_year, max_year = get_min_max_years_for_genre(genre_id)
        count = get_genre_movie_count(genre_id)
        genre_data[genre_id] = (min_year, max_year, name)
        table.add_row([genre_id, name, f"{min_year}-{max_year}", count])

    print("\n🎬 Available genres:")
    print(table)

    return genre_data


def display_ratings_table(ratings: Dict[str, str]) -> Dict[int, str]:
    """
    Формирует и отображает таблицу MPAA-рейтингов.
    Возвращает словарь: номер строки → код рейтинга (напр. 1 → "G").
    """
    table = PrettyTable(["#", "Code", "Description"])
    index_to_code = {}

    for idx, (code, description) in enumerate(ratings.items(), start=1):
        table.add_row([idx, code, description])
        index_to_code[idx] = code

    print("\n🎞 Available MPAA Ratings:")
    print(table)

    return index_to_code