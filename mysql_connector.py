import os
import logging
from functools import lru_cache
from typing import Optional, Dict, Any, List, Tuple

# Работа с переменными окружения
from dotenv import load_dotenv

# Работа с MySQL
import pymysql
import pymysql.cursors


# Настройка логирования (уровень INFO)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Загружаем переменные окружения из .env
load_dotenv()


def get_mysql_connection() -> pymysql.connections.Connection:
    """
    Создает и возвращает подключение к MySQL с параметрами из .env.
    Завершает выполнение программы при ошибке подключения.
    """
    try:
        # Подключение к БД с помощью параметров из окружения
        return pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
    except pymysql.MySQLError as e:
        logging.error(f"MySQL connection error: {e}")
        raise ConnectionError(f"MySQL connection error: {e}")


# Обёртка для выполнения SQL-запросов с безопасной обработкой ошибок
def fetch_movies(query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
    """
    Выполняет SQL-запрос.

    :param query: Строка запроса SQL
    :param params: параметры запроса
    :return: список результатов
    """
    try:
        with get_mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    except pymysql.ProgrammingError as e:
        logging.error(f"SQL execution error: {e}")
        return []
    except pymysql.MySQLError as e:
        logging.error(f"MySQL error: {e}")
        return []


@lru_cache(maxsize=1)
def get_all_genres() -> List[Dict[str, Any]]:
    """
    Получение жанров, для которых есть хотя бы один фильм.
    """
    query = """
        SELECT c.category_id AS genre_id, c.name
        FROM category c
        WHERE EXISTS (
            SELECT 1
            FROM film_category fc
            WHERE fc.category_id = c.category_id
        )
        ORDER BY c.name;
    """
    return fetch_movies(query)


def get_min_max_years_for_genre(genre_id: int) -> Tuple[Optional[int], Optional[int]]:
    """
    Возвращает кортеж (минимальный год, максимальный год) выпуска фильмов для жанра.
    При отсутствии данных возвращает (None, None).
    """
    query = """
        SELECT MIN(f.release_year) AS min_year, MAX(f.release_year) AS max_year
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        WHERE fc.category_id = %s
    """
    result = fetch_movies(query, (genre_id,))
    if result:
        return result[0]["min_year"], result[0]["max_year"]
    return None, None


def get_genre_movie_count(genre_id: int) -> int:
    """
    Возвращает количество фильмов в указанном жанре.
    """
    query = """
        SELECT COUNT(DISTINCT f.film_id) AS count
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        WHERE fc.category_id = %s
    """
    result = fetch_movies(query, (genre_id,))
    if result:
        return result[0]["count"]
    return 0


def search_movies(
    keyword: Optional[str] = None,
    genre_id: Optional[int] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    rating: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Осуществляет поиск фильмов по переданным параметрам:
    - keyword: часть названия фильма.
    - genre_id: ID жанра.
    - year_from, year_to: диапазон годов выпуска.
    - rating: рейтинг фильма.

    Возвращает список найденных фильмов или пустой список при ошибке.
    """
    query = """
        SELECT DISTINCT f.title, f.release_year, f.rating
        FROM film f
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        WHERE 1=1
    """
    params = []

    # Фильтр по ключевому слову в названии
    if keyword:
        query += " AND LOWER(f.title) LIKE %s"
        params.append(f"%{keyword.lower()}%")

    # Фильтр по жанру (category_id)
    if genre_id:
        query += " AND fc.category_id = %s"
        params.append(genre_id)

    # Фильтрация по диапазону лет
    if year_from is not None and year_to is not None:
        query += " AND f.release_year BETWEEN %s AND %s"
        params.extend([year_from, year_to])

    # Фильтр по рейтингу
    if rating:
        query += " AND f.rating = %s"
        params.append(rating)

    # Сортировка результатов
    query += " ORDER BY f.release_year, f.title"

    return fetch_movies(query, tuple(params))
