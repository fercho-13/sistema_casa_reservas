from sqlalchemy.orm import Session
import schemas, crud, database
from fastapi import APIRouter, HTTPException, Depends
from typing import List


# --- ENDPOINTS DE HABITACIONES ---

router = APIRouter(
    prefix="/habitaciones",
    tags=["Habitaciones"]
)

# Endpoint para crear una habitacion
@router.post("/crear-habitacion/{id_habitacion}", response_model = schemas.Habitacion)
def crear_habitacion(id_habitacion: int, habitacion: schemas.HabitacionCreate, db: Session = Depends(database.get_db)):
    db_habitacion = crud.get_habitacion(db, id_habitacion)
    if db_habitacion:
        raise HTTPException(status_code=409, detail="La habitacion ya existe")
    return crud.create_habitacion(id_habitacion, db=db, habitacion=habitacion)

# Endpoint para obtener todas las habitaciones
@router.get("/", response_model = List[schemas.Habitacion])
def leer_habitaciones(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    db_habitaciones = crud.get_habitaciones(db, skip = skip, limit = limit) 
    if not db_habitaciones:
        raise HTTPException(status_code = 404, detail = "No hay ninguna habitacion registrada")
    return db_habitaciones
    

# Endpoint para obtener una habitacion por ID
@router.get("/{id_habitacion}", response_model = schemas.Habitacion)
def leer_habitacion(id_habitacion: int, db: Session = Depends(database.get_db)): 
    db_habitacion = crud.get_habitacion(db, id_habitacion)
    if db_habitacion is None:
        raise HTTPException(status_code = 404, detail = "Habitacion no encontrada")
    return db_habitacion

# Endpoint para actualizar una habitacion por ID
@router.put("/actualizar-habitacion/{id_habitacion}", response_model = schemas.Habitacion)
def actualizar_habitacion(id_habitacion: int, habitacion: schemas.HabitacionCreate, db: Session = Depends(database.get_db)):
    db_habitacion = crud.get_habitacion(db, id_habitacion)
    if db_habitacion is None:
        raise HTTPException(status_code=404, detail="Habitacion no encontrada")
    
    if db_habitacion.nombre is not None:
        db_habitacion.nombre = habitacion.nombre

    if db_habitacion.descripcion is not None:
        db_habitacion.descripcion = habitacion.descripcion

    if db_habitacion.precio_hora is not None:
        db_habitacion.precio_hora = habitacion.precio_hora

    if db_habitacion.precio_dia is not None:
        db_habitacion.precio_dia = habitacion.precio_dia

    db.commit()
    db.refresh(db_habitacion)

    return db_habitacion

# Endpoint para eliminar una habitacion por ID
@router.delete("/eliminar-habitacion/{id_habitacion}")
def eliminar_habitacion(id_habitacion: int, db: Session = Depends(database.get_db)): # FALTA OBTENER ID
    if crud.delete_habitacion(db, id_habitacion) is False:
        raise HTTPException(status_code=404, detail="Habitacion no encontrada")
    return {"Exito": "Habitacion eliminada!"}

# --- ENDPOINTS DE RESERVAS EN BASE AL ID DE UNA HABITACION ---

# ENDPOINT PARA OBTENER TODAS LAS RESERVAS DE UNA HABITACION
@router.get("/{id_habitacion}/reservas", response_model = List[schemas.Reserva])
def obtener_reservas_por_habitacion(id_habitacion: int, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    db_reservas = crud.get_reservas_por_habitacion(db, id_habitacion, skip = skip, limit = limit)
    if not db_reservas:
        raise HTTPException(status_code=404, detail="La habitacion no tiene reservas")
    return db_reservas

# ENDPOINT PARA CREAR UNA RESERVA 
@router.post("/{id_habitacion}/crear-reserva/{id_reserva}", response_model = schemas.Reserva)
def crear_reserva_por_habitacion(id_habitacion: int, id_reserva: int, reserva: schemas.ReservaCreate, db: Session = Depends(database.get_db)):
    db_reserva = crud.get_reserva(db, id_reserva)
    if db_reserva:
        raise HTTPException(status_code = 409, detail = "La reserva ya existe")
    return crud.create_reserva(id_reserva, db, id_habitacion, reserva)