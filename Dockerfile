FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=hivebiolab.settings

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# App source
COPY . .

# Entrypoint
RUN chmod +x /app/entrypoint.sh

EXPOSE 8002

ENTRYPOINT ["/app/entrypoint.sh"]

# Production server (better than Daphne for scaling)
CMD ["gunicorn", "hivebiolab.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8002", "--workers", "3", "--timeout", "60"]