#!/bin/bash

# Wait for PostgreSQL to be ready
wait-for-it $POSTGRES_HOST:$POSTGRES_PORT -- echo "PostgreSQL is up and running"

# Run Django database migrations
python manage.py migrate

# Run the passed command
exec "$@"

