from datetime import UTC, datetime, timedelta
import jwt
import bcrypt

from app import config

ALGORITMO = "HS256"
DURACION_TOKEN = timedelta(days=7)



def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verificar_password(password: str, password_hash:str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def crear_token(usuario_id: int, empresa_id: int, rol: str) -> str:
    payload = {
        "sub": str(usuario_id),
        "empresaId": empresa_id,
        "rol": rol,
        "exp": datetime.now(UTC) + DURACION_TOKEN,
    }
    return jwt.encode(payload, config.jwt_secret(), algorithm = ALGORITMO)