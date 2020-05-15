#!/usr/bin/env sh

# Create new migrations for any app that requires it
docker-compose run app sh -c "python manage.py makemigrations"