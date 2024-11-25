from fastapi import APIRouter
import torch
from app.services.lstm_model_service import LSTMModel, prepare_data, train_model
from app.services.thingspeak_service import fetch_data_from_thingspeak
from app.services.data_processing_service import preprocess_data
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

router = APIRouter()

@router.post("/train")
def train_lstm_model():
    """
    Entrena el modelo LSTM con los datos climáticos.
    """
    df, _ = fetch_data_from_thingspeak()
    df = preprocess_data(df)

    if df.empty:
        return {"message": "No hay datos disponibles para entrenar el modelo."}

    time_steps = 24
    X_train, X_test, y_train, y_test, scaler = prepare_data(df, time_steps)

    input_dim = 3
    hidden_dim = 150
    num_layers = 2
    output_dim = 3
    model = LSTMModel(input_dim, hidden_dim, num_layers, output_dim)

    train_model(model, X_train, y_train)

    return {"message": "Modelo LSTM entrenado con éxito."}

@router.get("/predictions")
def get_predictions():
    """
    Genera predicciones basadas en los datos limpios.
    """
    df, _ = fetch_data_from_thingspeak()
    if df.empty:
        return {"message": "No se encontraron datos para generar predicciones."}

    df = preprocess_data(df)
    time_steps = 24
    X_train, X_test, y_train, y_test, scaler = prepare_data(df, time_steps)

    input_dim = 3
    hidden_dim = 150
    num_layers = 2
    output_dim = 3
    model = LSTMModel(input_dim, hidden_dim, num_layers, output_dim)
    model.load_state_dict(torch.load("lstm_model.pth"))
    model.eval()

    predictions = model(X_test).detach().numpy()
    predictions = scaler.inverse_transform(predictions)

    return {"predictions": predictions.tolist()}

@router.get("/evaluate")
def evaluate_model():
    """
    Evalúa el modelo LSTM y devuelve métricas y predicciones.
    """
    df, _ = fetch_data_from_thingspeak()
    if df.empty:
        return {"message": "No se encontraron datos para evaluar el modelo."}

    df = preprocess_data(df)
    time_steps = 24
    X_train, X_test, y_train, y_test, scaler = prepare_data(df, time_steps)

    input_dim = 3
    hidden_dim = 150
    num_layers = 2
    output_dim = 3
    model = LSTMModel(input_dim, hidden_dim, num_layers, output_dim)
    model.load_state_dict(torch.load("lstm_model.pth"))
    model.eval()

    criterion = torch.nn.MSELoss()
    with torch.no_grad():
        y_pred = model(X_test)
        test_loss = criterion(y_pred, y_test)
        y_pred_rescaled = scaler.inverse_transform(y_pred.numpy())
        y_test_rescaled = scaler.inverse_transform(y_test.numpy())

    mae_humedad = mean_absolute_error(y_test_rescaled[:, 1], y_pred_rescaled[:, 1])
    rmse_humedad = np.sqrt(mean_squared_error(y_test_rescaled[:, 1], y_pred_rescaled[:, 1]))

    mae_presion = mean_absolute_error(y_test_rescaled[:, 2], y_pred_rescaled[:, 2])
    rmse_presion = np.sqrt(mean_squared_error(y_test_rescaled[:, 2], y_pred_rescaled[:, 2]))

    return {
        "test_loss": test_loss.item(),
        "metrics": {
            "mae_humedad": mae_humedad,
            "rmse_humedad": rmse_humedad,
            "mae_presion": mae_presion,
            "rmse_presion": rmse_presion,
        },
        "predictions": y_pred_rescaled.tolist(),
    }
