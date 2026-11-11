from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, StringConstraints

from app.enums import EstadoTarea

Texto = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]


class TareaNueva(BaseModel):
    titulo: Texto
    especificaciones: str | None = None
    tipoId: int | None = None
    trabajadorId: int
    inicioPrevisto: datetime
    finPrevisto: datetime


class TareaRespuesta(BaseModel):
    id: int
    titulo: str
    especificaciones: str | None
    tipoId: int | None
    trabajadorId: int
    inicioPrevisto: datetime
    finPrevisto: datetime
    estado: EstadoTarea
