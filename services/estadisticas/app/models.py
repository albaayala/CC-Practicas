from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TareaFinalizada(Base):
    __tablename__ = "tareas_finalizadas"

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(index=True)
    tarea_id: Mapped[int] = mapped_column(unique=True)
    tipo_id: Mapped[int | None] = mapped_column(default=None)
    trabajador_id: Mapped[int]
    duracion_min: Mapped[int]
    retrasada: Mapped[bool] = mapped_column(Boolean, default=False)
    # fecha_fin: Mapped[datetime] = mapped_column(DateTime)
