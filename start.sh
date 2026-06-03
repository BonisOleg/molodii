#!/usr/bin/env bash
# За замовчуванням manage.py runserver уже без autoreloader (див. apps.devserver).
# Прапорець --noreload лишено явно для сумісності зі старими звичками.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Зупиняю попередні процеси на порті 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
sleep 0.5

export DJANGO_SETTINGS_MODULE=project.settings.develop

if [ -x ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
elif [ -x "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
else
    echo "Не знайдено віртуальне середовище (.venv або venv)."
    exit 1
fi

echo "Запускаю сервер..."
while true; do
    "$PYTHON" manage.py runserver 127.0.0.1:8000 --noreload
    echo "Сервер впав. Перезапуск через 1 сек..."
    sleep 1
done
