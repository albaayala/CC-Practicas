# elementos reutilizables para las pruebas
import os

# 1. Las variables de entorno se fijan antes de importar la app
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "sqlite:///./test.db")
os.environ["JWT_SECRET"] = "secreto-solo-para-pruebas-con-mas-de-32-caracteres"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app

@pytest.fixture()
def client():
    # Base de datos limpia para cada prueba
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c
