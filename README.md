# Currency service

## Описание

Сервис курса валют, который получает информацию с сайта ЦБ РФ. Хранит историю обмена валют и предлагает ее по REST API. Проект состоит из трех частей:

- приложение на FastAPI, которое отдает всю информацию по курсу валют,
- парсер сайта ЦБ РФ, реализованный при помощи Scrapy,
- база данных, хранящая историю курсов.

Доступна аутентификация пользователей по токену.

## Ключевые технологии и библиотеки:

- [Python](https://www.python.org/);
- [Scrapy](https://www.scrapy.org/)
- [FastAPI](https://fastapi.tiangolo.com/);
- [SQLAlchemy](https://www.sqlalchemy.org/);
- [Uvicorn](https://uvicorn.dev/);
- [PostgreSQL](https://www.postgresql.org/).

## Установка и запуск

Клонируйте репозиторий, создайте виртуальное окружение и установите зависимости:

```bash
git clone https://github.com/DeathPolarizer/higher-web-practice-python-currency.git
cd higer-web-pracice-python-currency
uv venv
. .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows
uv sync
```

Создайте `.env` файл с переменными окружения:

```bash
touch .env
```

Все необходимые для запуска переменные окружения перечислены в файле `.env-example`.

Запуск проекта при помощи Docker:

```bash
docker compose up --build
```

Запуск отдельных частей:

```bash
uv run uvicorn main:app --reload
uv run scrapy crawl cbr
```

## Разработка

Запуск тестов:

```bash
uv run pytest
```

Запуск проверок импортов:

```bash
uv check
```

## API

Документаци API endpoints проекта располагается по адресу после запуска приложения [тут](https://127.0.0.1:8000/docs)

## Автор проекта:

Смирнов Дмитрий - [Github](https://github.com/DeathPolarizer/)
