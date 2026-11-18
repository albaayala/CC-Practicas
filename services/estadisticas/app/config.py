import os

from dotenv import load_dotenv

load_dotenv()  # carga el .env si existe; NO pisa las variables ya definidas

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")
