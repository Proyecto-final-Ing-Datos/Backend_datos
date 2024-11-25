from sqlalchemy.orm import Session
from app.models import ClimateData
import logging
import unicodedata

def save_original_data_to_db(db: Session, data):
    """
    Guarda los datos originales en la base de datos.

    Args:
        db (Session): Sesión de la base de datos.
        data (list[dict]): Lista de datos originales.
    """
    logging.info("Guardando datos originales en la base de datos...")
    try:
        # Filtrar registros que tienen valores nulos en las columnas requeridas
        valid_data = [
            row for row in data
            if row.get("Temperatura (°C)") is not None
            and row.get("Humedad (%)") is not None
            and row.get("Presión Atmosférica (hPa)") is not None
            and row.get("Fecha y Hora") is not None
        ]

        if not valid_data:
            logging.warning("No hay datos válidos para guardar.")
            return

        for row in valid_data:
            climate_data = ClimateData(
                temperature=row.get("Temperatura (°C)"),
                humidity=row.get("Humedad (%)"),
                pressure=row.get("Presión Atmosférica (hPa)"),
                timestamp=row.get("Fecha y Hora"),
            )
            db.add(climate_data)
        db.commit()
        logging.info("Datos originales guardados exitosamente.")
    except Exception as e:
        db.rollback()
        logging.error(f"Error al guardar datos originales en la base de datos: {e}")
        raise


def save_cleaned_data_to_db(db: Session, data):
    """
    Guarda los datos limpios en la base de datos.

    Args:
        db (Session): Sesión de la base de datos.
        data (list[dict]): Lista de datos limpios.
    """
    logging.info("Guardando datos limpios en la base de datos...")
    try:
        for row in data:
            climate_data = ClimateData(
                temperature=row.get("Temperatura (°C)"),
                humidity=row.get("Humedad (%)"),
                pressure=row.get("Presión Atmosférica (hPa)"),
                timestamp=row.get("Fecha y Hora"),
            )
            db.add(climate_data)
        db.commit()
        logging.info("Datos limpios guardados exitosamente.")
    except Exception as e:
        db.rollback()
        logging.error(f"Error al guardar datos limpios en la base de datos: {e}")
        raise
