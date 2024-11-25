import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import logging

# Configuración básica de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Definir el modelo LSTM
class LSTMModel(nn.Module):
    """
    Modelo LSTM para predicción de series temporales.
    """
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(LSTMModel, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        # Definir la capa LSTM
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)

        # Capa Fully Connected (FC) para la salida
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        """
        Pasa los datos a través del modelo LSTM.
        """
        # Inicializar los estados oculto y de celda
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # Pasar los datos por la LSTM
        out, _ = self.lstm(x, (h0, c0))

        # Usar la última salida para la predicción
        out = self.fc(out[:, -1, :])
        return out

# Función para crear secuencias
def create_sequences(data, time_steps):
    """
    Crea secuencias para entrenar el modelo LSTM.

    Args:
        data (np.array): Datos escalados.
        time_steps (int): Número de pasos de tiempo a considerar.

    Returns:
        tuple: Arrays de secuencias y etiquetas.
    """
    sequences, labels = [], []
    for i in range(len(data) - time_steps):
        sequences.append(data[i:i + time_steps])
        labels.append(data[i + time_steps])
    return np.array(sequences), np.array(labels)

# Función para preparar los datos
def prepare_data(df, time_steps):
    """
    Escala y transforma los datos del DataFrame para el modelo.

    Args:
        df (pd.DataFrame): DataFrame con los datos originales.
        time_steps (int): Número de pasos de tiempo para las secuencias.

    Returns:
        tuple: Tensores de entrenamiento, prueba y escalador.
    """
    logging.info("Preparando los datos para el modelo LSTM...")
    try:
        # Seleccionar las columnas
        data = df[['Temperatura (°C)', 'Humedad (%)', 'Presión Atmosférica (hPa)']].values

        # Escalar los datos entre 0 y 1
        scaler = MinMaxScaler(feature_range=(0, 1))
        data_scaled = scaler.fit_transform(data)

        # Crear secuencias
        X, y = create_sequences(data_scaled, time_steps)

        # Dividir en datos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Convertir a tensores
        X_train = torch.tensor(X_train, dtype=torch.float32)
        X_test = torch.tensor(X_test, dtype=torch.float32)
        y_train = torch.tensor(y_train, dtype=torch.float32)
        y_test = torch.tensor(y_test, dtype=torch.float32)

        logging.info("Datos preparados exitosamente.")
        return X_train, X_test, y_train, y_test, scaler
    except Exception as e:
        logging.error(f"Error al preparar los datos: {e}")
        raise

# Función para entrenar el modelo
def train_model(model, X_train, y_train, num_epochs=1000, lr=0.001):
    """
    Entrena el modelo LSTM.

    Args:
        model (LSTMModel): Modelo LSTM a entrenar.
        X_train (torch.Tensor): Datos de entrada para entrenamiento.
        y_train (torch.Tensor): Etiquetas para entrenamiento.
        num_epochs (int): Número de épocas.
        lr (float): Tasa de aprendizaje.

    Returns:
        LSTMModel: Modelo entrenado.
    """
    logging.info("Iniciando el entrenamiento del modelo...")
    try:
        criterion = nn.MSELoss()  # Error cuadrático medio
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)

        for epoch in range(num_epochs):
            model.train()

            # Hacer las predicciones
            outputs = model(X_train)
            loss = criterion(outputs, y_train)

            # Backpropagation y optimización
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (epoch + 1) % 10 == 0:
                logging.info(f"Época [{epoch+1}/{num_epochs}], Pérdida: {loss.item():.4f}")

        logging.info("Entrenamiento del modelo completado.")
        return model
    except Exception as e:
        logging.error(f"Error durante el entrenamiento del modelo: {e}")
        raise

# Función para guardar el modelo
def save_model(model, path="lstm_model.pth"):
    """
    Guarda el modelo entrenado en un archivo.

    Args:
        model (LSTMModel): Modelo a guardar.
        path (str): Ruta del archivo donde guardar el modelo.
    """
    logging.info(f"Guardando el modelo en {path}...")
    try:
        torch.save(model.state_dict(), path)
        logging.info("Modelo guardado exitosamente.")
    except Exception as e:
        logging.error(f"Error al guardar el modelo: {e}")
        raise

# Función para cargar el modelo
def load_model(path="lstm_model.pth", input_dim=3, hidden_dim=150, num_layers=2, output_dim=3):
    """
    Carga un modelo previamente guardado.

    Args:
        path (str): Ruta del archivo del modelo guardado.
        input_dim (int): Dimensión de entrada.
        hidden_dim (int): Dimensión de las capas ocultas.
        num_layers (int): Número de capas.
        output_dim (int): Dimensión de salida.

    Returns:
        LSTMModel: Modelo cargado.
    """
    logging.info(f"Cargando el modelo desde {path}...")
    try:
        model = LSTMModel(input_dim, hidden_dim, num_layers, output_dim)
        model.load_state_dict(torch.load(path))
        model.eval()
        logging.info("Modelo cargado exitosamente.")
        return model
    except Exception as e:
        logging.error(f"Error al cargar el modelo: {e}")
        raise
