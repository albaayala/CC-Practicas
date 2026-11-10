import os

from dotenv import load_dotenv

load_dotenv()  # carga el .env si existe; NO pisa las variables ya definidas

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")


def jwt_secret() -> str:
    secreto = os.environ.get("JWT_SECRET")
    if not secreto:
        raise RuntimeError("Falta la variable de entorno JWT_SECRET")
    return secreto
