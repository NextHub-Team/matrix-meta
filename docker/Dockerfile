FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Poetry and Django
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 2.0.1
ENV PATH="/root/.local/bin:$PATH"

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --only main

# Copy the Django project
COPY . .

# Expose the port the Django app runs on
EXPOSE 8000


# Wait for PostgreSQL to be ready (you can adjust the host and port as needed)
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd
COPY docker/wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Add entrypoint script to handle migrations
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Default command to run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
