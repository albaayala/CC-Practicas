from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Tarea(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(index=True)
    titulo: Mapped[str] = mapped_column(String(200))
    especificaciones: Mapped[str | None] = mapped_column(String(220), default=None)
    tipo_id: Mapped[int | None] = mapped_column(default=None, index=True)
    trabajador_id: Mapped[int] = mapped_column(index=True)
    inicio_previsto: Mapped[datetime] = mapped_column(DateTime)
    fin_previsto: Mapped[datetime] = mapped_column(DateTime)
    estado:Mapped[str] = mapped_column(String(200), default="ASIGNADA")
    inicio_real: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    fin_real:Mapped[datetime | None] = mapped_column(DateTime, default=None)