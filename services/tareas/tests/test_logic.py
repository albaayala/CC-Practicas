from datetime import UTC, datetime

from app.logic import date_sin_zona_horaria, solapan


def fecha(hora: int) -> datetime:
    return datetime(2026, 10, 20, hora, 0)


def test_rangos_se_solapan():
    assert solapan(fecha(8), fecha(12), fecha(10), fecha(14))


def test_rangos_dentro_de_tramo():
    assert solapan(fecha(8), fecha(12), fecha(10), fecha(11))


def test_no_solapan():
    assert not solapan(fecha(8), fecha(9), fecha(11), fecha(12))


def test_no_solapan_mismo_ini_fin():
    assert not solapan(fecha(8), fecha(9), fecha(9), fecha(12))


def test_zona_horaria():
    con_zona = datetime(2026, 10, 20, 8, 0, tzinfo=UTC)
    assert date_sin_zona_horaria(con_zona) == datetime(2026, 10, 20, 8, 0)
    assert date_sin_zona_horaria(con_zona).tzinfo is None
