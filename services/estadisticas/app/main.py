from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db
from app.logic import calcular_resumen


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Servicio de Estadisticas", lifespan=lifespan)


def solo_admin(x_empresa_id: int | None = Header(None), x_rol: str | None = Header(None)) -> int:
    """Devuelve el id de empresa"""

    if x_empresa_id is None or x_rol is None:
        raise HTTPException(status_code=401, detail="No autenticado")

    if x_rol != "ADMIN":
        raise HTTPException(status_code=403, detail="Solo el administrador ve las estadísticas")

    return x_empresa_id


@app.get("/health")
def health():
    return {"status": "ok", "service": "estadisticas"}


@app.post("/internal/eventos/tarea-finalizada", status_code=201)
def registrar_finalizada(evento: schemas.EventoTareaFinalizada, db: Session = Depends(get_db)):
    ya_registrada = db.scalar(
        select(models.TareaFinalizada).where(models.TareaFinalizada.tarea_id == evento.tareaId)
    )

    if ya_registrada:
        return {"status": "duplicado"}

    db.add(
        models.TareaFinalizada(
            empresa_id=evento.empresaId,
            tarea_id=evento.tareaId,
            tipo_id=evento.tipoId,
            trabajador_id=evento.trabajadorId,
            duracion_min=evento.duracionMin,
            retrasada=evento.retrasada,
        )
    )

    db.commit()
    return {"status": "registrado"}


@app.get("/api/estadisticas/resumen", response_model=schemas.Resumen)
def resumen(empresa_id: int = Depends(solo_admin), db: Session = Depends(get_db)):

    finalizadas = db.scalars(
        select(models.TareaFinalizada).where(models.TareaFinalizada.empresa_id == empresa_id)
    )

    return calcular_resumen(finalizadas)
