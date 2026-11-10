# Datos reutilizables
REGISTRO = {
    "nombreEmpresa" : "Carnicería López",
    "nombreUsuario": "adminLopez",
    "password": "claveSegura"
}

def test_health(client):
    r=client.get("/health")
    assert r.status_code == 200
    assert r.json()=={"status": "ok", "service": "login"}


#  Pruebas de registro
# 1. todo ok
def test_registro_correcto(client):
    r=client.post("/api/auth/registro-empresa", json=REGISTRO)
    assert r.status_code == 201
    assert r.json()["rol"]== "ADMIN"


# 2. campos vacios error 400
def test_registro_campos_vacios(client):
    REGISTRO_VACIO = {
        "nombreEmpresa" : " ",
        "nombreUsuario": " ",
        "password": " "
    }
    r=client.post("/api/auth/registro-empresa", json=REGISTRO_VACIO)
    assert r.status_code == 400
    assert r.json()["detail"]=="Todos los campos deben estar rellenos"

# 3. usuario ya esiste 409
def test_registro_usuario_existe(client):
    REGISTRO_USUARIO = {
        "nombreEmpresa" : "Frueteria pepe",
        "nombreUsuario": "adminLopez",
        "password": "claveSegura"
    }
    r=client.post("/api/auth/registro-empresa", json=REGISTRO)
    r=client.post("/api/auth/registro-empresa", json=REGISTRO_USUARIO)
    assert r.status_code == 409
    assert r.json()["detail"]=="Esta empresa/usuario ya está registrada/o"


# 4. empresa ya esiste 409
def test_registro_empresa_existe(client):
    REGISTRO_EMPRESA= {
        "nombreEmpresa" : "Carnicería López",
        "nombreUsuario": "admin",
        "password": "claveSegura"
    }

    r=client.post("/api/auth/registro-empresa", json=REGISTRO)
    r=client.post("/api/auth/registro-empresa", json=REGISTRO_EMPRESA)
    assert r.status_code == 409
    assert r.json()["detail"]=="Esta empresa/usuario ya está registrada/o"


#  Prueba de login
# 1. todo ok, devuelve token, rol y debecamviar
def test_login_correcto(client):
    r=client.post("/api/auth/registro-empresa", json=REGISTRO)

    DATOS = {
        "nombreUsuario": "adminLopez",
        "password": "claveSegura"
    }

    r=client.post("/api/auth/login", json=DATOS)
    assert r.status_code == 200
    assert r.json()["rol"]=="ADMIN"
    assert r.json()["token"]
    assert r.json()["debeCambiarPassword"] is False


# 2. contraseña erronea 401
def test_login_pass_incorrecto(client):
    r=client.post("/api/auth/registro-empresa", json=REGISTRO)

    DATOS = {
        "nombreUsuario": "adminLopez",
        "password": "clave"
    }

    r=client.post("/api/auth/login", json=DATOS)
    assert r.status_code == 401

# 3. usuario no existe 401
def test_login_usuario_inexistente(client):
    r=client.post("/api/auth/registro-empresa", json=REGISTRO)

    DATOS = {
        "nombreUsuario": "adminL",
        "password": "claveSegura"
    }

    r=client.post("/api/auth/login", json=DATOS)
    assert r.status_code == 401

# 4. campos vacios 400
def test_login_campos_vacios(client):
    r=client.post("/api/auth/registro-empresa", json=REGISTRO)

    DATOS = {
        "nombreUsuario": "  ",
        "password": "  "
    }

    r=client.post("/api/auth/login", json=DATOS)
    assert r.status_code == 400
    assert r.json()["detail"]=="Todos los campos deben estar rellenos"
