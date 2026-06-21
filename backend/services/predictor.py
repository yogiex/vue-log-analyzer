import joblib
import pandas as pd
from config import Config

def load_model(session):
    if session == 'grammar':
        return joblib.load(Config.MODEL_GRAMMAR)
    elif session == 'listening':
        return joblib.load(Config.MODEL_LISTENING)
    elif session == 'reading':
        return joblib.load(Config.MODEL_READING)
    else:
        raise ValueError("Sesi tidak valid")

def predict_anomalies(df, session):
    model = load_model(session)
    features = ... # siapkan fitur sesuai sesi
    df['anomaly'] = model.predict(features)  # HANYA predict, bukan fit_predict
    return df