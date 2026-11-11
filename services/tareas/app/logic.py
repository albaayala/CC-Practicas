from datetime import UTC, datetime


def solapan(ini_a: datetime, fin_a: datetime, ini_b: datetime, fin_b: datetime) -> bool:
    # Dos tramso horarios se solapan si cada uno empieza antes de que el otro termine.
    # Si la fecha de fin de a es la fecha de inicio de b no se considera solape

    return ini_a < fin_b and ini_b < fin_a


def date_sin_zona_horaria(fecha: datetime) -> datetime:
    # Normalizamos la fecha para que no tenga zona horaria
    if fecha.tzinfo is not None:
        fecha = fecha.astimezone(UTC).replace(tzinfo=None)

    return fecha
