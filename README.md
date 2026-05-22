## TechnoService

Django‑приложение с PostgreSQL, упакованное в Docker.

### Требования

- Docker / Docker Desktop (с Docker Compose)
- Для Windows рекомендуется WSL2 (Ubuntu)

### Запуск в Docker

1. **Клонировать репозиторий**

   ```bash
   git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
   cd TechnoService/TechnoService
   ```

2. **Создать `.env` из примера и заполнить**

   ```bash
   cp .env.example .env
   ```

   В файле `.env` задать:

   - `DJANGO_SECRET_KEY` — длинный случайный ключ (минимум 50 символов)
   - `DEBUG` — `False` для продакшена или `True` для локальной разработки
   - `ALLOWED_HOSTS` — `localhost,127.0.0.1` или нужные хосты
   - `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — параметры БД

3. **Собрать и запустить контейнеры**

   ```bash
   docker compose up -d --build
   ```

   Будут запущены:

   - `db` — PostgreSQL 16
   - `web` — Django + Gunicorn

4. **Применить миграции (на всякий случай)**

   ```bash
   docker compose exec web python manage.py migrate
   ```

5. **Создать суперпользователя**

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. **Открыть сайт**

   - Приложение: `http://localhost:8000`
   - Админка: `http://localhost:8000/admin/`

### Полезные команды

- **Статус контейнеров**

  ```bash
  docker compose ps
  ```

- **Логи приложения**

  ```bash
  docker compose logs -f web
  ```

- **Остановка**

  ```bash
  docker compose down
  ```

- **Полная остановка с удалением данных (БД и медиа)**

  ```bash
  docker compose down -v
  ```

### Безопасность

- Файл `.env` уже добавлен в `.gitignore` и **не должен** коммититься.
- В репозитории хранится только `.env.example` без реальных паролей и секретов.

