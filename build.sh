#!/bin/bash
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build script completed successfully."
