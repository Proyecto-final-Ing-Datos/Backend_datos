from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.data_routes import router as data_router
from app.routes.model_routes import router as model_router
from app.routes.realtime_routes import router as realtime_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.thingspeak_service import fetch_data_from_thingspeak
from app.services.data_processing_service import preprocess_data
from app.services.database_service import save_original_data_to_db, save_cleaned_data_to_db
from app.db import SessionLocal, init_db  # Importar función para inicializar la base de datos
import logging

# Configurar logs básicos
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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

# Función para automatizar el guardado de datos
def fetch_and_store_data():
    """
    Obtiene datos desde ThingSpeak y los guarda en la base de datos automáticamente.
    """
    db = SessionLocal()
    try:
        logging.info("Iniciando la tarea automática de guardado de datos...")
        df, _ = fetch_data_from_thingspeak()
        if not df.empty:
            # Guardar datos originales
            save_original_data_to_db(db, df.to_dict(orient="records"))
            # Preprocesar y guardar datos limpios
            df_cleaned = preprocess_data(df)
            save_cleaned_data_to_db(db, df_cleaned.to_dict(orient="records"))
            logging.info("Datos originales y limpios guardados exitosamente.")
        else:
            logging.warning("No se encontraron datos en ThingSpeak.")
    except Exception as e:
        logging.error(f"Error en la tarea automática: {e}")
    finally:
        db.close()

# Configurar el job scheduler para que se ejecute cada 20 segundos
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_data, "interval", seconds=20)  # Cambiar "minutes=1" por "seconds=20"
scheduler.start()

# Crear tablas al iniciar la aplicación
@app.on_event("startup")
def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación.
    Crea las tablas en la base de datos.
    """
    logging.info("Creando tablas en la base de datos...")
    init_db()
    logging.info("Tablas creadas exitosamente.")

# Rutas raíz o de prueba
@app.get("/")
def root():
    return {"message": "¡Bienvenido a la API de Datos Climáticos!"}

# Detener el scheduler al cerrar la aplicación
@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
