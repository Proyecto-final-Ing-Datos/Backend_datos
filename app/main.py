from fastapi import FastAPI
from app.routes import climate  # Importa el módulo correctamente

# Crear la aplicación FastAPI
app = FastAPI()

# Registrar el router de climate
app.include_router(climate.router, prefix="/api/climate", tags=["Clima"])

@app.get("/")
def root():
    return {"message": "API de Datos Climáticos funcionando correctamente"}
