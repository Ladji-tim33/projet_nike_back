#!/usr/bin/env bash
# Stop the script si une commande échoue
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
