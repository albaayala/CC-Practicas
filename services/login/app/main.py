from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models
from app.database import Base, engine

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="Servicio Login", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "service": "login"}