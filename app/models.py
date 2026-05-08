from database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column 
from sqlalchemy import String, DateTime, ForeignKey, Numeric
from typing import List, Optional
from decimal import Decimal
from datetime import datetime 


class Habitacion(Base): 
    #Nombre de la tabla
    __tablename__ = "habitaciones"

    #Clave principal
    id_habitacion: Mapped[int] = mapped_column(primary_key = True, index = True)
    
    #Columnas
    nombre: Mapped[str] = mapped_column(String(50), nullable = False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(250))
    precio_hora: Mapped[Decimal] = mapped_column(Numeric(precision = 10, scale = 2)) #99.999.999,99
    precio_dia: Mapped[Decimal] = mapped_column(Numeric(precision = 10, scale = 2)) #99.999.999,99

    #Relacion
    reservas: Mapped[List["Reserva"]] = relationship(back_populates = "habitacion")


class Reserva(Base):
    #Nombre de la tabla
    __tablename__ = "reservas"

    #Clave principal
    id_reserva: Mapped[int] = mapped_column(primary_key = True, index = True)

    #Columnas
    nombre_cliente: Mapped[str] = mapped_column(String(50), nullable = False)
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime, nullable = False)
    fecha_fin: Mapped[datetime] = mapped_column(DateTime, nullable = False)

    #Clave foranea
    id_habitacion: Mapped[int] = mapped_column(ForeignKey("habitaciones.id_habitacion"), nullable = False)

    #Relacion
    habitacion: Mapped["Habitacion"] = relationship(back_populates = "reservas")
