from sqlalchemy.orm import Session
import crud, database, schemas
from fastapi import APIRouter, HTTPException, Depends
from typing import List

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)

# --- ENDPOINTS PARA ACCIONES DIRECTAS SOBRE RESERVAS

# ENDPOINT PARA OBTENER UNA RESERVA POR ID
@router.get("/{id_reserva}", response_model = schemas.Reserva)
def obtener_reserva(id_reserva: int, db: Session = Depends(database.get_db)):
    db_reserva = crud.get_reserva(db, id_reserva)
    if db_reserva is None:
        raise HTTPException(status_code = 404, detail = "Reserva no encontrada")
    return db_reserva

# ENDPOINT PARA OBTENER TODAS LAS RESERVAS
@router.get("/", response_model = List[schemas.Reserva])
def obtener_reservas(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    db_reservas = crud.get_reservas(db, skip, limit)
    if not db_reservas:
        raise HTTPException(status_code = 404, detail = "No hay ninguna reserva registrada")
    return db_reservas

# ENDPOINT PARA ACTUALIZAR UNA RESERVA
@router.put("/actualizar-reserva/{id_reserva}", response_model=schemas.Reserva)
def actualizar_reserva(id_reserva: int, reserva: schemas.ReservaCreate, db: Session = Depends(database.get_db)):
    db_reserva = crud.get_reserva(db, id_reserva)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    if db_reserva.nombre_cliente is not None:
        db_reserva.nombre_cliente = reserva.nombre_cliente
        
    if db_reserva.fecha_inicio is not None:
        db_reserva.fecha_inicio = reserva.fecha_inicio

    if db_reserva.fecha_fin is not None:
        db_reserva.fecha_fin = reserva.fecha_fin

    db.commit()
    db.refresh(db_reserva)

    return db_reserva

# ENDPOINT PARA ELIMINAR UNA RESERVA
@router.delete("/eliminar-reserva/{id_reserva}")
def eliminar_reserva(id_reserva: int, db: Session = Depends(database.get_db)):
    if crud.delete_reserva(db, id_reserva) is False:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"Exito": "Reserva eliminada"}