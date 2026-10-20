# Notas de despliegue simulado — django-cicd-practica

Este documento describe el despliegue simulado del proyecto **django-cicd-practica**
dentro del flujo de integracion y despliegue continuo (job `simulate-deploy` en
`.github/workflows/ci.yml`), y como reproducirlo manualmente en una maquina local.

## 1. Contexto

Despues de que el pipeline ejecuta los tests (job `test`) y construye/valida la
imagen Docker (job `build-docker`), el job `simulate-deploy` simula la entrega del
artefacto a un entorno distinto ("carpeta externa"), tal como ocurriria al llevar
una imagen ya probada desde CI hacia un servidor de despliegue.

## 2. Pasos del despliegue simulado (automatizados en CI)

1. **Descargar el proyecto** — se clona el repositorio en una carpeta nueva
   (`despliegue-externo/`), distinta a la usada por los jobs anteriores.
2. **Descargar el artefacto** — se descarga `django-cicd-practica.tar`, la imagen
   Docker generada y publicada como artefacto por el job `build-docker`
   (esto simula bajar la imagen desde un registro como DockerHub).
3. **Cargar la imagen** — `docker load -i django-cicd-practica.tar` registra la
   imagen en el motor Docker del entorno de despliegue.
4. **Ejecutar con Docker Compose** — `docker compose up -d` desde la carpeta
   `despliegue-externo/`, levantando los contenedores `web` (Django + Gunicorn) y
   `db` (PostgreSQL).
5. **Esperar y validar el servicio** — se reintenta `curl http://localhost:8000/salud/`
   hasta obtener respuesta, confirmando que Gunicorn, Django y la conexion a
   PostgreSQL funcionan correctamente dentro del contenedor.
6. **Validar "desde el navegador"** — se solicita la pagina principal (`/`) y el
   endpoint de salud (`/salud/`), devolviendo `HTTP 200` y
   `{"status": "ok", "app": "django-cicd-practica"}` respectivamente.
7. **Apagar el entorno** — `docker compose down -v` libera los contenedores y
   volumenes usados por la simulacion.

## 3. Reproducir el despliegue en una maquina local (fuera de CI)

```bash
# 1. Descargar/clonar el proyecto en una carpeta nueva
git clone https://github.com/sperear2-web/django-cicd-practica despliegue-local
cd despliegue-local

# 2. Construir y ejecutar con Docker Compose
docker compose up --build -d

# 3. Validar desde el navegador
#    Abrir http://localhost:8000/        -> Gestor de Tareas
#    Abrir http://localhost:8000/salud/  -> {"status": "ok", ...}

# 4. Apagar
docker compose down -v
```

## 4. Evidencia

La evidencia de la ejecucion real de este flujo (capturas de pantalla de GitHub
Actions, logs de los tests, del build de Docker y del healthcheck) se encuentra en
la carpeta `evidencia/` y en el documento final entregado para la practica
(PDF "Flujo CI/CD para Django").
