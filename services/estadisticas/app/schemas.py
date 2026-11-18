from pydantic import BaseModel, Field


class EventoTareaFinalizada(BaseModel):
    empresaId: int
    tareaId: int
    tipoId: int | None = None
    trabajadorId: int
    duracionMin: int = Field(ge=0)
    retrasada: bool = False
    # finalizadaEl: datetime


class Resumen(BaseModel):
    tareasFinalizadas: int
    retrasadas: int
    duracionMediaMin: int
