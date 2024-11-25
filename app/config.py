from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "API de Datos Climáticos"
    debug: bool = True
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

class Config:
    """
    Clase para almacenar configuraciones clave de la aplicación.
    """
    # Configuración del servidor
    APP_NAME = "API de Datos Climáticos"
    APP_VERSION = "1.0.0"

    # Configuración de ThingSpeak
    THINGSPEAK_API_URL = os.getenv("THINGSPEAK_API_URL", "https://api.thingspeak.com/channels/2713472/feeds.json")
    THINGSPEAK_API_KEY = os.getenv("THINGSPEAK_API_KEY", "ZI1X7WOO76C8LS54")
    THINGSPEAK_RESULTS = os.getenv("THINGSPEAK_RESULTS", 100)

    # Configuración de la base de datos (PostgreSQL)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "climate_data")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

    # Configuración de entrenamiento
    LSTM_INPUT_DIM = int(os.getenv("LSTM_INPUT_DIM", 3))
    LSTM_HIDDEN_DIM = int(os.getenv("LSTM_HIDDEN_DIM", 150))
    LSTM_NUM_LAYERS = int(os.getenv("LSTM_NUM_LAYERS", 2))
    LSTM_OUTPUT_DIM = int(os.getenv("LSTM_OUTPUT_DIM", 3))
    LSTM_EPOCHS = int(os.getenv("LSTM_EPOCHS", 1000))
    LSTM_LEARNING_RATE = float(os.getenv("LSTM_LEARNING_RATE", 0.001))

    # Configuración de seguridad (JWT, si aplica)
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Otras configuraciones
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
