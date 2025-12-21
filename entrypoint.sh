#!/bin/sh
echo "⏳ PostgreSQL kutilyapti..."
while ! nc -z db 5432; do
  sleep 0.2
done

echo "✅ PostgreSQL tayyor"

python manage.py migrate
python manage.py collectstatic --noinput

exec python manage.py runserver 0.0.0.0:8000
