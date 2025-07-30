import os
from datetime import datetime, UTC
from typing import Any, Dict

from dotenv import load_dotenv
from pymongo import MongoClient

# Загрузка переменных окружения
load_dotenv()

# ========= Настройка подключения к MongoDB ================

# Создаём клиент MongoDB, используя URI из переменных окружения
# retryWrites=True — повторяет запись в случае временных сбоев сети
client = MongoClient(os.getenv("MONGO_URI"), retryWrites=True)

db = client[os.getenv("MONGO_DB")]
collection = db[os.getenv("MONGO_COLLECTION")]


def log_search(search_type: str, params: Dict[str, Any], results_count: int) -> None:
    """
    Сохраняет лог о поисковом запросе в MongoDB.

    :param search_type: Тип выполненного поиска (например, "keyword", "rating", "genre_year")
    :param params: Словарь параметров поиска (в зависимости от типа запроса)
    :param results_count: Количество фильмов, найденных по данному запросу
    """
    log_entry = {
        "timestamp": datetime.now(
            UTC
        ).isoformat(),  # текущая дата/время в формате ISO (UTC)
        "search_type": search_type,  # тип поиска
        "params": params,  # тип поиска
        "results_count": results_count,  # количество найденных результатов
    }

    try:
        # Пытаемся сохранить документ в MongoDB
        result = collection.insert_one(log_entry)
        # Выводим ID созданной записи в случае успеха
        print(f"✅ Log entry inserted: {result.inserted_id}")
    except Exception as e:
        # В случае ошибки сохраняем сообщение в консоль
        print(f"❌ Log insert failed: {e}")
