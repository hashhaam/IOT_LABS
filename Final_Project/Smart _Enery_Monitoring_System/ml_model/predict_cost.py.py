import joblib
import numpy as np

# Load model
model = joblib.load('ml_model/cost_predictor.pkl')

def predict_cost(Vrms, Irms, kWh):
    Power = Vrms * Irms
    input_data = np.array([[Vrms, Irms, Power, kWh]])
    return model.predict(input_data)[0]