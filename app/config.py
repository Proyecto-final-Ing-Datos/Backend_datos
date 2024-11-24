from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "API de Datos Climáticos"
    debug: bool = True
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
