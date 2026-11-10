from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
# from sqlalchemy import select
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import Session

# from app import enums, mensajes, models, schemas, security
# from app.database import Base, engine, get_db

app = FastAPI(title="Servicio de Tareas")

@app.get("/health")
def health():
    return {"status": "ok", "service": "tareas"}