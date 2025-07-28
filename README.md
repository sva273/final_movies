## Описание
Интерактивное консольное Python-приложение для поиска фильмов в базе данных (MySQL) с логированием поисковых 
запросов в MongoDB.

Позволяет:
- Искать фильмы по ключевому слову.
- Искать фильмы по жанру и диапазону годов.
- Искать фильмы по рейтингу MPAA.
- Сохранять все поисковые запросы в MongoDB.
- Показывать 5 последних уникальных запросов по названию фильмов.
- Показывать TОР 5 запросов по названию фильмов и по жанру и диапазону годов.
- Показывать 5 последних запросов по рейтингу MPAA

##  Установка
# Клонируй проект:
```bash
git clone <repo_link>
cd final_movies
```

## Установи зависимости:
```bash
pip install -r requirements.txt
```

## Создай файл `.env` в корне и укажи данные подключения или используй шаблон файла `.env.example`:
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_db

MONGO_URI=mongodb://localhost:27017/
MONGO_DB=your_db
MONGO_COLLECTION=your_collection
```

## Запуск
```bash
python main.py
```

##  Используемые технологии
- Python
- MySQL
- MongoDB
- pymysql, pymongo
- python-dotenv
- prettytable (форматирование вывода)

## Структура проекта
```
final_movies
├── main.py
├── mysql_connector.py
├── log_writer.py
├── log_stats.py
├── formatter.py
├── all_searches.py
├── .env
├── requirements.txt
├── .env.example
└── README.md


