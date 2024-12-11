#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run migrations
python manage.py migrate

# Start the Django development server
exec python manage.py runserver 0.0.0.0:8000
