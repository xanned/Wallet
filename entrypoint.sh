#!/bin/sh

until cd /app/
do
    echo "Waiting for server volume..."
done

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput
python manage.py createsuperuser --username=admin --email=admin@example.com --noinput
gunicorn --bind 0.0.0.0:8000 e_wallet.wsgi -w 4