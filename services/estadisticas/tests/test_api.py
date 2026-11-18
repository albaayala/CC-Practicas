ADMIN = {"X-Empresa-Id": "1", "X-Rol": "ADMIN"}
TRABAJADOR = {"X-Empresa-Id": "1", "X-Rol": "TRABAJADOR"}


def evento(tarea_id: int, duracion: int, retrasada: bool = False, empresa: int = 1) -> dict:
    return {
        "empresaId": empresa,
        "tareaId": tarea_id,
        "trabajadorId": 7,
        "duracionMin": duracion,
        "retrasada": retrasada,
    }


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "service": "estadisticas"}


# Pruebas de recepción de eventos
def test_evento_nuevo_se_registra(client):
    r = client.post("/internal/eventos/tarea-finalizada", json=evento(1, 60))
    assert r.status_code == 201
    assert r.json() == {"status": "registrado"}


def test_evento_nuevo_se_ignoara(client):
    client.post("/internal/eventos/tarea-finalizada", json=evento(1, 60))
    r = client.post("/internal/eventos/tarea-finalizada", json=evento(1, 60))
    assert r.json() == {"status": "duplicado"}


def test_evento_con_duracion_negativa_se_rechaza(client):
    r = client.post("/internal/eventos/tarea-finalizada", json=evento(1, -5))
    assert r.status_code in (400, 422)


# Pruebas del resumne
def test_resumen_sin_datos_devuelve_ceros(client):
    r = client.get("/api/estadisticas/resumen", headers=ADMIN)
    assert r.status_code == 200
    assert r.json() == {"tareasFinalizadas": 0, "retrasadas": 0, "duracionMediaMin": 0}


def test_resumen_refleja_eventos_recibidos(client):
    client.post("/internal/eventos/tarea-finalizada", json=evento(1, 60))
    client.post("/internal/eventos/tarea-finalizada", json=evento(2, 120, retrasada=True))
    r = client.get("/api/estadisticas/resumen", headers=ADMIN)
    assert r.status_code == 200
    assert r.json() == {"tareasFinalizadas": 2, "retrasadas": 1, "duracionMediaMin": 90}


def test_un_evento_repetido_no_cuenta_dos_veces(client):
    client.post("/internal/eventos/tarea-finalizada", json=evento(1, 60))
    client.post("/internal/eventos/tarea-finalizada", json=evento(1, 60))
    r = client.get("/api/estadisticas/resumen", headers=ADMIN)
    assert r.json()["tareasFinalizadas"] == 1


def test_cada_empresa_solo_ve_sus_datos(client):
    client.post("/internal/eventos/tarea-finalizada", json=evento(1, 60, empresa=2))
    r = client.get("/api/estadisticas/resumen", headers=ADMIN)
    assert r.json()["tareasFinalizadas"] == 0


def test_el_resumen_no_mezcla_datos_de_otras_empresas(client):
    client.post("/internal/eventos/tarea-finalizada", json=evento(1, 60, empresa=1))
    client.post("/internal/eventos/tarea-finalizada", json=evento(2, 600, empresa=2))
    r = client.get("/api/estadisticas/resumen", headers=ADMIN)
    assert r.json() == {"tareasFinalizadas": 1, "retrasadas": 0, "duracionMediaMin": 60}


def test_un_trabajador_no_ve_estadisticas(client):
    assert client.get("/api/estadisticas/resumen", headers=TRABAJADOR).status_code == 403


def test_sin_identidad_no_se_accede(client):
    assert client.get("/api/estadisticas/resumen").status_code == 401
