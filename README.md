## Описание
Интерактивное консольное Python-приложение для поиска фильмов в базе данных (MySQL) с логированием поисковых 
запросов в MongoDB.

Позволяет:
- Искать фильмы по ключевому слову.
- Искать фильмы по жанру и диапазону годов.
- Искать фильмы по рейтингу MPAA.
- Сохранять все поисковые запросы в MongoDB.
- Показывать TОР 5 популярных запросов.
- Показывать 5 последних уникальных запросов.


##  Установка
# Клонируй проект:
```bash
git clone https://github.com/sva273/final_movies.git
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
├── tests                      # Папка с тестами.
│   ├── __init__.py 
│   ├── test_log_writer.py     # Тесты для логирования запросов.
│   ├── test_log_stats.py      # Тесты для статистики логов.
│   ├── test_mysql_connector.py # Тесты для MySQL соединений.
│   ├── test_all_searches.py   # Тесты для поиска фильмов.
│   ├── test_main.py           # Тесты для menu.
│   └── test_formatter.py    # Тесты по форматированию таблиц.
├── final_movies              
│   ├── __init__.py 
│   ├── log_writer.py     
│   ├── log_stats.py      
│   ├── mysql_connector.py 
│   ├── all_searches.py  
│   ├── main.py    
│   └── formatter.py    
├── .env
├── requirements.txt
├── .env.example
└── README.md


