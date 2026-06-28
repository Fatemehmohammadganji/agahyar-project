FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install project dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD uv run python manage.py migrate && uv run python manage.py runserver 0.0.0.0:8000
