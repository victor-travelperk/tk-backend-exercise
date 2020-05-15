#!/usr/bin/env sh

echo "Running all tests ..."
docker-compose run app sh -c "python manage.py test"