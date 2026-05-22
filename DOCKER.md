# Запуск TechnoService в Docker

## Архитектура

- **db** — контейнер PostgreSQL 16 (данные в томе `postgres_data`)
- **web** — контейнер Django + Gunicorn (код и приложение)
- **media_data** — отдельный том для загрузок (фото товаров, подписок)

## Быстрый старт

```bash
# 1. Создать .env из примера
cp .env.example .env

# 2. Заполнить пароли в .env (POSTGRES_PASSWORD, DJANGO_SECRET_KEY)

# 3. Собрать и запустить
docker compose up -d --build

# 4. Создать суперпользователя для админки
docker compose exec web python manage.py createsuperuser
```

Приложение: http://localhost:8000  
Админка: http://localhost:8000/admin/

## Команды

```bash
# Логи
docker compose logs -f web

# Остановка
docker compose down

# Остановка с удалением данных (БД, медиа)
docker compose down -v
```

## Миграция данных с SQLite

Если уже есть `db.sqlite3`:

```bash
# 1. Экспорт данных (на хосте, без Docker)
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission -o backup.json

# 2. Запустить Docker
docker compose up -d --build
docker compose exec web python manage.py migrate

# 3. Загрузить данные
docker compose exec web python manage.py loaddata backup.json
```

(Файл `backup.json` должен быть в проекте или скопирован в контейнер.)
