from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import enums, mensajes, models, schemas
from app.database import Base, engine, get_db
from app.logic import date_sin_zona_horaria, solapan


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Servicio de Tareas", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def campos_invalidos(_: Request, __: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": mensajes.CAMPOS_OBLIGATORIOS})


@dataclass
class Contexto:
    empresa_id: int
    usuario_id: int
    rol: str


def contexto(
    x_empresa_id: int | None = Header(None),
    x_usuario_id: int | None = Header(None),
    x_rol: str | None = Header(None),
) -> Contexto:
    # Indentidada del usuario. Ahora llegan cabeceras que añadirá
    # el API Gateway tras validar el token JWT.
    # Este servicio solo estará accesible desde la red interna
    if x_empresa_id is None or x_usuario_id is None or x_rol not in ("ADMIN", "TRABAJADOR"):
        raise HTTPException(status_code=401, detail="No autenticado")

    return Contexto(x_empresa_id, x_usuario_id, x_rol)


def _a_respuesta(t: models.Tarea) -> dict:
    return {
        "id": t.id,
        "titulo": t.titulo,
        "especificaciones": t.especificaciones,
        "tipoId": t.tipo_id,
        "trabajadorId": t.trabajador_id,
        "inicioPrevisto": t.inicio_previsto,
        "finPrevisto": t.fin_previsto,
        "estado": t.estado,
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "tareas"}


@app.post("/api/tareas", response_model=schemas.TareaRespuesta, status_code=201)
def crear_tarea(
    datos: schemas.TareaNueva, ctx: Contexto = Depends(contexto), db: Session = Depends(get_db)
):
    if ctx.rol != "ADMIN":
        raise HTTPException(status_code=403, detail="Solo el administrador puede crear tareas")

    inicio = date_sin_zona_horaria(datos.inicioPrevisto)
    fin = date_sin_zona_horaria(datos.finPrevisto)

    # Comporbamos fecha de inicio comience antes que al de fin
    if fin <= inicio:
        raise HTTPException(status_code=400, detail=mensajes.MENSAJE_FECHAS)

    # Comporbamos que no solape con taeas del trabajador
    tareas_trabajador = db.scalars(
        select(models.Tarea).where(
            models.Tarea.empresa_id == ctx.empresa_id,
            models.Tarea.trabajador_id == datos.trabajadorId,
            models.Tarea.estado != enums.EstadoTarea.FINALIZADA,
        )
    )

    for t in tareas_trabajador:
        if solapan(inicio, fin, t.inicio_previsto, t.fin_previsto):
            raise HTTPException(status_code=409, detail=mensajes.MENSAJE_SOLAPE)

    # Creamos tarea
    tarea = models.Tarea(
        empresa_id=ctx.empresa_id,
        titulo=datos.titulo,
        especificaciones=datos.especificaciones,
        tipo_id=datos.tipoId,
        trabajador_id=datos.trabajadorId,
        inicio_previsto=inicio,
        fin_previsto=fin,
    )

    db.add(tarea)
    db.commit()

    return _a_respuesta(tarea)


@app.get("/api/tareas", response_model=list[schemas.TareaRespuesta])
def listar_tareas(
    trabajadorId: int | None = None,
    estado: str | None = None,
    ctx: Contexto = Depends(contexto),
    db: Session = Depends(get_db),
):
    consulta = select(models.Tarea).where(models.Tarea.empresa_id == ctx.empresa_id)
    if ctx.rol == "TRABAJADOR":
        consulta = consulta.where(models.Tarea.trabajador_id == ctx.usuario_id)
    elif trabajadorId is not None:
        consulta = consulta.where(models.Tarea.trabajador_id == trabajadorId)

    if estado is not None:
        consulta = consulta.where(models.Tarea.estado == estado)

    tareas = db.scalars(consulta.order_by(models.Tarea.inicio_previsto))
    return [_a_respuesta(t) for t in tareas]
