from typing import List, Dict, Any, Optional, Tuple
from prettytable import PrettyTable
from final_movies.mysql_connector import get_min_max_years_for_genre, get_genre_movie_count


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
    # Проверка, что пришёл список — если нет, выводим предупреждение и выходим
    if not isinstance(results, list):
        print("⚠️ Invalid data passed to paginate_results: expected a list.")
        return

    # Вычисляем количество страниц, округляя вверх
    total_pages = (len(results) + page_size - 1) // page_size
    if total_pages == 0:
        print("⚠️ No data to display.")
        return

    page = 0  # Начинаем с первой страницы (индекс 0)

    while True:
        # Определяем срез списка для текущей страницы
        start = page * page_size
        end = start + page_size
        page_results = results[start:end]

        # Создаём объект PrettyTable и задаём заголовки колонок
        table = PrettyTable()
        table.field_names = columns or ["#", "Title", "Release Year", "Rating"]

        # Добавляем в таблицу фильмы текущей страницы с глобальным номером
        for idx, movie in enumerate(page_results, start=1 + start):
            row = [
                idx,  # Номер фильма в общем списке
                movie.get("title", "N/A"),  # Название фильма или "N/A", если нет
                movie.get("release_year", "N/A"),  # Год выпуска или "N/A"
                movie.get("rating", "N/A"),  # Рейтинг или "N/A"
            ]
            table.add_row(row)

        # Выводим информацию о количестве фильмов, текущей странице и таблицу
        print(
            f"\n=== Found {len(results)} movies | Page {page + 1} of {total_pages} ==="
        )
        print(table)

        # Запрашиваем команду у пользователя
        command = (
            input(
                "Enter command (n = next, p = prev, g <number> = go to, q = quit): "
            )
            .strip()
            .lower()
        )

        if not command:
            # Если пользователь нажал Enter без ввода — предупреждаем
            print("⚠️ Please enter a command (n, p, g <number>, or q).")
            continue

        # Обработка команд переключения страниц
        if command == "n":
            if page + 1 < total_pages:
                page += 1
            else:
                print("✅ Already on the last page.")
        elif command == "p":
            if page > 0:
                page -= 1
            else:
                print("✅ Already on the first page.")
        elif command.startswith("g "):
            try:
                target = int(command.split()[1]) - 1  # Переводим к индексу страницы
                if 0 <= target < total_pages:
                    page = target  # Переход на указанную страницу
                else:
                    print(f"⚠️ Page number must be between 1 and {total_pages}.")
            except ValueError:
                print("⚠️ Please enter a valid page number after 'g'.")
        elif command == "q":
            break  # Выход из просмотра
        else:
            print("⚠️ Invalid command.")


def print_pretty_table(
    headers: List[str], rows: List[List[Any]], title: str = ""
) -> None:
    """
    Универсальная функция вывода таблицы с заголовком.

    :param headers: Список заголовков столбцов.
    :param rows: Список строк, каждая — список значений.
    :param title: Заголовок таблицы (необязательно).
    """
    if title:
        print(f"\n{title}")  # Печать заголовка, если он задан
    table = PrettyTable(headers)  # Создаём таблицу с заголовками
    for row in rows:
        table.add_row(row)  # Добавляем все строки
    print(table)  # Выводим таблицу


def display_genre_table(
    genres: List[Dict[str, Any]],
) -> Dict[int, Tuple[int, int, str]]:
    """
    Отображает таблицу жанров с количеством фильмов и годами выпуска.
    Также возвращает словарь с подробной информацией по каждому жанру.

    :param genres: Список жанров (каждый жанр — словарь с genre_id и name)
    :return: Словарь: genre_id → (min_year, max_year, name)
    """
    genre_data: Dict[int, Tuple[int, int, str]] = (
        {}
    )  # Словарь для хранения данных о жанрах
    rows = []  # Пустой список строк для таблицы

    for g in genres:
        genre_id = g["genre_id"]  # ID жанра
        name = g["name"]  # Название жанра
        # Получаем минимальный и максимальный год выпуска фильмов данного жанра
        min_year, max_year = get_min_max_years_for_genre(genre_id)
        # Получаем количество фильмов в данном жанре
        count = get_genre_movie_count(genre_id)
        genre_data[genre_id] = (min_year, max_year, name)  # Сохраняем в словарь
        # Формируем строку таблицы с жанром, годами и количеством фильмов
        rows.append([genre_id, name, f"{min_year}-{max_year}", count])

    # Выводим таблицу жанров с заголовком
    print_pretty_table(
        ["ID", "Genre", "Years", "Count"], rows, title="🎬 Available genres:"
    )
    return genre_data  # Возвращаем словарь для дальнейшего использования


def display_ratings_table(ratings: Dict[str, str]) -> Dict[int, str]:
    """
    Формирует и отображает таблицу MPAA-рейтингов.
    Возвращает словарь: номер строки → код рейтинга (напр. 1 → "G").
    """
    index_to_code = {}
    table = PrettyTable()
    # Подменяем заголовок Description вручную центрированным вариантом
    desc_header = "Description"
    desc_width = max(len(desc_header), max(len(d) for d in ratings.values()))
    centered_desc = desc_header.center(desc_width)

    table.field_names = ["№", "Code", centered_desc]

    # Центр для Code и №, левый край для описания
    table.align["№"] = "c"
    table.align["Code"] = "c"
    table.align[centered_desc] = "l"  # Содержимое описания по левому краю

    for idx, (code, description) in enumerate(ratings.items(), start=1):
        table.add_row([idx, code, description])
        index_to_code[idx] = code

    print("🎞 Available MPAA Ratings:")
    print(table)
    return index_to_code
