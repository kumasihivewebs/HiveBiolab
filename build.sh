#!/bin/bash
set -e

echo "Collecting static files..."
DJANGO_BUILD=1 python manage.py collectstatic --noinput

echo "Build script completed successfully."
