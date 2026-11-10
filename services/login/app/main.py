from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import enums, mensajes, models, schemas, security
from app.database import Base, engine, get_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Servicio Login", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def campos_invalidos(_: Request, __: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": mensajes.CAMPOS_VACIOS})


@app.get("/health")
def health():
    return {"status": "ok", "service": "login"}


@app.post("/api/auth/registro-empresa", response_model=schemas.RegistroRespuesta, status_code=201)
def registro_empresa(datos: schemas.RegistroEmpresa, db: Session = Depends(get_db)):

    # comprobamos que empresa no exista
    empresa_existe = db.scalar(
        select(models.Empresa).where(models.Empresa.nombre == datos.nombreEmpresa)
    )
    # compobamos que el usuairo no exista
    usario_existe = db.scalar(
        select(models.Usuario).where(models.Usuario.nombre_user == datos.nombreUsuario)
    )

    # si existe al guno de los dos --> error
    if empresa_existe or usario_existe:
        raise HTTPException(status_code=409, detail=mensajes.EMPRESA_O_USUARIO_DUPLICADO)

    # si no existe creamos empresa
    empresa = models.Empresa(nombre=datos.nombreEmpresa)
    db.add(empresa)
    db.flush()

    # creamos usuario administrador
    usuario = models.Usuario(
        empresa_id=empresa.id,
        nombre_user=datos.nombreUsuario,
        password_hash=security.hash_password(datos.password),
        rol=enums.Rol.ADMIN,
    )

    db.add(usuario)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=mensajes.EMPRESA_O_USUARIO_DUPLICADO) from None

    # devolvemos respuesta
    return {"empresaId": empresa.id, "usuarioId": usuario.id, "rol": usuario.rol}


@app.post("/api/auth/login", response_model=schemas.LoginRespuesta, status_code=200)
def login(datos: schemas.Login, db: Session = Depends(get_db)):
    # comporbamos exita usuario
    usuario = db.scalar(
        select(models.Usuario).where(models.Usuario.nombre_user == datos.nombreUsuario)
    )

    # comporbamos que la contraseña sea correcta
    if usuario is None or not security.verificar_password(datos.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail=mensajes.CREDENCIALES_ERRONEAS)

    # generamos token
    token = security.crear_token(usuario.id, usuario.empresa_id, usuario.rol)
    return {"token": token, "rol": usuario.rol, "debeCambiarPassword": usuario.cambiar_password}
