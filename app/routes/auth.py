from fastapi import APIRouter

# Crear un router para las rutas climáticas
router = APIRouter()

@router.get("/")
def get_climate_data():
    return {"message": "Datos climáticos funcionando correctamente"}
