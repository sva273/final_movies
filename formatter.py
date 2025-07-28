from typing import List, Dict, Any, Optional
from prettytable import PrettyTable


def paginate_results(
    results: List[Dict[str, Any]],
    page_size: int = 10,
    columns: Optional[List[str]] = None,
) -> None:
    """
    Постраничный вывод результатов поиска через PrettyTable.

    :param results: Список словарей с результатами.
    :param page_size: Количество строк на странице.
    :param columns: Пользовательские заголовки таблицы (по умолчанию стандартные).
    """
    if not isinstance(results, list):
        print("⚠️ Invalid data passed to paginate_results: expected a list.")
        return

    total_pages = (len(results) + page_size - 1) // page_size
    if total_pages == 0:
        print("⚠️ No data to display.")
        return

    page = 0

    while True:
        start = page * page_size
        end = start + page_size
        page_results = results[start:end]

        table = PrettyTable()
        table.field_names = columns or ["#", "Title", "Release Year", "Rating"]

        for idx, movie in enumerate(page_results, start=1 + start):
            row = [
                idx,
                movie.get("title", "N/A"),
                movie.get("release_year", "N/A"),
                movie.get("rating", "N/A"),
            ]
            table.add_row(row)

        print(
            f"\n=== Found {len(results)} movies | Page {page + 1} of {total_pages} ==="
        )
        print(table)

        command = (
            input("Enter command (n = next, p = prev, g <number> = go to, q = quit): ")
            .strip()
            .lower()
        )

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
                target = int(command.split()[1]) - 1
                if 0 <= target < total_pages:
                    page = target
                else:
                    print("⚠️ Invalid page number.")
            except ValueError:
                print("⚠️ Please enter a valid page number after 'g'.")
        elif command == "q":
            break
        else:
            print("⚠️ Invalid command.")


