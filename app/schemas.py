from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

# --- SCHEMAS DE RESERVA ---

class ReservaBase(BaseModel):
    nombre_cliente: str
    fecha_inicio: datetime
    fecha_fin: datetime

class ReservaCreate(ReservaBase):
    @model_validator(mode = 'after')
    def verificar_fechas(self) -> 'ReservaCreate':
        if self.fecha_inicio >= self.fecha_fin:
            raise ValueError("La fecha fin debe ser posterior a la fecha inicio")
        if self.fecha_iciio < datetime.now():
            raise ValueError("No se pueden realizar resrvas en el pasado")
        return self

class Reserva(ReservaBase): 
    id_reserva: int
    id_habitacion: int

    model_config = ConfigDict(from_attributes = True)

# --- SCHEMAS DE HABITACIÓN ---

class HabitacionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_hora: Decimal
    precio_dia: Decimal

class HabitacionCreate(HabitacionBase):
    pass  # Se usa cuando creamos una habitación nueva

class Habitacion(HabitacionBase):
    id_habitacion: int
    # Incluimos las reservas asociadas para cuando consultemos la habitación
    reservas: List[Reserva] = []

    model_config = ConfigDict(from_attributes = True)