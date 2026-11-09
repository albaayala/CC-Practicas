# Que datos se aceptan

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, field_validator


Texto = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]

NombreUsuario = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]


def _validar_password(valor: str) -> str:
    # bcrypt solo admite contraseñas de hasta 72 bytes
    if len(valor.encode()) > 72:
        raise ValueError("Contraseña demasiado larga")
    return valor

class RegistroEmpresa(BaseModel):
    nombreEmpresa: Texto
    nombreUsuario: NombreUsuario
    password: str = Field(min_length=1)

    _comprobar_password = field_validator("password")(_validar_password)

class RegistroRespuesta(BaseModel):
    empresaId: int
    usuarioId: int
    rol: str

class Login(BaseModel):
    nombreUsuario: NombreUsuario
    password: str = Field(min_length=1)

    _comprobar_password = field_validator("password")(_validar_password)

class LoginRespuesta(BaseModel):
    token: str
    rol: str
    debeCambiarPassword: bool

