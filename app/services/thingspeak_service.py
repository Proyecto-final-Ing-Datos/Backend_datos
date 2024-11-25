import pandas as pd
import requests
import logging

# Configuración básica de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# URL por defecto de ThingSpeak
THING_SPEAK_URL = "https://api.thingspeak.com/channels/2713472/feeds.json?api_key=ZI1X7WOO76C8LS54&results=100"

def fetch_data_from_thingspeak(url=THING_SPEAK_URL):
    """
    Obtiene datos del canal de ThingSpeak y devuelve un DataFrame y la información del canal.

    Args:
        url (str): URL del canal ThingSpeak.

    Returns:
        tuple: DataFrame con los datos y un diccionario con la información del canal.
    """
    logging.info(f"Obteniendo datos desde ThingSpeak: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        feeds = data.get('feeds', [])
        channel_info = data.get('channel', {})

        if not feeds:
            logging.warning("No se encontraron datos en 'feeds'. Verifica la URL o el canal.")
            return pd.DataFrame(), channel_info

        # Crear DataFrame a partir de los feeds
        df = pd.DataFrame(feeds)
        logging.info(f"Datos obtenidos exitosamente. Total de registros: {len(df)}")
        return df, channel_info
    except requests.RequestException as e:
        logging.error(f"Error en la solicitud HTTP: {e}")
    except Exception as e:
        logging.error(f"Error al obtener datos: {e}")
    return pd.DataFrame(), {}

def detect_and_remove_zeros(df, columns):
    """
    Detecta y elimina filas con valores `0` en las columnas especificadas.

    Args:
        df (pd.DataFrame): DataFrame original.
        columns (list): Lista de columnas a verificar.

    Returns:
        pd.DataFrame: DataFrame sin valores `0` en las columnas especificadas.
    """
    logging.info("Detectando y eliminando valores '0' en las columnas especificadas...")
    try:
        for column in columns:
            if column in df.columns:
                zero_rows = df[df[column] == 0]

                if not zero_rows.empty:
                    logging.warning(f"Se encontraron {len(zero_rows)} valores '0' en la columna '{column}'.")
                    df = df[df[column] != 0]
                else:
                    logging.info(f"No se encontraron valores '0' en la columna '{column}'.")

        logging.info("Eliminación de ceros completada.")
        return df
    except Exception as e:
        logging.error(f"Error al detectar y eliminar ceros: {e}")
        raise

def preprocess_data(df):
    """
    Limpia, transforma y valida los datos de un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame con los datos originales.

    Returns:
        pd.DataFrame: DataFrame preprocesado con columnas renombradas, tipos corregidos y valores nulos eliminados.
    """
    logging.info("Iniciando preprocesamiento de datos...")
    try:
        if df.empty:
            logging.warning("El DataFrame está vacío. No se puede procesar.")
            return df

        # Renombrar las columnas con nombres descriptivos
        df.rename(columns={
            'field1': 'Temperatura (°C)',
            'field2': 'Humedad (%)',
            'field3': 'Presión Atmosférica (hPa)',
            'entry_id': 'ID',
            'created_at': 'Fecha y Hora'
        }, inplace=True)

        # Convertir tipos de datos
        df['Temperatura (°C)'] = pd.to_numeric(df['Temperatura (°C)'], errors='coerce')
        df['Humedad (%)'] = pd.to_numeric(df['Humedad (%)'], errors='coerce')
        df['Presión Atmosférica (hPa)'] = pd.to_numeric(df['Presión Atmosférica (hPa)'], errors='coerce')
        df['Fecha y Hora'] = pd.to_datetime(df['Fecha y Hora'], errors='coerce')

        # Eliminar filas con valores nulos
        df = df.dropna(subset=['Temperatura (°C)', 'Humedad (%)', 'Presión Atmosférica (hPa)'])

        logging.info(f"Preprocesamiento completado. Total de registros válidos: {len(df)}")
        return df
    except Exception as e:
        logging.error(f"Error al preprocesar datos: {e}")
        raise
