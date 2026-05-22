# Образ для FastAPI приложения TechnoService
FROM python:3.12-slim

# Не создавать .pyc и буферизовать вывод
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория в контейнере
WORKDIR /app

# Установка системных зависимостей (для asyncpg и psycopg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY . .

# Папка для медиафайлов (если нужна)
RUN mkdir -p /app/media

# Открываем порт
EXPOSE 8000

# Скрипт запуска
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]