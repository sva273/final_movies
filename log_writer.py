import os
from datetime import datetime, UTC
from typing import Any, Dict

from dotenv import load_dotenv
from pymongo import MongoClient

# Загрузка переменных окружения
load_dotenv()

# Настройка подключения к MongoDB
client = MongoClient(os.getenv("MONGO_URI"), retryWrites=True)
db = client[os.getenv("MONGO_DB")]
collection = db[os.getenv("MONGO_COLLECTION")]


def log_search(search_type: str, params: Dict[str, Any], results_count: int) -> None:
    """
    Сохраняет выполнение поиска в MongoDB.

    :param search_type: Тип поиска (по ключевому слову, по жанру и т.д.)
    :param params: Словарь параметров запроса
    :param results_count: Количество найденных результатов
    """
    log_entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "search_type": search_type,
        "params": params,
        "results_count": results_count,
    }
    try:
        result = collection.insert_one(log_entry)
        print(f"✅ Log entry inserted: {result.inserted_id}")
    except Exception as e:
        print(f"❌ Log insert failed: {e}")
