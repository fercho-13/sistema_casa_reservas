from fastapi import FastAPI
import models, database
from routers import habitaciones, reservas

# Crea las tablas si no existen (útil para el desarrollo)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Sistema de Reservas",
              description="API de gestion de reservas por hora y dia",
              version="1.0.0"
)

app.include_router(habitaciones.router)
app.include_router(reservas.router)

@app.get("/")
def home():
    return {"mensaje": "Sistema de gestion de reservas"}