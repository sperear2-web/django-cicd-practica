# django-cicd-practica

Proyecto Django (app "tareas": gestor simple de tareas) usado como base para la
practica **G003-S09 — Gestion de la construccion y despliegue continuo**
(Gestion de la Configuracion de Software, UNEMI). Implementa un flujo de
integracion y despliegue continuo con **GitHub Actions** y **Docker**.

## Estructura

- `config/` — proyecto Django (settings, urls, wsgi).
- `tareas/` — app funcional (modelo `Tarea`, vistas, templates, tests).
- `requirements.txt` — dependencias.
- `Dockerfile`, `docker-compose.yml` — contenedorizacion (Django + PostgreSQL).
- `.github/workflows/ci.yml` — pipeline de CI/CD.
- `deploy-notes.md` — pasos del despliegue simulado.

## Uso local sin Docker (SQLite)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Uso con Docker (PostgreSQL)

```bash
docker compose up --build
```

La app queda disponible en http://localhost:8000/ y el endpoint de
healthcheck en http://localhost:8000/salud/.
