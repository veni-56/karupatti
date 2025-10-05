# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps for Pillow/psycopg2 and builds
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy project
COPY django_backend /app/django_backend

# Use the Django backend as the working directory
WORKDIR /app/django_backend

# Expose port (Render sets PORT env)
EXPOSE 8000

# Default command runs gunicorn with our config
CMD ["gunicorn", "karupatti_shop.wsgi:application", "-c", "gunicorn.conf.py"]
