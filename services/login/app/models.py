from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    nombre_user: Mapped[str] = mapped_column(String(80), unique=True)
    nombre_completo: Mapped[str | None] = mapped_column(String(120), default=None)
    password_hash: Mapped[str] = mapped_column(String(100))
    rol: Mapped[str] = mapped_column(String(20))
    cambiar_password: Mapped[bool] = mapped_column(Boolean, default=False)
