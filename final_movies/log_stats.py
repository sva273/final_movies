# Импорт библиотек и модулей
from dotenv import load_dotenv  # Для загрузки переменных окружения из .env-файла
from final_movies.log_writer import collection  # MongoDB-коллекция для хранения логов поиска
from final_movies.mysql_connector import get_all_genres  # Функция для получения жанров из базы MySQL
from final_movies.all_searches import available_ratings  # Словарь с расшифровкой MPAA рейтингов

# Загружаем переменные окружения
load_dotenv()

# Загружаем жанры из базы и создаём отображение genre_id -> name
genres = get_all_genres()
genre_map = {g["genre_id"]: g["name"] for g in genres}


def format_search_label(search_type: str, params: dict) -> str:
    """Формирует строку для отображения запроса в логах в зависимости от типа поиска.

    :param search_type: Тип запроса (keyword, genre_year, rating и т.д.)
    :param params: Словарь параметров, переданных при поиске
    :return: Строковое представление запроса (для вывода пользователю)
    """
    if search_type == "keyword":
        return f"Keyword: {params['keyword'].lower()}"
    elif search_type == "genre_year":
        return (
            f"Genre: {params['genre_name']} ({params['year_from']}-{params['year_to']})"
        )
    elif search_type == "rating":
        rating_code = params.get("rating")
        rating_name = available_ratings.get(rating_code, rating_code)
        return f"Rating: {rating_name}"
    else:
        return f"{search_type}: {params}"


def display_top_searches(limit: int = 5) -> None:
    """
    Выводит ТОП самых популярных поисковых запросов, независимо от их типа.

    Группирует по типу и параметрам поиска, сортирует по количеству запросов
    и отображает ограниченное число самых частых записей.

    :param limit: Максимальное количество записей для отображения
    """
    print("\n=== Top Popular Searches (All Types) ===")

    try:
        # MongoDB aggregation stage:
        # 1. Группировка по search_type и параметрам запроса
        # 2. Подсчёт количества повторений
        # 3. Сортировка по убыванию
        # 4. Ограничение количества результатов
        stage = [
            {
                "$group": {
                    "_id": {"search_type": "$search_type", "params": "$params"},
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": limit},
        ]

        results = collection.aggregate(stage)

        # Вывод результатов в консоль
        for idx, entry in enumerate(results, 1):
            search_type = entry["_id"]["search_type"]
            params = entry["_id"]["params"]
            count = entry["count"]
            label = format_search_label(search_type, params)
            print(f"{idx}. {label}, count: {count}")

    except Exception as e:
        print(f"❌ Error fetching logs: {e}")


def display_last_unique_searches(limit: int = 5) -> None:
    """
    Показывает последние уникальные поисковые запросы по типу и параметрам.

    Каждая уникальная комбинация search_type + параметры отображается
    с датой последнего запроса и количеством результатов.

    :param limit: Максимальное количество уникальных запросов для отображения
    """
    print("\n=== Last Unique Searches ===")

    try:
        # Aggregation stage:
        # 1. Группировка по типу и параметрам запроса
        # 2. Получение последнего timestamp и первого количества результатов
        # 3. Сортировка по дате (timestamp)
        # 4. Лимитирование количества записей
        stage = [
            {
                "$group": {
                    "_id": {"search_type": "$search_type", "params": "$params"},
                    "latest_timestamp": {"$max": "$timestamp"},
                    "results_count": {"$first": "$results_count"},
                }
            },
            {"$sort": {"latest_timestamp": -1}},
            {"$limit": limit},
        ]

        results = collection.aggregate(stage)

        # Вывод уникальных запросов
        for idx, entry in enumerate(results, 1):
            search_type = entry["_id"]["search_type"]
            params = entry["_id"]["params"]
            results_count = entry["results_count"]
            label = format_search_label(search_type, params)
            print(f"{idx}. {label}, {results_count} results")

    except Exception as e:
        print(f"❌ Error fetching logs: {e}")
