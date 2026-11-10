from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
# from sqlalchemy import select
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import Session

from app import enums, models
from app.database import Base, engine, get_db

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="Servicio de Tareas", lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def campos_invalidos(_: Request, __: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": "Los campos deben estar rellenos"})


@app.get("/health")
def health():
    return {"status": "ok", "service": "tareas"}