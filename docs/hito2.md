# Documentación del hito 2

Para este hito, cada microservicio se ha empaquetado en una imagen Docker independiente, además, el sistema completo se levanta en local con un solo comando y un se ha creado un flujo de CI que válida el código y publica las imagenes en GitHub Container Registry (GHCR).

![CI](https://github.com/albaayala/CC-Practicas/actions/workflows/ci.yml/badge.svg)

## Estado de la implementación
| Componente | Estado |
|---|---|
| Servicio de Login (registro de empresas y login con JWT) | Implementado y probado |
| Servicio de Tareas (crear y listar las tareas +  validación de solapamiento) | Implementado y probado |
| Servicio de Estadisiticas (resumen y receptción de eventos) | Implementado y probado |
| Dockerflie por servicio | Implementado |
| `compose.yaml` con 3 sevicios y 3 base de datos | Implementado |
| CI: linters, pruebas y publicacione en GHCR | Implementado |
| Api Gateway, broker de mensajes y Redis | Aún sin implementar |

De esta forma, este hito implementoa los tres microservicios con  sus bases de datos, el resto de piezas quedarán para incorporar en los siguientes hitos.

## Arrancar el entorno local

Requisitos: Docker y Docker Compose.

1. Copia el archivo de ejemplo y rellénelo:
```bash
cp .env.example .env
```
2. Genera un valor aleatorio para cada variable:
```bash
python3 -c "import secrets; print(secrets.token_hex(16))"
```
| Varaibale | Uso |
| --- | --- |
| `JWT_SECRET` | Clave con la que el servio Login firma los tokens |
| `LOGIN_DB_PASSWORD` | Contraseña de la base de datos de Login |
| `TAREAS_DB_PASSWORD` | Contraseña de la base de datos de Tareas |
| `ESTADISTICAS_DB_PASSWORD` | Contraseña de la base de datos de Estadísticas |

3. Levanta el sistema:
```bash
docker compose up --build
```
| Servicio | Dirección | Documentación |
|---|---|---|
| Login | http://localhost:8000 | http://localhost:8000/docs |
| Tareas | http://localhost:8001 | http://localhost:8001/docs |
| Estadísticas | http://localhost:8002 | http://localhost:8002/docs |

Actualmente, no se cuenta con un frontend, por eso se usa que nos da fastApi.

4. Para el sistema
   -  Conservar los datos: `docker compose down`
   -  Borrar los volumenes: `docker compose down -v`

## Imagenes Docker

Cada servicio tiene su propio `Dockerfile`y `.dockerignore`en `services/<servicios>/.`. Las decisiones comunes son:
- **Construcción multietapa.** Una primera etapa instala las dependencias, dejando en la imagen final solo con las librerias ya isntaladas y el código , sin `pip` ni caché.
-  **Imagen base `python:3.12-slim`.** Es la misma versión de Python que se usa en el desarrollo, mucho más ligera que la imagen completa y más fiabe que `alpine`.
-  **Usuario sin privilegios.** El contenendor se ejecuta  con un usuario `app`de UID/GID `10001`, un identificador númeroco fijo que no se identifica como root. El cófigo pertenence a ese usuario.
- **Optimización de la caché de capas.** Primero se copia `requirements.txt` y se instalan las dependencias, y el código se copia al final, de esta forma, un cambio en el código no reinstala las librerías.
- **Dependencias con versión fijada.** Cada `requirements.txt` fija versiones exactas, de modo que la imagen es reproducible. Las herramientas de desarrollo (`pytest`, `httpx`, `ruff`) están separadas en `requirements-dev.txt` y no entran en la imagen.
- **`.dockerignore`.** Excluye `.env`, `.venv`, bases de datos locales, pruebas y cachés, para que ningún secreto ni archivo innecesario llegue a la imagen.
- **Puerto expuesto.** Todos los servicios escuchan en el 8000 dentro de su contenedor (`EXPOSE 8000`, con `uvicorn` en `0.0.0.0`). El `compose.yaml` los publica en puertos distintos del anfitrión.

Los Dockerfile se validan con [Hadolint](https://github.com/hadolint/hadolint) y no producen ningún aviso.

## Orquestación con Docker Compose

En el archivo `compose.yaml`se definen los seis contenedores:

| Contenedor | Imagen | Función |
| --- | --- | --- |
|`login`, `tareas`, `estadisticas` | Construida desde `services/<service>` | Microservicios |
| `db-login`, `db-tareas`, `db-estadisticas`| `postgres:16-alpine` | Una base de datos por servicio |

De esta forma se cumple:
- **Una base de datos por servicio.** Nigún servicio accede a la base de datos de otro.
- **Volúmenes persistentes.** Cada base de datos usa un volumen con nombre (`login-data`, `tareas-data`, `estadisticas-data`) que sobrevive a `docker compose down`.
- **Redes aisladas.** Cada base de datos está en una red privada (`login-db-net`, `tareas-db-net`, `estadisticas-db-net`) a la que solo pertenece su servicio. Los tres servicios comparten además la red `servicios` para poder comunicarse entre sí.
- **Orden de arranque.** Cada base de datos tiene un `healtcheck` y su servicio declara `depends_on` con `condition: service_healthy`, por lo que ningún servicio arranca antes de que su base de datos acepte conexiones.
- **Configuración por variables de entorno.** Las contraseñas y el secreto del token se leen del `.env`. Cada servicio  recibe solo las variables que  necesita.
  
## Integración continua

El flujo `.github/workflows/ci.yml` se ejecuta en cada `push` y `pull_request` hacia `main`, con permisos mínimos de lectura. Tiene tres jobs:

| Job | Qué hace |
|---|---|
| `lint` | Ejecuta `ruff check` y `ruff format --check` sobre todo el código y Hadolint sobre los tres Dockerfiles |
| `tests` | Ejecuta las pruebas de cada servicio en paralelo (matriz de tres servicios) contra una base de datos PostgreSQL real levantada como servicio del job |
| `docker` | Se ejecuta solo si `lint` y `tests` pasan. Construye las tres imágenes y las publica en GHCR |

- **Pruebas contra PostgreSQL.** En local las pruebas usan SQLite por comodidad, y en el CI la variable `TEST_DATABASE_URL` las dirige a PostgreSQL, el mismo motor que usa el entorno real.
- **Publicación condicionada.** En un Pull Request las imágenes solo se construyen para validar que los Dockerfiles funcionan. Solo se publican cuando el cambio llega a `main`.
- **Autenticación sin secretos manuales.** El job usa el `GITHUB_TOKEN` que GitHub genera en cada ejecución, con permiso de escritura de paquetes únicamente en ese job.

## Imagenes publicadas

Cada imagen se etiqueta con el hash corto del commit (`sha-<hash>`) y, en `main`, también con `latest`:

| Servicio | Imagen |
|---|---|
| Login | [`ghcr.io/albaayala/cc-practicas-login`](https://github.com/albaayala/CC-Practicas/pkgs/container/cc-practicas-login) |
| Tareas | [`ghcr.io/albaayala/cc-practicas-tareas`](https://github.com/albaayala/CC-Practicas/pkgs/container/cc-practicas-tareas) |
| Estadísticas | [`ghcr.io/albaayala/cc-practicas-estadisticas`](https://github.com/albaayala/CC-Practicas/pkgs/container/cc-practicas-estadisticas) |

```bash
docker pull ghcr.io/albaayala/cc-practicas-login:latest
```

## Cómo comprobarlo
### Persistencia de datos
1. Con el sistema en marcha, registra una empresa en `http://localhost:8000/docs`.
2. `docker compose down` y después `docker compose up -d`.
3. Inicia sesión con esa empresa y verás que los datos siguen ahí.

### Aislamiento de redes

```bash
docker compose exec login python -c "import socket; socket.create_connection(('db-login', 5432), 3); print('login -> db-login: OK')"
docker compose exec login python -c "import socket; socket.create_connection(('db-tareas', 5432), 3); print('login -> db-tareas: OK')"
```
El primero se conecta y el segundo debe fallar ya que la base de deatos de Tareas no es accesible por el fichero  Login.

### Pruebas y linter en local

Desde la carptea de cada servicio comprueba:
```bash
pip install -r requirements-dev.txt
pytest -v
ruff check . && ruff format --check .
```

## Limitaciones conocidas
- Los servicios se publican en los puertos 8000, 8001 y 8002, para facilitar las pruebas. Cuando exista el API Gateway será el único punto de entrada expuesto.
- Tareas y Estadísticas obtienen la identidad del usuario de cabeceras (`X-Empresa-Id`, `X-Usuario-Id`, `X-Rol`) que añadirá el API Gateway tras validar el token. Por eso deben ser accesibles únicamente desde la red interna.
- La ruta `/internal/eventos/tarea-finalizada` de Estadísticas es una entrada temporal para recibir eventos. La sustituirá el consumidor del broker de mensajes, y no debe ser accesible desde el exterior.
- El Servicio de Tareas todavía no verifica contra Login que el trabajador asignado existe, ni publica eventos hacia Estadísticas.
- Las tablas se crean al arrancar cada servicio; no se usan migraciones.
