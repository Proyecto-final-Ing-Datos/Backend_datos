from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Settings

# Crear una instancia de Settings para acceder a las configuraciones
settings = Settings()

# Crear la URL de conexión a la base de datos utilizando la instancia de Settings
DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la clase base para los modelos
Base = declarative_base()

# Función para inicializar las tablas
def init_db():
    """
    Inicializa las tablas en la base de datos.
    """
    Base.metadata.create_all(bind=engine)

# Dependencia para usar en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
