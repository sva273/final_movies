import os
import logging
from datetime import datetime, UTC
from typing import Any, Dict

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# --- Настройка логирования ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# --- Загрузка переменных окружения ---
load_dotenv()

# --- Проверка переменных окружения ---
mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")
mongo_collection = os.getenv("MONGO_COLLECTION")

if not all([mongo_uri, mongo_db, mongo_collection]):
    raise EnvironmentError("❌ One or more MongoDB environment variables are missing.")

# --- Подключение к MongoDB ---
try:
    client = MongoClient(mongo_uri, retryWrites=True)
    db = client[mongo_db]
    collection = db[mongo_collection]
    logger.info("✅ Connected to MongoDB")
except PyMongoError as e:
    logger.error(f"❌ Failed to connect to MongoDB: {e}")
    collection = None  # Позволяет использовать fallback при логировании



def log_search(search_type: str, params: Dict[str, Any], results_count: int) -> None:
    """
    Сохраняет лог о поисковом запросе в MongoDB.

    :param search_type: Тип выполненного поиска (например, "keyword", "rating", "genre_year")
    :param params: Словарь параметров поиска (в зависимости от типа запроса)
    :param results_count: Количество фильмов, найденных по данному запросу
    """
    log_entry = {
        "timestamp": datetime.now(UTC).isoformat(),  # текущий UTC в ISO-формате
        "search_type": search_type,
        "params": params,
        "results_count": results_count,
    }

    if collection is None:
        logger.warning("⚠️ Skipping MongoDB log — no active collection.")
        return

    try:
        collection.insert_one(log_entry)
    except PyMongoError as insert_err:
        logger.error(f"❌ Failed to save log entry: {insert_err}")
