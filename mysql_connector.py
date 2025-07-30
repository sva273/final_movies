import os
import logging
from functools import lru_cache
from typing import Optional, Dict, Any, List, Tuple

# Загрузка переменных окружения
from dotenv import load_dotenv

# Импорт библиотеки для работы с MySQL
import pymysql
import pymysql.cursors


# Настройка базового логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Загружаем переменные окружения из .env
load_dotenv()


def get_mysql_connection() -> pymysql.connections.Connection:
    """
    Создаёт подключение к MySQL с использованием параметров из .env.
    При ошибке подключения выводит сообщение в лог и вызывает исключение.

    :return: Объект подключения к базе данных
    """
    try:
        # Подключение к БД с помощью параметров из окружения
        return pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            cursorclass=pymysql.cursors.DictCursor,  # Результаты будут в виде словарей
            autocommit=True,  # Автоматическая фиксация транзакций
        )
    except pymysql.MySQLError as e:
        logging.error(f"MySQL connection error: {e}")
        raise ConnectionError(f"MySQL connection error: {e}")


# Обёртка для выполнения SQL-запросов с безопасной обработкой ошибок
def fetch_movies(query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
    """
    Универсальный исполнитель SQL-запросов SELECT.
    Выполняет запрос и возвращает результат в виде списка словарей.

    :param query: SQL-запрос
    :param params: параметры запроса (для подстановки)
    :return: список словарей с результатами запроса
    """
    try:
        with get_mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result if isinstance(result, list) else []
    except pymysql.ProgrammingError as e:
        logging.error(f"SQL execution error: {e}")
        return []
    except pymysql.MySQLError as e:
        logging.error(f"MySQL error: {e}")
        return []


@lru_cache(maxsize=1)
def get_all_genres() -> List[Dict[str, Any]]:
    """
    Возвращает список всех жанров, у которых есть хотя бы один фильм.
    Использует кэширование, чтобы не выполнять запрос повторно.

    :return: Список жанров (genre_id и name)
    """
    # noinspection SqlNoDataSourceInspection
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
    Определяет минимальный и максимальный год выпуска фильмов для заданного жанра.

    :param genre_id: ID жанра (category_id)
    :return: кортеж из двух элементов (min_year, max_year), либо (None, None) при отсутствии данных
    """
    # noinspection SqlNoDataSourceInspection
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
    Возвращает количество уникальных фильмов, связанных с указанным жанром.

    :param genre_id: ID жанра
    :return: число фильмов в жанре
    """
    # noinspection SqlNoDataSourceInspection
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
    Выполняет поиск фильмов по одному или нескольким критериям:
    - по ключевому слову в названии
    - по ID жанра
    - по диапазону годов выпуска
    - по рейтингу MPAA.

    Все параметры являются необязательными и могут комбинироваться.

    :param keyword: Часть названия фильма (без учёта регистра)
    :param genre_id: ID жанра
    :param year_from: начальный год
    :param year_to: конечный год
    :param rating: рейтинг (G, PG, PG-13, R, NC-17)
    :return: список фильмов, соответствующих фильтрам
    """
    # noinspection SqlNoDataSourceInspection
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
