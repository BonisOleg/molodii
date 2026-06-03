#!/usr/bin/env bash
# Build step for Render (і сумісних PaaS): залежності, статика, міграції.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_demo
