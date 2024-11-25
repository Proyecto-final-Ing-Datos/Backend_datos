from fastapi import APIRouter
from app.services.thingspeak_service import fetch_data_from_thingspeak
from app.services.data_processing_service import (
    preprocess_data,
    detect_and_remove_duplicates_by_column,
    split_datetime_column_inplace,
    enrich_data,
    calculate_temperature_stats,
    calculate_humidity_stats,
    calculate_pressure_stats,
    calculate_daily_stats_with_date_column,
)

router = APIRouter()

@router.get("/original")
def get_original_data():
    """
    Devuelve los datos originales sin preprocesar desde ThingSpeak.
    """
    df, channel_info = fetch_data_from_thingspeak()
    if df.empty:
        return {"message": "No se encontraron datos originales."}
    return {"channel_info": channel_info, "data": df.to_dict(orient="records")}

@router.get("/cleaned")
def get_cleaned_data():
    """
    Devuelve los datos preprocesados.
    """
    df, _ = fetch_data_from_thingspeak()
    if df.empty:
        return {"message": "No se encontraron datos originales para limpiar."}

    df = preprocess_data(df)
    return {"data": df.to_dict(orient="records")}

@router.get("/processed-data")
def get_processed_data():
    """
    Endpoint para obtener datos procesados del canal ThingSpeak, enriquecidos y con estadísticas calculadas.
    """
    df, channel_info = fetch_data_from_thingspeak()
    if df.empty:
        return {"message": "No se encontraron datos en el canal ThingSpeak."}

    df = preprocess_data(df)
    df = detect_and_remove_duplicates_by_column(df, 'Fecha y Hora')
    df = split_datetime_column_inplace(df, 'Fecha y Hora')
    df = enrich_data(df, channel_info)

    temp_stats = calculate_temperature_stats(df)
    humidity_stats = calculate_humidity_stats(df)
    pressure_stats = calculate_pressure_stats(df)
    daily_stats = calculate_daily_stats_with_date_column(df)

    return {
        "processed_data": df.to_dict(orient="records"),
        "hourly_temperature_stats": temp_stats.to_dict(orient="records"),
        "hourly_humidity_stats": humidity_stats.to_dict(orient="records"),
        "hourly_pressure_stats": pressure_stats.to_dict(orient="records"),
        "daily_stats": daily_stats.to_dict(orient="records"),
    }
