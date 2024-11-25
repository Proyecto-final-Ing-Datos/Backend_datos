from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.data_routes import router as data_router
from app.routes.model_routes import router as model_router
from app.routes.realtime_routes import router as realtime_router

# Crear instancia de FastAPI
app = FastAPI(
    title="API de Datos Climáticos",
    description="API para procesar, visualizar y predecir datos climáticos utilizando IoT y modelos LSTM.",
    version="1.0.0"
)

# Configuración de CORS (opcional, útil si tienes un frontend separado)
origins = [
    "http://localhost:3000",  # Dirección de tu frontend local (React, Angular, etc.)
    "https://mi-frontend.com"  # URL del frontend en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas desde los módulos de rutas
app.include_router(data_router, prefix="/api/data", tags=["Data"])
app.include_router(model_router, prefix="/api/model", tags=["Model"])
app.include_router(realtime_router, prefix="/api/realtime", tags=["Realtime"])

# Rutas raíz o de prueba
@app.get("/")
def root():
    return {"message": "¡Bienvenido a la API de Datos Climáticos!"}
