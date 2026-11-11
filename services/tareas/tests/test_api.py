ADMIN = {"X-Empresa-Id": "1", "X-Usuario-Id": "1", "X-Rol": "ADMIN"}

ADMIN_EMPRESA_2 = {"X-Empresa-Id": "2", "X-Usuario-Id": "1", "X-Rol": "ADMIN"}

TRABAJADOR_7 = {"X-Empresa-Id": "1", "X-Usuario-Id": "7", "X-Rol": "TRABAJADOR"}

TRABAJADOR_8 = {"X-Empresa-Id": "1", "X-Usuario-Id": "8", "X-Rol": "TRABAJADOR"}

TAREA = {
    "titulo": "Instalar ventana",
    "trabajadorId": 7,
    "inicioPrevisto": "2026-10-20T08:00:00Z",
    "finPrevisto": "2026-10-20T12:00:00Z",
}


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "service": "tareas"}


# Test de crear tareas


def test_crear_tarea_correcta(client):
    r = client.post("/api/tareas", json=TAREA, headers=ADMIN)
    assert r.status_code == 201
    assert r.json()["estado"] == "ASIGNADA"


def test_tarea_sin_campo_obligatorio(client):
    r = client.post("/api/tareas", json={**TAREA, "titulo": ""}, headers=ADMIN)
    assert r.status_code == 400
    assert r.json()["detail"] == "Hay campos obligatorios vacíos"


def test_fecha_fin_anterior_al_ini(client):
    r = client.post(
        "/api/tareas", json={**TAREA, "finPrevisto": "2026-10-20T07:00:00Z"}, headers=ADMIN
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "La fecha de fin debe ser posterior a la de inicio"


def test_hay_solape_trabajador(client):
    client.post("/api/tareas", json=TAREA, headers=ADMIN)
    r = client.post("/api/tareas", json=TAREA, headers=ADMIN)
    assert r.status_code == 409
    assert r.json()["detail"] == "Este trabajador ya tiene una tarea asignada en ese rango de hora"


def test_mismo_franja_horaria_otro_trabajador(client):
    client.post("/api/tareas", json=TAREA, headers=ADMIN)
    r = client.post("/api/tareas", json={**TAREA, "trabajadorId": 8}, headers=ADMIN)
    assert r.status_code == 201
    assert r.json()["estado"] == "ASIGNADA"


def test_trabajdor_no_crear_tareas(client):
    r = client.post("/api/tareas", json=TAREA, headers=TRABAJADOR_7)
    assert r.status_code == 403
    assert r.json()["detail"] == "Solo el administrador puede crear tareas"


def test_tareas_cosecutivas(client):
    client.post("/api/tareas", json=TAREA, headers=ADMIN)
    r = client.post(
        "/api/tareas",
        json={
            **TAREA,
            "inicioPrevisto": "2026-10-20T12:00:00Z",
            "finPrevisto": "2026-10-20T13:00:00Z",
        },
        headers=ADMIN,
    )
    assert r.status_code == 201
    assert r.json()["estado"] == "ASIGNADA"


def test_sin_cabecera(client):
    r = client.post("/api/tareas", json=TAREA)
    assert r.status_code == 401


def test_rol_inexistente(client):
    r = client.post("/api/tareas", json=TAREA, headers={**ADMIN, "X_Rol": "JEFE"})
    assert r.status_code == 201
    assert r.json()["estado"] == "ASIGNADA"


# Test de listar tareas


def test_sin_identidad_no_accede(client):
    assert client.get("/api/tareas").status_code == 401


def test_trabajador_solo_ve_sus_tareas(client):
    client.post("/api/tareas", json=TAREA, headers=ADMIN)
    client.post("/api/tareas", json={**TAREA, "trabajadorId": 8}, headers=ADMIN)

    propias = client.get("/api/tareas", headers=TRABAJADOR_7).json()

    assert [t["trabajadorId"] for t in propias] == [7]
    assert len(client.get("/api/tareas", headers=ADMIN).json()) == 2
    assert len(client.get("/api/tareas", headers=TRABAJADOR_8).json()) == 1


def test_listar_sin_tareas_devuelve_lista_vacia(client):
    r = client.get("/api/tareas", headers=ADMIN)
    assert r.status_code == 200
    assert r.json() == []


def test_administrador_ve_todas_las_tareas_de_su_empresa(client):
    client.post("/api/tareas", json=TAREA, headers=ADMIN)
    client.post("/api/tareas", json={**TAREA, "trabajadorId": "8"}, headers=ADMIN)

    r = client.get("/api/tareas", headers=ADMIN)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_administrador_filtra_por_trabajador(client):
    client.post("/api/tareas", json=TAREA, headers=ADMIN)
    client.post("/api/tareas", json={**TAREA, "trabajadorId": "8"}, headers=ADMIN)
    r = client.get("/api/tareas", params={"trabajadorId": 8}, headers=ADMIN)
    assert [t["trabajadorId"] for t in r.json()] == [8]


def test_trabajador_no_puede_ver_tareas_de_otro_aunque_lo_pida(client):
    client.post("/api/tareas", json=TAREA, headers=ADMIN)
    client.post("/api/tareas", json={**TAREA, "trabajadorId": "8"}, headers=ADMIN)

    r = client.get("/api/tareas", params={"trabajadorId": 8}, headers=TRABAJADOR_7)
    assert [t["trabajadorId"] for t in r.json()] == [7]


def test_otra_empresa_no_ve_tareas_ajenas(client):
    client.post("/api/tareas", json=TAREA, headers=ADMIN)
    r = client.get("/api/tareas", headers=ADMIN_EMPRESA_2)
    assert r.status_code == 200
    assert r.json() == []
