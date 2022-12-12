# Проектная работа 4 спринта

Ссылка на проект - https://github.com/valerycode/Async_API_sprint_1/

# Описание проекта
Два микросервиса для онлайн кинотеатра:
1. ETL по выгрузке данных из Postgres в Elasticsearch.
2. API для онлайн кинотеатра, где можно получить данные по кинопроизведениям, их жанрам, актерам, сценаристам и режиссерам.

# Документация API
OpenAPI - http://localhost:8000/api/openapi

# Технологии
- Код приложения на Python + FastAPI.
- Приложение запускается под управлением сервера ASGI(uvicorn).
- База данных - PostgresSQL.
- Хранилище – ElasticSearch.
- Кеширование данных – redis cluster.
- Запуск приложения через Docker Compose.

# Как развернуть проект
Сделать fork проекта в свой аккаунт

Скачать репозиторий, перейти в директорию с проектом
```
git clone git@github.com:ваш-логин/foodgram-project-react.git

```
```
cd /<путь-до-директории>/
```

Создать виртуальное окружение, активировать его
```
python3 -m venv venv
. venv/bin/activate
```

Установить зависимости
```
python -m pip install -r requirements.txt
```

Добавить свои данные для переменных в secrets
В файл .env в директории проекта:
```
REDIS_HOST
REDIS_PORT
ELASTIC_HOST
ELASTIC_PORT
ELASTIC_USER
ELASTIC_PASSWORD
```

В файл .env в модуле etl:
```
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST 
DB_PORT
DB_OPTIONS
ELASTIC_SERVER
```

Запуск приложения осуществляется командой:
```
docker-compose up --build -d
```
