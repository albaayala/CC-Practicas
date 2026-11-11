from enum import StrEnum


class EstadoTarea(StrEnum):
    ASIGNADA = "ASIGNADA"
    ACTIVA = "ACTIVA"
    PAUSADA = "PAUSADA"
    FINALIZADA = "FINALIZADA"
