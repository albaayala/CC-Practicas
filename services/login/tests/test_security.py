import jwt
import pytest
from app import security


# hash_password no devuelve la contraseña original y acepta la original
def test_hash_no_guarda_original():
    pass_h = security.hash_password("miClave")
    assert pass_h != "miClave"
    assert security.verificar_password("miClave", pass_h)


# verificar_password rechaza la erronea
def test_rechaza_pass_icorrecta():
    pass_h = security.hash_password("miClave123")
    assert not security.verificar_password("otraClave", pass_h)


# crear token y su lecura decuelve empresa, rol y sub
def test_token_contiene_elementos():
    token = security.crear_token(usuario_id=7, empresa_id=3, rol="ADMIN")
    datos = security.decodificar_token(token)
    assert datos["sub"] == "7"
    assert datos["empresaId"] == 3
    assert datos["rol"] == "ADMIN"


#  un token manipulado lanza jwt.InvalidTokenError
def test_token_manipulado_se_rechaza():
    token = security.crear_token(1, 1, "ADMIN")
    with pytest.raises(jwt.InvalidTokenError):
        security.decodificar_token(token + "x")
