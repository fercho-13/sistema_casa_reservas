from sqlalchemy.orm import Session
import models, schemas
from decimal import Decimal

# --- METODOS PARA HABITACIONES ---

# 1. OBTENER LOS DATOS DE UNA HABITACION POR ID
def get_habitacion(db: Session, id_habitacion: int):
    return db.query(models.Habitacion).filter(models.Habitacion.id_habitacion == id_habitacion).first()

# 2. OBTENER LOS DATOS DE TODAS LAS HABITACIONES
def get_habitaciones(db: Session, skip: int, limit: int):
    return db.query(models.Habitacion).offset(skip).limit(limit).all()

# 3. CREAR UNA NUEVA HABITACION
def create_habitacion(id: int, db: Session, habitacion: schemas.HabitacionCreate):
    # Creamos la instancia del modelo de SQLAlchemy con los datos del Schema
    db_habitacion = models.Habitacion(
        id_habitacion = id,
        nombre = habitacion.nombre,
        descripcion = habitacion.descripcion,
        precio_hora = habitacion.precio_hora,
        precio_dia = habitacion.precio_dia
    )
    try:
        db.add(db_habitacion) # Prepara la inserción
        db.commit()           # Confirma la transacción en MySQL
        db.refresh(db_habitacion) # Recarga el objeto (para obtener el ID generado)
        return db_habitacion
    except Exception as e:
        db.rollback()
        raise e

# 4. ACTUALIZAR LOS DATOS DE UNA HABITACION
def update_habitacion(db: Session, id_habitacion: int, habitacion_data: schemas.HabitacionCreate):
    db_habitacion = get_habitacion(db, id_habitacion)
    if db_habitacion:
        db_habitacion.nombre = habitacion_data.nombre
        db_habitacion.descripcion = habitacion_data.descripcion
        db_habitacion.precio_hora = habitacion_data.precio_hora
        db_habitacion.precio_dia = habitacion_data.precio_dia
        db.commit()
        db.refresh(db_habitacion)
    return db_habitacion

# 5. ELIMINAR UNA HABITACION
def delete_habitacion(db: Session, id_habitacion: int):
    db_habitacion = get_habitacion(db, id_habitacion)
    if db_habitacion:
        db.delete(db_habitacion)
        db.commit()
        return True
    return False


# --- METODOS PARA RESERVAS --- 

# 1. OBTENER LOS DATOS DE UNA RESERVA POR ID (SIN ID_HABITACION)
def get_reserva(db: Session, id_reserva: int):
    return db.query(models.Reserva).filter(models.Reserva.id_reserva == id_reserva).first()

# 2. OBTENER LOS DATOS DE TODAS LAS RESERVAS (SIN ID_HABITACION)
def get_reservas(db: Session, skip: int, limit: int):
    return db.query(models.Reserva).offset(skip).limit(limit).all()

# 3. CREAR UNA RESERVA NUEVA
def create_reserva(id: int, db: Session, target_id_habitacion: int, reserva: schemas.ReservaCreate):
    db_reserva = models.Reserva(
        id_reserva = id,
        nombre_cliente = reserva.nombre_cliente,
        fecha_inicio = reserva.fecha_inicio,
        fecha_fin = reserva.fecha_fin,
        id_habitacion = target_id_habitacion
    )
    try:
        db.add(db_reserva)
        db.commit()
        db.refresh(db_reserva)
        return db_reserva
    except Exception as e:
        db.rollback()
        raise e

# 4. ACTUALIZAR LOS DATOS DE UNA RESERVA POR ID
def update_reserva(db: Session, id_reserva: int, reserva_data: schemas.ReservaCreate):
    db_reserva = get_reserva(db, id_reserva)
    if db_reserva:
        db_reserva.nombre_cliente = reserva_data.nombre_cliente
        db_reserva.fecha_inicio = reserva_data.fecha_inicio
        db_reserva.fecha_fin = reserva_data.fecha_fin
        db_reserva.id_habitacion = reserva_data.id_habitacion
        db.commit()
        db.refresh(db_reserva)
    return db_reserva

# 5. ELIMINAR UNA RESERVA POR ID
def delete_reserva(db: Session, id_reserva: int):
    db_reserva = get_reserva(db, id_reserva)
    if db_reserva:
        db.delete(db_reserva)
        db.commit()
        return True
    return False

# 6. OBTENER LOS DATOS DE TODAS LAS RESERVAS DE UNA DETERMINADA HABITACION
def get_reservas_por_habitacion(db: Session, id_habitacion: int, skip: int, limit: int):
    return db.query(models.Reserva).filter(models.Reserva.id_habitacion == id_habitacion).offset(skip).limit(limit).all()
