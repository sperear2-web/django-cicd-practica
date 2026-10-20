# Dockerfile - django-cicd-practica
# Basado en python:3.10 segun lo pedido en la guia de practica (Sesion 2)

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema necesarias para psycopg2 (cliente PostgreSQL)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalacion de dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Codigo del proyecto
COPY . .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
