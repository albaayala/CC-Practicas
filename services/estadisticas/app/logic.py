# Calculo de las estadisticas

from collections.abc import Iterable
from typing import Protocol


class Finalizacion(Protocol):
    duracion_min: int
    retrasada: bool


def calcular_resumen(finalizaciones: Iterable[Finalizacion]) -> dict:
    lista = list(finalizaciones)
    total = len(lista)
    media = 0.0
    retrasadas = 0

    if not total == 0:
        for f in lista:
            media += f.duracion_min
            if f.retrasada:
                retrasadas += 1

        media /= total

        media = round(media)

    return {"tareasFinalizadas": total, "retrasadas": retrasadas, "duracionMediaMin": media}
