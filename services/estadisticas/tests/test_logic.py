from dataclasses import dataclass

from app.logic import calcular_resumen


@dataclass
class Fin:
    duracion_min: int
    retrasada: bool = False


def test_resumen_sin_datos():
    assert calcular_resumen([]) == {
        "tareasFinalizadas": 0,
        "retrasadas": 0,
        "duracionMediaMin": 0,
    }


def test_resumen_con_datos():
    datos = [Fin(60), Fin(120, retrasada=True), Fin(90)]
    duracion_media = round((60 + 120 + 90) / 3)
    resumen = calcular_resumen(datos)
    assert resumen["tareasFinalizadas"] == 3
    assert resumen["retrasadas"] == 1
    assert resumen["duracionMediaMin"] == duracion_media
