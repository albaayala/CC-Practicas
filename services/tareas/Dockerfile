# --------------- Instalar dependencias ---------------
FROM python:3.12-slim AS builder
WORKDIR /builder

# instalar las depedendias que hemos definido en los ficheros requirements.txt
# la de test no, ya que es es solo para test
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --------------- Imagen final ---------------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Usuario sin provilegios
# RUN groupadd --system app && useradd --system --gid app --no-create-home app
RUN groupadd --system --gid 10001 app && useradd --system --uid 10001 --gid app --no-create-home app

WORKDIR /app

#librerias instaladas
COPY --from=builder /install /usr/local

# Codigo fina
# COPY --chown=app:app app ./app
COPY --chown=10001:10001 app ./app

# USER app
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
