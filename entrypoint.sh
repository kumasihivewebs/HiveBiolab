#!/bin/sh
set -e

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput

# Start the server
exec "$@"

