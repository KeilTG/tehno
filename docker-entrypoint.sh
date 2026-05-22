#!/bin/bash
set -e

echo "Starting FastAPI application..."

# Запуск FastAPI через uvicorn
exec uvicorn main:app --host 0.0.0.0 --port 8000