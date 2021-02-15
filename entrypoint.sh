#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for Postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Applying database migrations"
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files"
python manage.py collectstatic --noinput --clear

exec "$@"