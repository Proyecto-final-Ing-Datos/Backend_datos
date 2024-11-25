import pandas as pd
import logging

# Configuración básica de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def preprocess_data(df):
    """
    Limpia, transforma y valida los datos de un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos originales.

    Returns:
        pd.DataFrame: DataFrame preprocesado con columnas renombradas, tipos corregidos y valores nulos eliminados.
    """
    logging.info("Iniciando preprocesamiento de datos...")
    try:
        if df.empty:
            logging.warning("El DataFrame está vacío.")
            return df

        df.rename(columns={
            'field1': 'Temperatura (°C)',
            'field2': 'Humedad (%)',
            'field3': 'Presión Atmosférica (hPa)',
            'entry_id': 'id',
            'created_at': 'Fecha y Hora'
        }, inplace=True)

        df['Temperatura (°C)'] = pd.to_numeric(df['Temperatura (°C)'], errors='coerce')
        df['Humedad (%)'] = pd.to_numeric(df['Humedad (%)'], errors='coerce')
        df['Presión Atmosférica (hPa)'] = pd.to_numeric(df['Presión Atmosférica (hPa)'], errors='coerce')
        df['Fecha y Hora'] = pd.to_datetime(df['Fecha y Hora'], errors='coerce')

        df = df.dropna(subset=['Temperatura (°C)', 'Humedad (%)', 'Presión Atmosférica (hPa)'])
        logging.info("Preprocesamiento completado exitosamente.")
        return df
    except Exception as e:
        logging.error(f"Error en el preprocesamiento: {e}")
        raise

def detect_and_remove_duplicates_by_column(df, column):
    """
    Detecta y elimina filas duplicadas basadas en una columna específica.

    Args:
        df (pd.DataFrame): DataFrame original.
        column (str): Nombre de la columna para detectar duplicados.

    Returns:
        pd.DataFrame: DataFrame sin duplicados en la columna especificada.
    """
    logging.info(f"Detectando duplicados en la columna '{column}'...")
    if column not in df.columns:
        logging.warning(f"La columna '{column}' no existe en el DataFrame.")
        return df

    duplicates = df[df.duplicated(subset=[column], keep=False)]
    if not duplicates.empty:
        logging.info(f"Se detectaron {len(duplicates)} duplicados. Eliminando...")
        df = df.drop_duplicates(subset=[column], keep='first')
    else:
        logging.info("No se encontraron duplicados.")
    return df

def split_datetime_column_inplace(df, datetime_column):
    """
    Divide una columna datetime en 'Fecha', 'Hora' y 'Hora Solo'.

    Args:
        df (pd.DataFrame): DataFrame original.
        datetime_column (str): Nombre de la columna datetime.

    Returns:
        pd.DataFrame: DataFrame con columnas adicionales ('Fecha', 'Hora', 'Hora Solo').
    """
    logging.info(f"Dividiendo la columna '{datetime_column}' en 'Fecha', 'Hora' y 'Hora Solo'...")
    if datetime_column not in df.columns:
        logging.warning(f"La columna '{datetime_column}' no existe en el DataFrame.")
        return df

    try:
        df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')
        df['Fecha'] = df[datetime_column].dt.date
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df['Hora'] = df[datetime_column].dt.time
        df['Hora Solo'] = df[datetime_column].dt.floor('h').dt.time
        logging.info("División de columna completada exitosamente.")
    except Exception as e:
        logging.error(f"Error al dividir la columna datetime: {e}")
        raise
    return df

def enrich_data(df, channel_info):
    """
    Enriquecer los datos con información adicional del canal (latitud, longitud, etc.).

    Args:
        df (pd.DataFrame): DataFrame original.
        channel_info (dict): Información del canal de ThingSpeak.

    Returns:
        pd.DataFrame: DataFrame enriquecido con datos adicionales.
    """
    logging.info("Enriqueciendo los datos con información adicional...")
    try:
        if df.empty:
            logging.warning("El DataFrame está vacío. No se puede enriquecer.")
            return df

        df['Latitud'] = channel_info.get('latitude')
        df['Longitud'] = channel_info.get('longitude')
        df['Lugar'] = channel_info.get('location', "Desconocido")
        logging.info("Datos enriquecidos exitosamente.")
        return df
    except Exception as e:
        logging.error(f"Error al enriquecer datos: {e}")
        raise

def calculate_temperature_stats(df):
    """
    Calcula estadísticas por hora para la temperatura.

    Args:
        df (pd.DataFrame): DataFrame con columna 'Fecha y Hora' y 'Temperatura (°C)'.

    Returns:
        pd.DataFrame: DataFrame con estadísticas de temperatura ('max', 'min', 'mean') por hora.
    """
    logging.info("Calculando estadísticas de temperatura...")
    if 'Fecha y Hora' not in df.columns or 'Temperatura (°C)' not in df.columns:
        logging.warning("Las columnas requeridas no existen en el DataFrame.")
        return pd.DataFrame()

    try:
        df = df.set_index('Fecha y Hora')
        temp_stats = df['Temperatura (°C)'].resample('1h').agg(['max', 'min', 'mean']).dropna()
        temp_stats.rename(columns={
            'max': 'Temperatura Máxima (°C)',
            'min': 'Temperatura Mínima (°C)',
            'mean': 'Temperatura Promedio (°C)'
        }, inplace=True)
        logging.info("Estadísticas de temperatura calculadas exitosamente.")
        return temp_stats
    except Exception as e:
        logging.error(f"Error al calcular estadísticas de temperatura: {e}")
        raise
def calculate_humidity_stats(df):
    """
    Calcula estadísticas por hora para la humedad.
    """
    if 'Fecha y Hora' not in df.columns or 'Humedad (%)' not in df.columns:
        print("Las columnas 'Fecha y Hora' y 'Humedad (%)' deben existir en el DataFrame.")
        return pd.DataFrame()

    df = df.set_index('Fecha y Hora')

    # Calcular estadísticas por hora
    humidity_stats = df['Humedad (%)'].resample('1h').agg(['max', 'min', 'mean']).dropna()

    humidity_stats.rename(columns={
        'max': 'Humedad Máxima (%)',
        'min': 'Humedad Mínima (%)',
        'mean': 'Humedad Promedio (%)'
    }, inplace=True)

    return humidity_stats

def calculate_pressure_stats(df):
    """
    Calcula estadísticas por hora para la presión atmosférica.
    """
    if 'Fecha y Hora' not in df.columns or 'Presión Atmosférica (hPa)' not in df.columns:
        print("Las columnas 'Fecha y Hora' y 'Presión Atmosférica (hPa)' deben existir en el DataFrame.")
        return pd.DataFrame()

    # Asegurarse de que 'Fecha y Hora' sea un índice
    df = df.set_index('Fecha y Hora')

    # Calcular estadísticas por hora
    pressure_stats = df['Presión Atmosférica (hPa)'].resample('1h').agg(['max', 'min', 'mean']).dropna()

    # Renombrar columnas para mayor claridad
    pressure_stats.rename(columns={
        'max': 'Presión Máxima (hPa)',
        'min': 'Presión Mínima (hPa)',
        'mean': 'Presión Promedio (hPa)'
    }, inplace=True)

    return pressure_stats

def calculate_daily_stats_with_date_column(df):
    """
    Calcula los máximos, mínimos y promedios diarios para temperatura, humedad y presión.

    Args:
        df (pd.DataFrame): DataFrame con columnas 'Fecha', 'Temperatura (°C)', 'Humedad (%)', y 'Presión Atmosférica (hPa)'.

    Returns:
        pd.DataFrame: DataFrame con estadísticas diarias.
    """
    logging.info("Calculando estadísticas diarias...")
    if 'Fecha' not in df.columns or 'Temperatura (°C)' not in df.columns or 'Humedad (%)' not in df.columns or 'Presión Atmosférica (hPa)' not in df.columns:
        logging.warning("Las columnas requeridas no existen en el DataFrame.")
        return pd.DataFrame()

    try:
        daily_stats = df.groupby('Fecha').agg({
            'Temperatura (°C)': ['max', 'min', 'mean'],
            'Humedad (%)': ['max', 'min', 'mean'],
            'Presión Atmosférica (hPa)': ['max', 'min', 'mean']
        })
        daily_stats.columns = [
            'Temperatura Máxima (°C)', 'Temperatura Mínima (°C)', 'Temperatura Promedio (°C)',
            'Humedad Máxima (%)', 'Humedad Mínima (%)', 'Humedad Promedio (%)',
            'Presión Máxima (hPa)', 'Presión Mínima (hPa)', 'Presión Promedio (hPa)'
        ]
        daily_stats.reset_index(inplace=True)
        logging.info("Estadísticas diarias calculadas exitosamente.")
        return daily_stats
    except Exception as e:
        logging.error(f"Error al calcular estadísticas diarias: {e}")
        raise
