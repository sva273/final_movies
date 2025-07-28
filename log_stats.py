from dotenv import load_dotenv
from log_writer import collection
from mysql_connector import get_all_genres
from all_searches import available_ratings

# Загружаем переменные окружения
load_dotenv()

# Загружаем жанры из базы и создаём отображение genre_id -> name
genres = get_all_genres()
genre_map = {g["genre_id"]: g["name"] for g in genres}


# === Форматирующие функции для вывода ===


def format_keyword_label(d: dict) -> str:
    # Возвращает ключевое слово в нижнем регистре из агрегированного словаря
    return d["keyword"].lower()


def format_genre_year_label(d: dict) -> str:
    # Формирует подпись жанра и диапазона годов для вывода в статистике
    return f"{d['genre_name']} ({d['year_from']}-{d['year_to']})"


# === Универсальный агрегатор ===


def display_aggregate_logs(
    title: str,
    match_filter: dict,
    group_fields: list,
    label_format_func,
    limit: int = 5,
) -> None:
    """
     Обобщённый вывод агрегированных логов (топы по ключевым словам, жанрам и т.д.)

    :param title: Заголовок раздела
    :param match_filter: Фильтр MongoDB ($match)
    :param group_fields: Поля для группировки
    :param label_format_func: Функция форматирования метки
    :param limit: Ограничение на количество результатов
    """
    print(f"\n=== {title} ===")
    try:
        stages = [
            {"$match": match_filter},
            {
                "$group": {
                    "_id": {field: f"$params.{field}" for field in group_fields},
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": limit},
        ]

        # Вывод результата
        for idx, entry in enumerate(collection.aggregate(stages), 1):
            label = label_format_func(entry["_id"])
            count = entry["count"]
            print(f"{idx}. {label}, count: {count}")

    except Exception as e:
        print(f"❌ Error fetching logs: {e}")


# === Специализированные отображения ===


def display_top_searches() -> None:
    """
    Отображает топ 5 запросов: по ключевым словам и по жанрам + годам.
    """
    display_aggregate_logs(
        "Top 5 Keyword Searches",
        {"search_type": "keyword"},
        ["keyword"],
        format_keyword_label,
    )

    display_aggregate_logs(
        "Top 5 Genre + Year Searches",
        {"search_type": "genre_year"},
        ["genre_name", "year_from", "year_to"],
        format_genre_year_label,
    )


def display_last_unique_searches() -> None:
    """
    Отображает 5 последних уникальных поисков (по типу и параметрам).
    """
    print("\n=== Last 5 Unique Searches ===")

    try:
        stages = [
            {
                "$group": {
                    "_id": {"search_type": "$search_type", "params": "$params"},
                    "latest_timestamp": {"$max": "$timestamp"},
                    "results_count": {"$first": "$results_count"},
                }
            },
            {"$sort": {"latest_timestamp": -1}},
            {"$limit": 5},
        ]

        results = list(collection.aggregate(stages))

        for idx, entry in enumerate(results, 1):
            search_type = entry["_id"]["search_type"]
            params = entry["_id"]["params"]
            results_count = entry["results_count"]

            if search_type == "keyword":
                print(f"{idx}. keyword | {params['keyword']}, {results_count} results")

            elif search_type == "genre_year":
                print(
                    f"{idx}. genre_year | {params['genre_name']}, {params['year_from']}-{params['year_to']},"
                    f" {results_count} results"
                )

            elif search_type == "rating":
                rating_code = params["rating"]
                rating_name = available_ratings.get(rating_code, rating_code)
                print(f"{idx}. rating | {rating_name}, {results_count} results")

            else:
                print(f"{idx}. {search_type} | {params}, {results_count} results")

    except Exception as e:
        print(f"❌ Error fetching logs: {e}")


def display_last_rating_searches() -> None:
    """
    Показывает 5 последних поисков по рейтингу MPAA.
    """
    print("\n=== Last 5 Rating Searches ===")
    try:
        cursor = (
            collection.find({"search_type": "rating"}).sort("timestamp", -1).limit(5)
        )

        for idx, doc in enumerate(cursor, 1):
            rating_code = doc["params"]["rating"]
            rating_name = available_ratings.get(rating_code, rating_code)
            results_count = doc["results_count"]
            print(f"{idx}. Rating: {rating_name} | {results_count} results")

    except Exception as e:
        print(f"❌ Error fetching logs: {e}")
