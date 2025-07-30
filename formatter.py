from typing import List, Dict, Any, Optional
from prettytable import PrettyTable


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

    :param results: Список словарей с результатами.
    :param page_size: Количество строк на странице.
    :param columns: Пользовательские заголовки таблицы (по умолчанию стандартные).
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

        command = (
            input("Enter command (n = next, p = prev, g <number> = go to, q = quit): ")
            .strip()
            .lower()
        )

        # Обработка пользовательского ввода команд управления страницами
        if command == "n":
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


